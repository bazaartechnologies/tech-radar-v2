# Technology Radar - Premium Interactive Visualization

A world-class interactive technology radar with stunning UI/UX, inspired by Thoughtworks. Built with modern web technologies for maximum visual appeal and usability.

## 🚀 Quick Start

**⚠️ Important:** Due to browser security (CORS), you need to run a local server. Opening `index.html` directly won't work.

### Easiest Method - Use the Startup Script

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

**To add a technology:** Edit `data.json` → Add new entry → Save → Refresh browser

## 📋 Quick Reference

| Action | File | What to Edit |
|--------|------|--------------|
| Add technology | `data.json` | Add new `{ name, quadrant, ring, description }` |
| Move ring | `data.json` | Change `ring` value (0=Adopt, 1=Trial, 2=Assess, 3=Hold) |
| Change category | `data.json` | Change `quadrant` value (0=Techniques, 1=Tools, 2=Platforms, 3=Languages) |
| Rename quadrant | `radar.js` | Edit `quadrants` array names |
| Change colors | `styles.css` or `radar.js` | Edit CSS variables or ring colors |
| Customize theme | `styles.css` | Edit `:root` variables |

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
├── index.html      # Main HTML structure
├── styles.css      # All styling and themes
├── radar.js        # Radar logic and interactions
├── data.json       # Technology data (EDIT THIS FILE)
├── README.md       # Complete documentation
├── start.sh        # Startup script for macOS/Linux
└── start.bat       # Startup script for Windows
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

## Contributing

To suggest changes:
1. Edit `data.json`
2. Commit with a clear message explaining the change
3. Submit for review (if using version control)

## License

Open source - use and modify as needed for your organization.
