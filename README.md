# Technology Radar - AI-Powered & Interactive

A world-class interactive technology radar with AI-powered data collection and stunning UI/UX, inspired by Thoughtworks. Automatically scans GitHub organizations to detect technologies, analyze adoption patterns, and classify them with domain-aware intelligence.

## 🤖 Key Features

- **AI-Powered Technology Detection**: Automatically scans GitHub repositories to identify technologies
- **Domain-Aware Classification**: Segments analysis by engineering domain (mobile, backend, frontend, infrastructure, etc.)
- **Temporal Analysis**: Tracks adoption trends over time (recent, legacy, active, stale repos)
- **Smart Ring Decisions**: AI-assisted classification into Adopt/Trial/Assess/Hold rings
- **Resumable Scanning**: Checkpoint system allows pausing and resuming long scans
- **Rate-Limited & Safe**: Respects GitHub API limits with intelligent throttling
- **Organization-Agnostic**: Works with any GitHub organization without hardcoded patterns

## 🚀 Quick Start

### Option 1: View the Radar (Frontend Only)

**⚠️ Important:** Due to browser security (CORS), you need to run a local server. Opening `index.html` directly won't work.

#### Easiest Method - Use the Startup Script

**macOS/Linux:**
```bash
./start.sh
```

**Windows:**
```cmd
start.bat
```

Then open http://localhost:8000 in your browser.

### Alternative Methods

```bash
# Option 1: Python (recommended)
python3 -m http.server 8000

# Option 2: Node.js
npx serve

# Option 3: PHP
php -S localhost:8000
```

**To add a technology:**
- **Manual**: Edit `data.json` → Add new entry → Save → Refresh browser
- **Automated**: Use the ETL pipeline (see Option 2 below)

### Option 2: Generate Data Automatically (AI-Powered ETL)

**Prerequisites:**
- Python 3.8+
- GitHub Personal Access Token
- OpenAI API Key

**Setup:**
```bash
cd data-etl

# Install dependencies
pip3 install -r requirements.txt

# Configure your organization
# Edit config/config.yaml and set:
#   - github.organizations: [your-org-name]
#   - Add GITHUB_TOKEN to environment
#   - Add OPENAI_API_KEY to environment

export GITHUB_TOKEN="ghp_your_token_here"
export OPENAI_API_KEY="sk-your_key_here"

# Run the scanner
python3 src/main.py
```

**Advanced Usage:**

```bash
# Limit to first 50 repos (for testing)
python3 src/main.py --limit 50

# Resume from checkpoint if interrupted
python3 src/main.py --resume

# Clear checkpoint and start fresh
python3 src/main.py --clear-checkpoint

# Combine options
python3 src/main.py --limit 100 --resume
```

The ETL pipeline will:
1. Scan all repositories in your GitHub organization
2. Detect technologies from file patterns and languages
3. Use AI to determine repository domain (mobile, backend, etc.)
4. Analyze temporal patterns (recent adoption, legacy usage, activity)
5. Classify technologies into rings with AI assistance
6. Generate domain-specific breakdowns
7. Output to `data.json` with rich metadata

## 📋 Quick Reference

| Action | File | What to Edit |
|--------|------|--------------|
| Add technology | `data.json` | Add new `{ name, quadrant, ring, description }` |
| Move ring | `data.json` | Change `ring` value (0=Adopt, 1=Trial, 2=Assess, 3=Hold) |
| Change category | `data.json` | Change `quadrant` value (0=Techniques, 1=Tools, 2=Platforms, 3=Languages) |
| Rename quadrant | `radar.js` | Edit `quadrants` array names |
| Change colors | `styles.css` or `radar.js` | Edit CSS variables or ring colors |
| Customize theme | `styles.css` | Edit `:root` variables |

## 📊 Data Schema

### Output Format (`data.json` / `data.ai.json`)

The ETL pipeline generates a JSON file with the following structure:

```json
[
  {
    "name": "Java",
    "quadrant": 3,
    "ring": 2,
    "description": "Java is used in 61.5% of repositories...",
    "confidence": 0.85,
    "metadata": {
      "repos_count": 24,
      "usage_percentage": 61.5,
      "total_repos": 39,
      "ai_confidence": "high",
      "ai_model": "gpt-4o-mini",
      "temporal_data": {
        "total_repos": 24,
        "recent_repos": 0,
        "new_repos": 0,
        "legacy_repos": 24,
        "active_repos": 16,
        "stale_repos": 8,
        "avg_age_months": 58.2,
        "trend": "STABLE",
        "recency_score": 0.0,
        "activity_score": 0.667,
        "repos_list": ["repo1", "repo2"],
        "by_domain": {
          "mobile": {
            "total_repos": 7,
            "recent_repos": 0,
            "new_repos": 0,
            "active_repos": 5,
            "recency_score": 0.0,
            "activity_score": 0.714,
            "trend": "STABLE"
          },
          "backend": {
            "total_repos": 11,
            "recent_repos": 0,
            "new_repos": 0,
            "active_repos": 9,
            "recency_score": 0.0,
            "activity_score": 0.818,
            "trend": "STABLE"
          }
        }
      },
      "usage_score": 0.615,
      "recency_score": 0.0,
      "activity_score": 0.667,
      "domain_breakdown": {
        "mobile": {
          "suggested_ring": 0,
          "ring_name": "Adopt",
          "confidence": 0.9,
          "total_repos": 7,
          "recent_repos": 0,
          "activity_score": 0.714,
          "trend": "STABLE"
        },
        "backend": {
          "suggested_ring": 0,
          "ring_name": "Adopt",
          "confidence": 0.9,
          "total_repos": 11,
          "recent_repos": 0,
          "activity_score": 0.818,
          "trend": "STABLE"
        }
      }
    },
    "decision_factors": [
      "✓ High usage (61.5%)",
      "✗ No new adoption in last 6 months",
      "• 67% of repos actively maintained",
      "➡ Trend: STABLE"
    ],
    "needs_review": false
  }
]
```

### Field Descriptions

**Core Fields:**
- `name`: Technology name (e.g., "Java", "React", "Kubernetes")
- `quadrant`: Category (0=Techniques, 1=Tools, 2=Platforms, 3=Languages & Frameworks)
- `ring`: Adoption level (0=Adopt, 1=Trial, 2=Assess, 3=Hold)
- `description`: AI-generated description explaining the classification
- `confidence`: AI confidence score (0.0-1.0)

**Metadata:**
- `repos_count`: Number of repositories using this technology
- `usage_percentage`: Percentage of total repositories
- `ai_confidence`: "high", "medium", or "low"
- `ai_model`: OpenAI model used for classification

**Temporal Data:**
- `total_repos`: Total repositories using this tech
- `recent_repos`: Repos with activity in last 6 months
- `new_repos`: Repos created in last 6 months
- `legacy_repos`: Repos older than 2 years
- `active_repos`: Repos with commits in last 3 months
- `stale_repos`: Repos with no commits in last 6 months
- `avg_age_months`: Average repository age
- `trend`: "GROWING", "STABLE", "DECLINING", or "ABANDONED"
- `recency_score`: Normalized recency metric (0.0-1.0)
- `activity_score`: Normalized activity metric (0.0-1.0)
- `by_domain`: Per-domain breakdown of temporal metrics

**Domain Breakdown:**
- Per-domain classification showing different rings for different contexts
- Example: Java might be "Adopt" for mobile but "Assess" for backend
- Each domain includes: suggested_ring, ring_name, confidence, metrics

**Decision Factors:**
- Human-readable list explaining the classification reasoning
- Shows key metrics that influenced the decision

**Supported Domains:**
- `mobile`: Mobile applications (iOS, Android, React Native, Flutter)
- `backend`: Backend services and APIs
- `frontend`: Web frontend applications
- `infrastructure`: DevOps, IaC, deployment tools
- `data`: Data engineering, ETL, analytics
- `ml`: Machine learning and AI projects
- `library`: Shared libraries and SDKs
- `tooling`: Developer tools and utilities

## 🔄 ETL Pipeline Features

### Resume Capability
The scanner saves checkpoints every 10 repositories (configurable). If interrupted:
```bash
python3 src/main.py --resume
```

### Checkpoint Files
- `.scan_progress.json`: Tracks scan progress (repos processed, last position)
- Automatically created during scans
- Can be cleared with `--clear-checkpoint`

### Rate Limiting
- Respects GitHub API limits (30 searches/minute)
- Configurable safety threshold (default: pause at 100 remaining requests)
- Automatic retry with exponential backoff

### Configuration (`config/config.yaml`)
```yaml
github:
  organizations: [your-org-name]
  repo_limit: 0  # 0 = scan all, or set a limit for testing
  min_stars: 0
  include_private: true
  include_archived: false

openai:
  model: gpt-4o-mini
  max_tokens: 1000
  temperature: 0.3

classification:
  min_repos: 2  # Minimum repos to include a technology
  thresholds:
    adopt: 0.70   # 70%+ usage
    trial: 0.40   # 40-70% usage
    assess: 0.10  # 10-40% usage

checkpoint:
  enabled: true
  save_interval: 10  # Save every N repos
```

## Philosophy

This radar follows the Thoughtworks approach:

- **Adopt**: Technologies we have high confidence in. Use them when appropriate.
- **Trial**: Technologies worth pursuing. Worth investing to see if they have impact.
- **Assess**: Technologies worth exploring to understand how they will affect you.
- **Hold**: Proceed with caution. Not recommended for new projects.

## Quadrants

1. **Techniques**: Practices, processes, and methodologies
2. **Tools**: Development tools, DevOps tools, testing frameworks
3. **Platforms**: Infrastructure, cloud services, databases
4. **Languages & Frameworks**: Programming languages and frameworks

## 📖 How-To Guides

### How to Add a New Technology

1. **Open `data.json`** in your text editor
2. **Add a new entry** to the array with this structure:

```json
{
  "name": "Technology Name",
  "quadrant": 0,
  "ring": 0,
  "description": "Brief description explaining the technology and our stance on it."
}
```

3. **Set the quadrant** (category):
   - `0` = Techniques (practices, methodologies)
   - `1` = Tools (development tools, testing frameworks)
   - `2` = Platforms (infrastructure, cloud, databases)
   - `3` = Languages & Frameworks

4. **Set the ring** (adoption level):
   - `0` = Adopt (proven, recommended)
   - `1` = Trial (worth pursuing)
   - `2` = Assess (worth exploring)
   - `3` = Hold (proceed with caution)

5. **Save the file** - refresh your browser to see changes

**Example - Adding Go to Trial:**
```json
{
  "name": "Go (Golang)",
  "quadrant": 3,
  "ring": 1,
  "description": "Fast, statically typed language for microservices and cloud-native applications."
}
```

### How to Move a Technology to a Different Ring

1. **Open `data.json`**
2. **Find the technology** you want to move
3. **Change the `ring` value**:
   - Moving from Trial (1) to Adopt (0)
   - Moving from Assess (2) to Trial (1)
   - etc.
4. **Update the description** to explain why it moved
5. **Save and refresh**

**Example - Moving Next.js from Trial to Adopt:**
```json
{
  "name": "Next.js",
  "quadrant": 3,
  "ring": 0,  // Changed from 1 to 0
  "description": "React framework now proven in production. Recommended for new React projects."
}
```

### How to Remove a Technology

1. **Open `data.json`**
2. **Find the technology entry** (including the curly braces `{ }`)
3. **Delete the entire entry** including the comma after it
4. **Save and refresh**

⚠️ **Important:** Make sure to maintain valid JSON format (commas between entries, but not after the last one)

### How to Change Quadrant Names

1. **Open `radar.js`**
2. **Find the `quadrants` array** (around line 19-24)
3. **Edit the names** while keeping the angles:

```javascript
this.quadrants = [
    { name: 'Your Custom Name 1', angle: 0 },
    { name: 'Your Custom Name 2', angle: 90 },
    { name: 'Your Custom Name 3', angle: 180 },
    { name: 'Your Custom Name 4', angle: 270 }
];
```

4. **Update the filter buttons** in `index.html` to match

### How to Customize Colors

**Option 1: Change Ring Colors**

Edit `radar.js` (around line 26-31):
```javascript
this.rings = [
    { name: 'Adopt', radius: 0.25, color: '#10b981' },  // Change these
    { name: 'Trial', radius: 0.5, color: '#06b6d4' },
    { name: 'Assess', radius: 0.75, color: '#f59e0b' },
    { name: 'Hold', radius: 1.0, color: '#ef4444' }
];
```

**Option 2: Change Theme Colors**

Edit `styles.css` (lines 1-20) CSS variables:
```css
:root {
    --accent-primary: #8b5cf6;  /* Purple */
    --accent-secondary: #06b6d4; /* Cyan */
    /* ... change any color variable */
}
```

### How to Use the Interactive Features

**Zoom & Pan:**
- Scroll your mouse wheel to zoom in/out
- Click and drag the background to pan
- Press `R` to reset the view

**Search:**
- Type in the search box to filter technologies
- Search works on both name and description

**Filter by Category:**
- Click any quadrant button to filter
- Click "All" to show everything

**View Details:**
- Click any technology blip (numbered circle)
- Details panel shows on the right

**Export:**
- Click the download icon (top right)
- Press `E` key
- Saves as `tech-radar.svg`

**Toggle Theme:**
- Click the sun/moon icon (top right)
- Press `T` key
- Preference is saved automatically

### How to Deploy Online

**GitHub Pages:**
1. Push your code to GitHub
2. Go to Settings → Pages
3. Select main branch
4. Your radar will be at `https://username.github.io/repo-name`

**Netlify:**
1. Drag the folder to [netlify.com/drop](https://netlify.com/drop)
2. Done! You get a URL instantly

**Vercel:**
```bash
npx vercel --prod
```

### How to Run Locally with Live Reload

Choose one method:

**Python:**
```bash
cd tech-radar
python -m http.server 8000
# Open http://localhost:8000
```

**Node.js:**
```bash
npx serve
# Open the URL shown
```

**VS Code:**
Install "Live Server" extension, right-click `index.html` → "Open with Live Server"

### How to Validate Your JSON

If the radar doesn't load after editing `data.json`:

1. **Use a JSON validator:** Copy your `data.json` content to [jsonlint.com](https://jsonlint.com)
2. **Check for common errors:**
   - Missing or extra commas
   - Unclosed quotes or brackets
   - Invalid property names

3. **Open browser console** (F12 → Console tab) to see error messages

## 🔧 Troubleshooting

### Radar not showing after changes
- Check browser console for errors (F12)
- Validate `data.json` format at jsonlint.com
- Hard refresh: `Ctrl+Shift+R` (Windows) or `Cmd+Shift+R` (Mac)

### Styles not loading
- Make sure all files are in the same folder
- Check that `styles.css` exists and is linked in `index.html`
- Clear browser cache

### Export not working
- Modern browsers may block downloads - check permissions
- Make sure you're not running from `file://` protocol (use a local server)

### Theme not persisting
- Check if browser allows localStorage
- Some browsers in private/incognito mode don't persist storage

### Technologies overlapping
- This is intentional for visual variety
- Zoom in for better view
- Technologies in the same ring/quadrant may overlap slightly

## 💡 Tips & Tricks

### For Teams
1. **Version control:** Use Git to track changes to `data.json`
2. **Regular reviews:** Schedule quarterly radar updates
3. **Collaborative editing:** Create a process for proposing changes
4. **Share widely:** Deploy to a URL everyone can access
5. **Document decisions:** Use meaningful descriptions

### For Presentations
1. **Export to SVG** for high-quality slides
2. **Use zoom** to focus on specific areas
3. **Toggle theme** based on presentation background
4. **Filter by quadrant** to discuss specific categories
5. **Print** directly from browser for handouts

### For Customization
1. **Start with data:** Add your technologies first
2. **Then customize colors** to match your brand
3. **Consider your audience** when naming quadrants
4. **Keep descriptions concise** but meaningful
5. **Use consistent** ring criteria across all entries

## Best Practices

### When to Add Technologies

- The technology is being actively used or considered
- There's a clear opinion about its place in your tech strategy
- It's relevant to your team's current or future work

### When to Update Ring Position

- **Moving to Adopt**: After successful trial usage in multiple projects
- **Moving to Trial**: When you want teams to start experimenting
- **Moving to Assess**: When a technology appears on your radar
- **Moving to Hold**: When you want to discourage further use

### Writing Good Descriptions

- Be specific about why it's in that ring
- Mention context: "for microservices" or "for frontend development"
- Keep it concise but informative (1-3 sentences)
- Focus on the "why" not just the "what"

## Running Locally

Simply open `index.html` in a web browser. No build step required.

For a better development experience with live reload:

```bash
# Using Python
python -m http.server 8000

# Using Node.js
npx serve

# Using PHP
php -S localhost:8000
```

Then open http://localhost:8000 in your browser.

## ✨ Premium Features

### 🎨 Visual Design
- **Modern Glassmorphism** - Frosted glass effects with backdrop blur
- **Gradient Aesthetics** - Beautiful color gradients throughout
- **Dark & Light Themes** - Fully functional theme switcher with localStorage persistence
- **Smooth Animations** - Carefully crafted transitions and micro-interactions
- **Pulse Effects** - Animated blips with pulsing rings for visual interest
- **Custom Scrollbars** - Styled scrollbars matching the theme

### 🖱️ Interactive Features
- **Zoom & Pan** - Mouse wheel to zoom (0.5x to 3x), drag to pan the radar
- **Interactive Tooltips** - Instant hover tooltips showing technology names
- **Click for Details** - Full technology information panel on click
- **Bidirectional Highlighting** - Synced highlighting between radar and list view
- **Real-time Search** - Live filtering as you type
- **Quadrant Filtering** - Filter by category with animated transitions

### ⌨️ Keyboard Shortcuts
- `Scroll` - Zoom in/out on the radar
- `Drag` - Pan the radar view
- `R` or `0` - Reset zoom to default
- `+` or `=` - Zoom in
- `-` or `_` - Zoom out
- `T` - Toggle between dark and light theme
- `E` - Export radar as SVG

### 📱 Responsive Design
- Fully responsive layout for all screen sizes
- Mobile-optimized touch interactions
- Tablet-friendly interface
- Print-ready styles for documentation

### ♿ Accessibility
- Full keyboard navigation support
- Clear focus indicators
- ARIA labels for screen readers
- High contrast ratios (WCAG AA compliant)
- Semantic HTML structure

### 💾 Export Functionality
- Export radar as high-quality SVG
- Vector graphics preserve all styling
- Ready for presentations and documentation

## 📁 File Structure

```
tech-radar/
├── index.html           # Main HTML structure
├── styles.css           # All styling and themes
├── radar.js             # Radar logic and interactions
├── data.json            # Technology data (manually edited OR generated)
├── README.md            # Complete documentation
├── start.sh             # Startup script for macOS/Linux
├── start.bat            # Startup script for Windows
│
└── data-etl/            # AI-powered ETL pipeline
    ├── src/
    │   ├── main.py                  # Entry point
    │   ├── scanner.py               # GitHub repository scanner
    │   ├── domain_detector.py       # AI-powered domain detection
    │   ├── temporal_analyzer.py     # Temporal pattern analysis
    │   ├── classifier_enhanced.py   # AI-assisted classification
    │   ├── output_generator.py      # JSON output generation
    │   ├── progress.py              # Checkpoint management
    │   └── rate_limiter.py          # GitHub API rate limiting
    │
    ├── config/
    │   └── config.yaml              # Configuration file
    │
    ├── requirements.txt             # Python dependencies
    ├── .scan_progress.json          # Checkpoint file (auto-generated)
    └── README.md                    # ETL documentation
```

## Customization

### Colors

Edit `styles.css` to change ring colors:

```css
.ring-color.adopt { background: #93c47d; }    /* Green */
.ring-color.trial { background: #6fa8dc; }    /* Blue */
.ring-color.assess { background: #ffd966; }   /* Yellow */
.ring-color.hold { background: #e06666; }     /* Red */
```

### Quadrant Names

Edit the `quadrants` array in `radar.js`:

```javascript
this.quadrants = [
    { name: 'Your Custom Name', angle: 0 },
    // ... etc
];
```

## Tips for Teams

1. **Regular Reviews**: Schedule quarterly reviews to update the radar
2. **Collaborative Editing**: Use version control (git) to track changes
3. **Document Decisions**: Update descriptions when moving technologies
4. **Share Widely**: Host the radar where everyone can access it
5. **Stay Current**: Don't let it get stale - a radar is only useful if maintained

## Example Workflow

1. New technology emerges → Add to "Assess" ring
2. Team experiments successfully → Move to "Trial"
3. Multiple projects adopt it → Move to "Adopt"
4. Better alternative found → Move old tech to "Hold"
5. No longer relevant → Remove from radar

## 🌍 Organization-Agnostic Design

This tool is designed to work with **any GitHub organization** without modification:

- **No hardcoded patterns**: Domain detection uses AI to analyze repository structure
- **No org-specific logic**: All organization names are in `config/config.yaml`
- **Fully configurable**: All thresholds, filters, and rules are in configuration
- **Universal domains**: Standard domains (mobile, backend, frontend, etc.) work for any organization
- **Extensible**: Easy to add custom domains or classification rules

**To use with your organization:**
1. Edit `data-etl/config/config.yaml`
2. Replace `your-org-name` with your GitHub organization
3. Set your API keys as environment variables
4. Run the scanner - it will adapt to your organization's structure automatically

The AI-powered domain detector analyzes:
- Repository directory structure
- File types and distribution
- README content and descriptions
- Technology stack and patterns
- Repository topics and metadata

No manual pattern configuration required!

## 🤝 Contributing

To suggest changes:
1. Edit `data.json` (manual) or run the ETL pipeline (automated)
2. Commit with a clear message explaining the change
3. Submit for review (if using version control)

## 📝 License

Open source - use and modify as needed for your organization.

---

**Built with:**
- Frontend: Vanilla JavaScript, CSS3, SVG
- ETL Pipeline: Python 3.8+, PyGithub, OpenAI API
- AI Models: GPT-4o-mini for classification and domain detection
- Design: Inspired by Thoughtworks Technology Radar
