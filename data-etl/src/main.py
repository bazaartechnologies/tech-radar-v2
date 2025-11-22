#!/usr/bin/env python3
"""
Tech Radar Data ETL - Main Entry Point

Scans GitHub repositories and generates tech radar data using AI.
"""

import sys
import json
import argparse
import logging
from pathlib import Path
from datetime import datetime

from config import Config, setup_logging
from scanner import GitHubScanner
from classifier import TechnologyClassifier
from progress import ProgressTracker, ProgressDisplay

logger = logging.getLogger(__name__)


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description='Tech Radar Data ETL - Scan GitHub repos and generate tech radar data',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run with default config
  python main.py

  # Scan specific organization
  python main.py --org myorg

  # Limit to first 100 repos (fast testing)
  python main.py --limit 100

  # Dry run (no file output)
  python main.py --dry-run

  # Quick test: scan 50 repos in dry-run mode
  python main.py --limit 50 --dry-run

  # Resume from checkpoint
  python main.py --resume

  # Start fresh (clear checkpoint)
  python main.py --fresh

  # Custom config and output
  python main.py --config custom.yaml --output custom.ai.json
        """
    )

    parser.add_argument(
        '--config',
        type=str,
        help='Path to config YAML file (default: config/config.yaml)'
    )

    parser.add_argument(
        '--org',
        type=str,
        help='Override organization to scan (overrides config)'
    )

    parser.add_argument(
        '--output',
        type=str,
        help='Override output file path (overrides config)'
    )

    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Run scan but do not write output file'
    )

    parser.add_argument(
        '--resume',
        action='store_true',
        help='Resume from checkpoint (skip already scanned repos)'
    )

    parser.add_argument(
        '--fresh',
        action='store_true',
        help='Start fresh (clear checkpoint and rescan all)'
    )

    parser.add_argument(
        '--verbose',
        '-v',
        action='store_true',
        help='Enable verbose output (DEBUG level)'
    )

    parser.add_argument(
        '--limit',
        type=int,
        help='Limit number of repositories to scan (e.g., --limit 100)'
    )

    return parser.parse_args()


def write_output(data: list, output_path: Path, config: Config) -> None:
    """
    Write data to output file.

    Args:
        data: List of technology entries
        output_path: Output file path
        config: Configuration
    """
    try:
        # Sort data
        sort_by = config['output'].get('sort_by', 'usage')
        if sort_by == 'usage':
            data.sort(key=lambda x: x['metadata']['usage_percentage'], reverse=True)
        elif sort_by == 'name':
            data.sort(key=lambda x: x['name'])
        elif sort_by == 'ring':
            data.sort(key=lambda x: (x['ring'], x['name']))

        # Remove metadata if not wanted
        if not config['output'].get('include_metadata', True):
            for entry in data:
                entry.pop('metadata', None)

        # Write file
        output_path.parent.mkdir(parents=True, exist_ok=True)

        indent = 2 if config['output'].get('format') == 'pretty' else None

        with open(output_path, 'w') as f:
            json.dump(data, f, indent=indent)

        logger.info(f"✓ Written {len(data)} technologies to {output_path}")

    except Exception as e:
        logger.error(f"Error writing output file: {e}")
        raise


def print_summary(data: list, stats: dict, config: Config) -> None:
    """
    Print summary statistics.

    Args:
        data: List of technology entries
        stats: Scanning statistics
        config: Configuration
    """
    print("\n" + "=" * 70)
    print("SCAN SUMMARY")
    print("=" * 70)

    # Repositories
    print(f"\n📦 Repositories:")
    print(f"  Scanned:  {stats['repos_scanned']}")
    print(f"  Skipped:  {stats['repos_skipped']}")
    print(f"  Errors:   {stats['errors']}")

    # Technologies by ring
    print(f"\n🎯 Technologies by Ring:")
    by_ring = {}
    for entry in data:
        ring = entry['ring']
        by_ring[ring] = by_ring.get(ring, 0) + 1

    ring_names = {0: 'Adopt', 1: 'Trial', 2: 'Assess', 3: 'Hold'}
    for ring in sorted(by_ring.keys()):
        print(f"  {ring_names[ring]:<8} {by_ring[ring]:>3} technologies")

    # Technologies by quadrant
    print(f"\n📊 Technologies by Quadrant:")
    by_quadrant = {}
    for entry in data:
        quadrant = entry['quadrant']
        by_quadrant[quadrant] = by_quadrant.get(quadrant, 0) + 1

    quadrant_names = {
        0: 'Techniques',
        1: 'Tools',
        2: 'Platforms',
        3: 'Languages & Frameworks'
    }
    for quadrant in sorted(by_quadrant.keys()):
        print(f"  {quadrant_names[quadrant]:<25} {by_quadrant[quadrant]:>3} technologies")

    # API usage
    print(f"\n🌐 API Usage:")
    print(f"  API calls:     {stats['api_calls']}")
    if 'rate_limit' in stats:
        rl = stats['rate_limit']
        print(f"  Rate limit:    {rl['remaining']}/{rl['limit']} remaining")

    # Output
    output_path = config.get_output_path()
    print(f"\n💾 Output:")
    print(f"  File: {output_path}")
    print(f"  Next steps:")
    print(f"    1. Review the file for accuracy")
    print(f"    2. Adjust classifications if needed")
    print(f"    3. Rename to 'data.json' to use in tech radar")

    print("\n" + "=" * 70 + "\n")


def main():
    """Main entry point."""
    args = parse_args()

    try:
        # Load configuration
        config = Config(args.config)

        # Setup logging
        if args.verbose:
            config.config['logging']['level'] = 'DEBUG'
        setup_logging(config)

        logger.info("=" * 70)
        logger.info("Tech Radar Data ETL")
        logger.info("=" * 70)

        # Override config with CLI args
        if args.org:
            config.config['github']['organizations'] = [args.org]
            logger.info(f"Overriding organization: {args.org}")

        output_path = Path(args.output) if args.output else config.get_output_path()

        # Initialize progress tracker
        checkpoint_enabled = config['checkpoint'].get('enabled', True) and args.resume
        if args.fresh:
            checkpoint_enabled = False

        progress_tracker = ProgressTracker(
            config.get_checkpoint_path(),
            enabled=checkpoint_enabled
        )

        if args.fresh:
            progress_tracker.clear()
            logger.info("Starting fresh scan (checkpoint cleared)")
        elif args.resume:
            progress = progress_tracker.get_progress()
            logger.info(f"Resuming scan ({progress['scanned_repos']} repos already scanned)")

        progress_tracker.start_scan()

        # Initialize scanner
        logger.info("Initializing GitHub scanner...")
        scanner = GitHubScanner(
            config.get_github_token(),
            config.to_dict()
        )

        # Set repo limit if specified
        if args.limit:
            scanner.repo_limit = args.limit
            logger.info(f"Limiting scan to {args.limit} repositories")

        # Scan repositories
        logger.info("Scanning repositories...")
        print()

        tech_counts, repo_details = scanner.scan_organizations()

        stats = scanner.get_stats()
        progress_tracker.update_stats(stats)

        logger.info(f"Found {len(tech_counts)} unique technologies")

        if not tech_counts:
            logger.warning("No technologies found! Check your configuration and repository access.")
            return 1

        # Classify technologies
        logger.info("Classifying technologies with AI...")
        classifier = TechnologyClassifier(
            config.get_openai_key(),
            config.to_dict()
        )

        total_repos = stats['repos_scanned']
        classified_data = classifier.classify_technologies(
            tech_counts,
            total_repos,
            repo_details
        )

        logger.info(f"Classified {len(classified_data)} technologies")

        # Write output
        if args.dry_run:
            logger.info("Dry run - skipping file write")
            print(f"\n📋 Preview (first 5 entries):")
            for entry in classified_data[:5]:
                print(f"\n  {entry['name']}")
                print(f"    Ring: {entry['ring']} | Quadrant: {entry['quadrant']}")
                print(f"    Usage: {entry['metadata']['usage_percentage']:.1f}%")
                print(f"    {entry['description'][:80]}...")
        else:
            write_output(classified_data, output_path, config)

        # Print summary
        print_summary(classified_data, stats, config)

        # Finalize
        progress_tracker.finalize()

        logger.info("Scan completed successfully!")
        return 0

    except KeyboardInterrupt:
        logger.warning("\nScan interrupted by user")
        return 130

    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        print(f"\n❌ Error: {e}")
        print("\nTroubleshooting:")
        print("  1. Check your .env file has valid tokens")
        print("  2. Verify organization name is correct")
        print("  3. Check logs in logs/scan.log")
        print("  4. Run with --verbose for detailed output")
        return 1


if __name__ == '__main__':
    sys.exit(main())
