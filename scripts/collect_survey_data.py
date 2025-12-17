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
    return f"""## Training Plan Survey Response - Post-Completion

**Training Plan:** {data.get('race', 'Unknown')} - {data.get('plan', 'Unknown')}
**Timestamp:** {data.get('timestamp', 'Unknown')}

### Responses

1. **Race completion:** {data.get('completed', 'N/A')}
2. **Plan effectiveness:** {data.get('effectiveness', 'N/A')}/5
3. **Plan adherence:** {data.get('adherence', 'N/A')}
4. **Average training hours/week:** {data.get('hours', 'N/A')}
5. **What worked best:** {data.get('worked_best', 'N/A') or 'N/A'}
6. **What didn't work:** {data.get('didnt_work', 'N/A') or 'N/A'}
7. **Race performance vs expectations:** {data.get('performance', 'N/A') or 'N/A'}
8. **Plan difficulty:** {data.get('difficulty', 'N/A')}/5
9. **Would recommend:** {data.get('recommend', 'N/A')}
10. **Specific improvements needed:** {data.get('improvements', 'N/A') or 'N/A'}
11. **Additional feedback:** {data.get('feedback', 'N/A') or 'N/A'}

---
*Submitted via post-completion training plan survey*"""

if __name__ == "__main__":
    # Example usage
    sample_data = {
        "timestamp": datetime.now().isoformat(),
        "race": "Mid South",
        "plan": "Ayahuasca Beginner",
        "completed": "yes",
        "effectiveness": "4",
        "adherence": "mostly",
        "hours": "3.5",
        "worked_best": "intensity, structure",
        "didnt_work": "volume",
        "performance": "met",
        "difficulty": "3",
        "recommend": "yes",
        "improvements": "Add one more recovery day per week in weeks 6-8",
        "feedback": "Great plan overall, felt well prepared for race day"
    }
    
    filepath = save_survey_response(sample_data)
    print(f"✅ Survey response saved to: {filepath}")
    print("\nGitHub Issue body:")
    print(create_github_issue_body(sample_data))
