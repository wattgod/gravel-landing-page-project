#!/usr/bin/env python3
"""
Survey Data Collection Script
Collects survey responses and saves them to GitHub
"""

import json
import os
from datetime import datetime
from pathlib import Path
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

def save_survey_response(data):
    """Save survey response to data directory"""
    data_dir = Path(__file__).parent.parent / "data" / "survey_responses"
    data_dir.mkdir(parents=True, exist_ok=True)
    
    # Create filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"survey_{timestamp}.json"
    filepath = data_dir / filename
    
    # Save response
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)
    
    return filepath

def create_github_issue_body(data):
    """Format survey data as GitHub Issue body"""
    return f"""## Training Plan Survey Response

**Race:** {data.get('race', 'Unknown')}
**Plan:** {data.get('plan', 'Unknown')}
**Week:** {data.get('week', 'Unknown')}
**Timestamp:** {data.get('timestamp', 'Unknown')}

### Responses

1. **Overall satisfaction:** {data.get('satisfaction', 'N/A')}/5
2. **Biggest challenge:** {data.get('challenge', 'N/A')}
3. **Confidence level:** {data.get('confidence', 'N/A')}/5
4. **Training hours/week:** {data.get('hours', 'N/A')}
5. **Following plan:** {data.get('following', 'N/A')}
6. **What's working well:** {data.get('working_well', 'N/A') or 'N/A'}
7. **Biggest concern:** {data.get('concern', 'N/A')}
8. **Plan difficulty:** {data.get('difficulty', 'N/A')}/5
9. **What to change:** {data.get('changes', 'N/A') or 'N/A'}
10. **Additional feedback:** {data.get('feedback', 'N/A') or 'N/A'}

---
*Submitted via training plan survey*"""

if __name__ == "__main__":
    # Example usage
    sample_data = {
        "timestamp": datetime.now().isoformat(),
        "race": "Mid South",
        "plan": "Ayahuasca Beginner",
        "week": "4",
        "satisfaction": "4",
        "challenge": "time",
        "confidence": "3",
        "hours": "3.5",
        "following": "mostly",
        "working_well": "The HIIT sessions are effective",
        "concern": "readiness",
        "difficulty": "3",
        "changes": "More recovery days",
        "feedback": "Great plan overall"
    }
    
    filepath = save_survey_response(sample_data)
    print(f"✅ Survey response saved to: {filepath}")
    print("\nGitHub Issue body:")
    print(create_github_issue_body(sample_data))
