# Tech Radar Data ETL

Automated technology scanning tool that analyzes GitHub repositories and generates tech radar data using AI.

## Features

- 🔍 Scans GitHub organizations for technology usage
- 🤖 AI-powered classification using OpenAI GPT-4o-mini
- 📊 Usage-based adoption level detection
- 🔄 Automatic pagination and rate limiting
- 💾 Progress checkpointing for resumability
- 📝 Comprehensive logging and error handling
- 🛡️ Circuit breaker pattern for API reliability

## Quick Start

### 1. Install Dependencies

```bash
cd data-etl
pip install -r requirements.txt
```

### 2. Configure Environment

Create `.env` file:

```bash
GITHUB_TOKEN=your_github_token_here
OPENAI_API_KEY=your_openai_key_here
```

⚠️ **Never commit `.env` file to git!**

### 3. Configure Scan

Edit `config/config.yaml`:

```yaml
github:
  organizations:
    - bazaartechnologies
  exclude_repos:
    - "*-archived"
    - "test-*"

openai:
  model: gpt-4o-mini
  max_tokens: 1000

output:
  file: ../data.ai.json
  format: pretty
```

### 4. Run Scan

```bash
# Scan all repos in configured organizations
python src/main.py

# Scan specific organization
python src/main.py --org bazaartechnologies

# Dry run (no file output)
python src/main.py --dry-run

# Resume from checkpoint
python src/main.py --resume
```

## How It Works

### 1. Repository Discovery
- Fetches all repositories from configured GitHub organizations
- Applies filters (archived, private, etc.)
- Handles pagination automatically

### 2. Technology Detection
Scans for technologies in:
- `package.json` (Node.js/JavaScript)
- `requirements.txt`, `Pipfile`, `pyproject.toml` (Python)
- `go.mod`, `go.sum` (Go)
- `Cargo.toml` (Rust)
- `pom.xml`, `build.gradle` (Java)
- `Gemfile` (Ruby)
- `composer.json` (PHP)
- `Dockerfile` (Docker)
- `.github/workflows/*.yml` (CI/CD tools)

### 3. AI Classification

For each discovered technology, AI determines:

**Quadrant** (Category):
- 0: Techniques (methodologies, practices)
- 1: Tools (development tools, testing frameworks)
- 2: Platforms (infrastructure, databases, cloud)
- 3: Languages & Frameworks

**Ring** (Adoption Level) - Usage-based:
- **Adopt** (0): Found in 70%+ of repos
- **Trial** (1): Found in 40-70% of repos
- **Assess** (2): Found in 10-40% of repos
- **Hold** (3): Found in <10% of repos

**Description**: AI-generated summary explaining:
- What the technology is
- Why it's in that ring
- Recommendations for usage

### 4. Output Generation

Creates `data.ai.json` with format:

```json
[
  {
    "name": "React",
    "quadrant": 3,
    "ring": 0,
    "description": "JavaScript library for building user interfaces. Found in 85% of repositories. Widely adopted, mature ecosystem.",
    "metadata": {
      "repos_count": 42,
      "usage_percentage": 85.7,
      "detected_versions": ["18.2.0", "17.0.2"],
      "confidence": "high"
    }
  }
]
```

User can review and manually rename to `data.json` when ready.

## Configuration Reference

### config.yaml

```yaml
github:
  # Organizations to scan
  organizations:
    - bazaartechnologies
    - another-org

  # Repository filters
  exclude_repos:
    - "*-archived"    # Exclude archived repos
    - "test-*"        # Exclude test repos
    - "legacy-*"      # Exclude legacy repos

  # Repository requirements
  min_stars: 0
  include_forks: false
  include_archived: false
  include_private: true

openai:
  # Model to use
  model: gpt-4o-mini  # or gpt-4o, gpt-4-turbo

  # Token limits
  max_tokens: 1000
  temperature: 0.3    # Lower = more consistent

  # Retry configuration
  max_retries: 3
  timeout: 30

classification:
  # Usage-based thresholds
  thresholds:
    adopt: 0.7    # 70%+
    trial: 0.4    # 40-70%
    assess: 0.1   # 10-40%
    # Below 10% = Hold

  # Minimum repos to be considered
  min_repos: 2

  # Technology filters
  exclude_patterns:
    - "*-internal"  # Exclude internal tools
    - "custom-*"    # Exclude custom tools

output:
  # Output file path (relative to data-etl/)
  file: ../data.ai.json

  # Format: pretty or compact
  format: pretty

  # Include metadata
  include_metadata: true

  # Sort by usage
  sort_by: usage  # or name, ring

logging:
  # Log level
  level: INFO  # DEBUG, INFO, WARNING, ERROR

  # Log file
  file: logs/scan.log

  # Console output
  console: true

# Rate limiting
rate_limit:
  # Max requests per minute (GitHub search API limit is 30)
  max_per_minute: 25

  # Safety threshold (pause if remaining < this)
  safety_threshold: 100

# Progress tracking
checkpoint:
  enabled: true
  file: .scan_progress.json
  save_interval: 10  # Save every N repos
```

## CLI Commands

```bash
# Basic scan
python src/main.py

# Scan specific org
python src/main.py --org myorg

# Dry run (preview only)
python src/main.py --dry-run

# Resume from checkpoint
python src/main.py --resume

# Clear checkpoint and start fresh
python src/main.py --fresh

# Verbose output
python src/main.py --verbose

# Custom config file
python src/main.py --config custom-config.yaml

# Output to custom file
python src/main.py --output custom-output.json
```

## Error Handling

### Rate Limiting
- Automatically pauses when approaching GitHub API limits
- Uses exponential backoff for retries
- Displays estimated wait time

### Network Errors
- Automatic retry with exponential backoff (max 5 attempts)
- Circuit breaker opens after 5 consecutive failures
- Progress saved via checkpoints - resume anytime

### API Errors
- Invalid tokens → Clear error message with setup instructions
- Quota exceeded → Pause and notify user
- Parse errors → Log and skip problematic repos

## Monitoring

### Progress Tracking
```
Scanning repositories...
[=========>        ] 45/100 repos (45%)
Current: bazaartechnologies/frontend-app
Technologies found: 23
ETA: 5 minutes
```

### Logs
All operations logged to:
- Console (INFO level)
- `logs/scan.log` (DEBUG level)
- `logs/errors.log` (ERROR level only)

### Metrics
Final report includes:
- Repositories scanned
- Technologies discovered
- API calls made
- Errors encountered
- Duration and rate

## Troubleshooting

### "Authentication failed"
- Check your GitHub token in `.env`
- Ensure token has `repo` and `read:org` scopes
- Regenerate token if compromised

### "Rate limit exceeded"
- Wait for rate limit reset (check logs for time)
- Reduce `max_per_minute` in config
- Use GitHub GraphQL API (more efficient)

### "OpenAI API error"
- Check API key in `.env`
- Verify OpenAI account has credits
- Check model name is correct (`gpt-4o-mini`)

### Empty or incomplete results
- Check logs in `logs/scan.log`
- Verify organization name is correct
- Ensure repos contain recognizable tech files
- Use `--verbose` flag for detailed output

### Scan is too slow
- GitHub has strict rate limits (5000/hour)
- Use GraphQL mode (add `--graphql` flag)
- Scan fewer repositories
- Run during off-peak hours

## Best Practices

### Regular Scans
Schedule weekly scans via cron:
```bash
# Every Monday at 2 AM
0 2 * * 1 cd /path/to/data-etl && python src/main.py >> logs/cron.log 2>&1
```

### Review AI Results
Always review `data.ai.json` before using:
1. Check classifications make sense
2. Verify descriptions are accurate
3. Adjust rings if needed
4. Remove irrelevant entries
5. Rename to `data.json` when ready

### Version Control
- Commit `data.ai.json` to track changes over time
- Use git diff to see what changed
- Keep history of tech stack evolution

### Multi-Org Scanning
For multiple organizations:
```yaml
github:
  organizations:
    - bazaartechnologies
    - partner-org
    - client-org
```

## Security

### API Keys
- Store in `.env` (never commit!)
- Use environment variables in CI/CD
- Rotate keys regularly
- Use minimum required scopes

### Data Privacy
- Tool only reads public repository data
- No code content is sent to OpenAI
- Only package names and versions analyzed
- Review logs before sharing

## Development

### Running Tests
```bash
pytest tests/
pytest tests/ --cov=src  # With coverage
```

### Adding New Tech Detectors
Edit `src/detectors.py`:
```python
def detect_scala(repo):
    """Detect Scala projects"""
    if repo.has_file('build.sbt'):
        return parse_sbt_file(repo.get_file('build.sbt'))
    return []
```

### Custom Classification Logic
Edit `src/classifier.py`:
```python
def classify_custom(tech, usage_data):
    """Custom classification logic"""
    if tech.name == 'SpecialTool':
        return Ring.ADOPT  # Force specific ring
    return classify_by_usage(tech, usage_data)
```

## Architecture

```
data-etl/
├── src/
│   ├── main.py           # Entry point, CLI
│   ├── scanner.py        # GitHub scanning logic
│   ├── detector.py       # Technology detection
│   ├── classifier.py     # AI classification
│   ├── rate_limiter.py   # Rate limiting
│   ├── utils.py          # Helpers
│   └── config.py         # Config loader
├── tests/
│   ├── test_scanner.py
│   ├── test_detector.py
│   └── test_classifier.py
├── config/
│   ├── config.yaml       # Main config
│   └── config.example.yaml
├── logs/                 # Generated logs
├── .env                  # API keys (git-ignored)
├── .env.example          # Template
├── requirements.txt      # Dependencies
└── README.md
```

## License

Open source - use and modify as needed.

## Support

For issues or questions:
1. Check logs in `logs/scan.log`
2. Review this README
3. Check GitHub API status: https://www.githubstatus.com
4. Check OpenAI status: https://status.openai.com
