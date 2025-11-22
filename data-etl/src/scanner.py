"""
GitHub repository scanner with pagination and rate limiting.
"""

import logging
import fnmatch
from typing import List, Dict, Set, Optional
from github import Github
from github.Repository import Repository
from github.GithubException import GithubException

from rate_limiter import RateLimiter, CircuitBreaker
from detector import TechnologyDetector

logger = logging.getLogger(__name__)


class GitHubScanner:
    """Scans GitHub repositories for technology usage."""

    def __init__(self, github_token: str, config: dict):
        """
        Initialize scanner.

        Args:
            github_token: GitHub personal access token
            config: Configuration dictionary
        """
        self.github = Github(github_token, per_page=100)
        self.config = config
        self.rate_limiter = RateLimiter(
            self.github,
            max_per_minute=config.get('rate_limit', {}).get('max_per_minute', 25),
            safety_threshold=config.get('rate_limit', {}).get('safety_threshold', 100)
        )
        self.circuit_breaker = CircuitBreaker(failure_threshold=5, timeout=60)
        self.detector = TechnologyDetector()

        # Get repo limit from config (can be overridden externally)
        config_limit = config.get('github', {}).get('repo_limit', 0)
        self.repo_limit = config_limit if config_limit > 0 else None

        # Stats
        self.stats = {
            'repos_scanned': 0,
            'repos_skipped': 0,
            'api_calls': 0,
            'errors': 0
        }

    def scan_organizations(
        self,
        progress_callback: Optional[callable] = None
    ) -> tuple[Dict[str, int], List[Dict]]:
        """
        Scan all configured organizations.

        Args:
            progress_callback: Optional callback(current, total, repo_name)

        Returns:
            Tuple of (tech_counts, repo_details)
        """
        orgs = self.config['github']['organizations']
        all_repo_techs = []
        repo_details = []

        for org_name in orgs:
            logger.info(f"Scanning organization: {org_name}")

            try:
                org_techs, org_repos = self.scan_organization(
                    org_name,
                    progress_callback
                )
                all_repo_techs.extend(org_techs)
                repo_details.extend(org_repos)

            except GithubException as e:
                logger.error(f"Error accessing organization {org_name}: {e}")
                self.stats['errors'] += 1
            except Exception as e:
                logger.error(f"Unexpected error scanning {org_name}: {e}")
                self.stats['errors'] += 1

        # Aggregate technologies
        tech_counts = self.detector.aggregate_technologies(all_repo_techs)

        logger.info(f"Scan complete. Found {len(tech_counts)} unique technologies.")
        return tech_counts, repo_details

    def scan_organization(
        self,
        org_name: str,
        progress_callback: Optional[callable] = None
    ) -> tuple[List[Dict[str, Set[str]]], List[Dict]]:
        """
        Scan all repositories in an organization.

        Args:
            org_name: Organization name
            progress_callback: Optional progress callback

        Returns:
            Tuple of (list of repo technologies, list of repo details)
        """
        self.rate_limiter.check_and_wait()
        self.stats['api_calls'] += 1

        org = self.github.get_organization(org_name)
        repos = list(org.get_repos())

        # Apply limit if specified
        total_repos = len(repos)
        if self.repo_limit and self.repo_limit < total_repos:
            repos = repos[:self.repo_limit]
            logger.info(f"Found {total_repos} repositories in {org_name}, limiting to {self.repo_limit}")
        else:
            logger.info(f"Found {len(repos)} repositories in {org_name}")

        all_repo_techs = []
        repo_details = []

        for idx, repo in enumerate(repos):
            # Check if should skip
            if self._should_skip_repo(repo):
                logger.debug(f"Skipping {repo.name} (filtered)")
                self.stats['repos_skipped'] += 1
                continue

            # Progress callback
            if progress_callback:
                progress_callback(idx + 1, len(repos), repo.name)

            try:
                # Scan repository with circuit breaker protection
                techs = self.circuit_breaker.call(
                    self._scan_repository,
                    repo
                )

                if techs:
                    all_repo_techs.append(techs)
                    repo_details.append({
                        'name': repo.name,
                        'full_name': repo.full_name,
                        'url': repo.html_url,
                        'stars': repo.stargazers_count,
                        'technologies': techs
                    })

                self.stats['repos_scanned'] += 1

            except Exception as e:
                logger.error(f"Error scanning {repo.name}: {e}")
                self.stats['errors'] += 1

        return all_repo_techs, repo_details

    def _scan_repository(self, repo: Repository) -> Dict[str, Set[str]]:
        """
        Scan a single repository for technologies.

        Args:
            repo: Repository object

        Returns:
            Dict of technologies by category
        """
        logger.debug(f"Scanning repository: {repo.name}")

        # Rate limiting
        self.rate_limiter.check_and_wait()
        self.stats['api_calls'] += 1

        # Detect technologies
        technologies = self.detector.detect_technologies(repo)

        # Log what we found
        tech_count = sum(len(techs) for techs in technologies.values())
        if tech_count > 0:
            logger.info(f"  {repo.name}: Found {tech_count} technologies")

        return technologies

    def _should_skip_repo(self, repo: Repository) -> bool:
        """
        Check if repository should be skipped based on filters.

        Args:
            repo: Repository object

        Returns:
            True if should skip
        """
        config = self.config['github']

        # Check archived
        if repo.archived and not config.get('include_archived', False):
            return True

        # Check fork
        if repo.fork and not config.get('include_forks', False):
            return True

        # Check private
        if repo.private and not config.get('include_private', True):
            return True

        # Check stars
        min_stars = config.get('min_stars', 0)
        if repo.stargazers_count < min_stars:
            return True

        # Check exclude patterns
        exclude_patterns = config.get('exclude_repos', [])
        for pattern in exclude_patterns:
            if fnmatch.fnmatch(repo.name, pattern):
                return True

        return False

    def get_stats(self) -> dict:
        """Get scanning statistics."""
        return {
            **self.stats,
            'rate_limit': self.rate_limiter.get_status()
        }
