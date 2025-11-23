# Domain-Based Tech Radar Analysis

## Overview

The tech radar now supports **AI-powered domain detection** that automatically classifies repositories into engineering domains (mobile, backend, frontend, infrastructure, etc.) and provides domain-specific technology classifications.

## Key Features

### 1. **Dynamic AI-Powered Domain Detection**

Instead of hardcoding repository naming patterns, the system uses AI to analyze:

- **Root directory structure** (e.g., `app/`, `src/main/java/`, `terraform/`)
- **File types and patterns** (e.g., `AndroidManifest.xml`, `Dockerfile`, `.tf` files)
- **README content** (first 500 chars for context)
- **Technology stack** (frameworks, languages, tools detected)
- **Repository topics** (GitHub topics/tags)

**Example:**
```
Repo: bazaar-zone-service
├── src/main/java/
├── pom.xml
├── Dockerfile
└── README: "Microservice for zone management..."

AI Analysis: → backend (confidence: 0.95)
```

### 2. **Domain-Segmented Classifications**

Technologies are now analyzed **per domain**, showing different adoption patterns:

```json
{
  "name": "Java",
  "ring": 2,  // Global classification
  "metadata": {
    "domain_breakdown": {
      "mobile": {
        "suggested_ring": 0,  // ADOPT (95% of mobile repos)
        "ring_name": "Adopt",
        "confidence": 0.95,
        "total_repos": 105,
        "trend": "STABLE"
      },
      "backend": {
        "suggested_ring": 2,  // ASSESS (25% of backend repos)
        "ring_name": "Assess",
        "confidence": 0.72,
        "total_repos": 36,
        "trend": "DECLINING"
      }
    }
  }
}
```

### 3. **Temporal Analysis by Domain**

The temporal analyzer now tracks adoption trends separately for each domain:

```json
{
  "temporal_data": {
    "by_domain": {
      "mobile": {
        "total_repos": 105,
        "recent_repos": 0,    // No new mobile repos in 6 months
        "activity_score": 0.85,
        "trend": "STABLE"
      },
      "backend": {
        "total_repos": 36,
        "recent_repos": 1,
        "activity_score": 0.50,
        "trend": "DECLINING"
      }
    }
  }
}
```

## Architecture

### Components

1. **`domain_detector.py`**
   - AI-powered domain classification
   - Analyzes repo structure and content
   - Returns domain with confidence score

2. **`scanner.py`** (Updated)
   - Integrates domain detection during scanning
   - Stores domain info with each repository

3. **`temporal_analyzer.py`** (Updated)
   - Analyzes metrics per domain
   - Tracks adoption trends by domain

4. **`classifier_enhanced.py`** (Updated)
   - Generates domain-specific classifications
   - Suggests different rings per domain

### Data Flow

```
GitHub Repo
    ↓
Scanner (with Domain Detector)
    ↓
Repo Details + Domain Info
    ↓
Temporal Analyzer (by domain)
    ↓
Classifier (domain breakdown)
    ↓
Tech Radar JSON (with domain data)
```

## Use Cases

### Use Case 1: Java Migration Strategy

**Question:** Should we migrate from Java to Kotlin?

**Answer from Domain Analysis:**
```
Java:
  Mobile:  ADOPT → HOLD (95% usage, 0 new repos → migrate to Kotlin)
  Backend: ASSESS (25% usage → keep for legacy services)

Kotlin:
  Mobile:  TRIAL → ADOPT (growing, 3 new repos)
  Backend: TRIAL (experimental, 5 repos)
```

**Insight:** Java is still ADOPT for mobile (high usage) but should move to HOLD (no new adoption). Backend can keep Java for legacy services.

### Use Case 2: Dockerfile Adoption

**Question:** Is Dockerfile widely adopted?

**Answer:**
```
Dockerfile:
  Backend:        ADOPT (80% usage)
  Infrastructure: ADOPT (95% usage)
  Frontend:       TRIAL (30% usage)
  Mobile:         N/A (not applicable)
```

**Insight:** Dockerfile is ADOPT for backend/infra, but frontend teams are still exploring it.

## Configuration

No hardcoded patterns needed! The AI adapts to your organization's repository structure.

### Optional: Custom Domain Patterns

You can optionally guide the AI with hints in `config.yaml`:

```yaml
domain_detection:
  enabled: true
  custom_hints:
    # Optional: Add domain-specific keywords for your org
    backend:
      - "service"
      - "api"
    mobile:
      - "app"
```

## Running with Domain Detection

Domain detection is **enabled by default** if OpenAI API key is provided:

```bash
# Run full scan with domain detection
python main.py

# Test on limited repos
python main.py --limit 50
```

## Output Format

The generated `data.ai.json` now includes:

```json
[
  {
    "name": "Java",
    "quadrant": 3,
    "ring": 2,
    "metadata": {
      "repos_count": 141,
      "usage_percentage": 48.0,
      "temporal_data": {
        "by_domain": {
          "mobile": {
            "total_repos": 105,
            "trend": "STABLE",
            "activity_score": 0.85
          },
          "backend": {
            "total_repos": 36,
            "trend": "DECLINING",
            "activity_score": 0.50
          }
        }
      },
      "domain_breakdown": {
        "mobile": {
          "suggested_ring": 0,
          "ring_name": "Adopt",
          "confidence": 0.95
        },
        "backend": {
          "suggested_ring": 2,
          "ring_name": "Assess",
          "confidence": 0.72
        }
      }
    }
  }
]
```

## Benefits

### ✅ **Opensource-Ready**
- No hardcoded organization-specific patterns
- Works with any GitHub organization
- AI adapts to different repo structures

### ✅ **Accurate Domain Detection**
- Analyzes actual repo content, not just naming
- High confidence classifications
- Handles edge cases (e.g., monorepos)

### ✅ **Strategic Insights**
- Reveals technology footprint per domain
- Identifies migration opportunities
- Shows where adoption is growing/declining

### ✅ **Context-Aware Classifications**
- Java might be ADOPT for mobile but HOLD for new backend services
- Dockerfile might be ADOPT for backend but TRIAL for frontend
- Same tech, different strategies per domain

## Example Insights

**From your data:**

1. **Java in Mobile:**
   - 95% usage (105/110 mobile repos)
   - Should be **ADOPT** (current reality)
   - But **HOLD** strategically (0 new repos, migrate to Kotlin)

2. **Kotlin Growth:**
   - 3 new mobile repos in 6 months
   - **TRIAL** → **ADOPT** trajectory
   - Validates migration strategy

3. **Dockerfile Backend:**
   - 80% of backend services use it
   - **ADOPT** status (containerization standard)
   - Not penalized by 43.9% global usage

## Next Steps

### Visualization

Update the tech radar UI to show:
- Toggle between global and domain-specific views
- Domain filters (show only mobile, backend, etc.)
- Migration paths (Java → Kotlin in mobile domain)

### Reporting

Generate domain-specific reports:
```bash
python main.py --domain-report mobile
```

### ADR Integration (Future)

Link strategic decisions to domain classifications:
```yaml
# ADR-001: Migrate mobile from Java to Kotlin
tech: Java
domain: mobile
current_ring: ADOPT
target_ring: HOLD
migration_to: Kotlin
deadline: 2025-Q4
```

## Troubleshooting

### Domain detection not working?

1. Check OpenAI API key is set
2. Verify repos have accessible README or root files
3. Check logs for AI errors

### Unexpected domain classifications?

The AI analyzes actual content. If a repo is classified wrong, it might be:
- Mixed-purpose repo (contains both mobile and backend)
- Poor README/documentation
- Non-standard structure

You can manually override in the output JSON if needed.

## Summary

**Before:** Technologies classified globally, missing context

**After:** Technologies classified per domain, revealing true adoption patterns

**Result:** Strategic, domain-aware technology decisions that match reality
