#!/usr/bin/env python3
"""
Unified Plan Generator
Generates coordinated cycling + strength training plans.
"""

import json
import sys
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional

# Add config and generation_modules to path
sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent / "generation_modules"))

from config.phase_alignment import (
    CYCLING_PHASES, 
    PHASE_ALIGNMENT, 
    get_strength_phase,
    get_strength_frequency
)
from config.tier_config import TIERS, get_tier, get_strength_sessions
from config.race_strength_profiles import get_race_profile, get_emphasized_exercises
from config.weekly_structure import get_weekly_template, get_strength_days

# Import existing generators
from generation_modules.strength_generator import (
    load_strength_templates,
    create_strength_zwo_file,
    get_pathway_name,
    get_session_letter
)
from generation_modules.zwo_generator import generate_all_zwo_files


class UnifiedPlanGenerator:
    """Generates unified cycling + strength training plans."""
    
    def __init__(
        self, 
        race_id: str, 
        tier_id: str, 
        plan_weeks: int, 
        race_date: str, 
        race_data: dict = None,
        weekly_structure_override: dict = None,
        exercise_exclusions: list = None,
        equipment_available: list = None
    ):
        self.race_id = race_id
        self.tier_id = tier_id
        self.plan_weeks = plan_weeks
        self.race_date = datetime.strptime(race_date, "%Y-%m-%d")
        
        # Load configurations
        self.tier = get_tier(tier_id)
        self.race_profile = get_race_profile(race_id)
        self.race_data = race_data or {}
        
        # Athlete-specific overrides
        self.weekly_structure_override = weekly_structure_override
        self.exercise_exclusions = exercise_exclusions or []
        self.equipment_available = equipment_available or []
        
        # Calculate plan start date
        self.start_date = self.race_date - timedelta(weeks=plan_weeks)
        
        # Build phase schedule
        self.phase_schedule = self._build_phase_schedule()
        
    def _build_phase_schedule(self) -> List[Dict]:
        """Build week-by-week phase schedule."""
        schedule = []
        
        # Phase distribution based on plan length
        if self.plan_weeks <= 8:
            phases = [
                ("base_1", 2),
                ("build_1", 3),
                ("peak", 2),
                ("taper", 1)
            ]
        elif self.plan_weeks <= 12:
            phases = [
                ("base_1", 2),
                ("base_2", 2),
                ("build_1", 3),
                ("build_2", 2),
                ("peak", 2),
                ("taper", 1)
            ]
        elif self.plan_weeks <= 16:
            phases = [
                ("base_1", 3),
                ("base_2", 3),
                ("build_1", 4),
                ("build_2", 3),
                ("peak", 2),
                ("taper", 1)
            ]
        else:  # 20+ weeks
            phases = [
                ("base_1", 4),
                ("base_2", 4),
                ("build_1", 5),
                ("build_2", 4),
                ("peak", 2),
                ("taper", 1)
            ]
        
        week = 1
        for phase_name, duration in phases:
            for i in range(duration):
                if week > self.plan_weeks:
                    break
                    
                strength_phase = get_strength_phase(phase_name)
                strength_freq = get_strength_frequency(self.tier_id, phase_name)
                
                # Use custom weekly structure if provided, otherwise use template
                if self.weekly_structure_override:
                    weekly_template = self.weekly_structure_override
                    # Extract strength days from custom structure
                    strength_days = [
                        day for day, schedule in weekly_template.get("days", {}).items()
                        if schedule.get("am") == "strength" or schedule.get("pm") == "strength"
                    ]
                else:
                    weekly_template = get_weekly_template(self.tier_id, phase_name)
                    strength_days = get_strength_days(self.tier_id, phase_name, strength_freq)
                
                schedule.append({
                    "week": week,
                    "cycling_phase": phase_name,
                    "strength_phase": strength_phase,
                    "strength_sessions": strength_freq,
                    "strength_days": strength_days,
                    "weekly_template": weekly_template,
                    "week_start_date": self.start_date + timedelta(weeks=week-1)
                })
                week += 1
        
        return schedule
    
    def generate_plan(self, output_dir: str, plan_template: dict = None) -> Dict:
        """Generate complete unified training plan."""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Create subdirectories
        workouts_dir = output_path / "workouts"
        workouts_dir.mkdir(exist_ok=True)
        (output_path / "calendar").mkdir(exist_ok=True)
        
        generated = {
            "cycling_workouts": [],
            "strength_workouts": [],
            "calendar": []
        }
        
        # Generate cycling workouts if plan template provided
        if plan_template:
            cycling_count = generate_all_zwo_files(
                plan_template,
                self.race_data,
                {"tier": self.tier_id, "weeks": self.plan_weeks},
                output_path
            )
            generated["cycling_workouts"] = list(workouts_dir.glob("*.zwo"))
        
        # Load strength templates (relative to this file)
        generation_modules_dir = Path(__file__).parent / "generation_modules"
        templates_file = generation_modules_dir / "MASTER_TEMPLATES_V2_PN_FINAL.md"
        if not templates_file.exists():
            templates_file = generation_modules_dir / "MASTER_TEMPLATES_V2.md"
        
        strength_templates = load_strength_templates(str(templates_file))
        
        # Map strength phase names to template keys
        phase_to_template_map = {
            "Learn to Lift": {
                "A": ["RED_A_PHASE1", "RED_A_PHASE2", "RED_A_PHASE3"],
                "B": ["RED_B_PHASE1", "RED_B_PHASE2", "RED_B_PHASE3"]
            },
            "Lift Heavy Sh*t": {
                "A": ["YELLOW_A_HYPER", "YELLOW_A_MAX"],
                "B": ["YELLOW_B_HYPER", "YELLOW_B_MAX"]
            },
            "Lift Fast": {
                "A": ["GREEN_A_POWER", "GREEN_A_CONV"],
                "B": ["GREEN_B_POWER", "GREEN_B_CONV"]
            },
            "Don't Lose It": {
                "A": ["GREEN_A_MAINT"],
                "B": ["GREEN_B_MAINT"]
            }
        }
        
        for week_info in self.phase_schedule:
            week = week_info["week"]
            
            # Generate strength workouts for the week
            strength_workouts = self._generate_strength_week(
                week_info, 
                strength_templates,
                phase_to_template_map,
                workouts_dir
            )
            generated["strength_workouts"].extend(strength_workouts)
            
            # Build calendar entry
            calendar_entry = self._build_calendar_week(week_info, strength_workouts)
            generated["calendar"].append(calendar_entry)
        
        # Generate unified calendar
        self._generate_calendar_file(generated["calendar"], output_path / "calendar")
        
        # Generate plan summary
        summary = self._generate_plan_summary(generated, output_path)
        
        return {
            "summary": summary,
            "files_generated": {
                "cycling": len(generated["cycling_workouts"]),
                "strength": len(generated["strength_workouts"]),
                "calendar": 1
            },
            "output_dir": str(output_path)
        }
    
    def _generate_strength_week(
        self, 
        week_info: Dict, 
        strength_templates: dict,
        phase_to_template_map: dict,
        output_dir: Path
    ) -> List[str]:
        """Generate strength workouts for a week."""
        week = week_info["week"]
        phase = week_info["strength_phase"]
        sessions = week_info["strength_sessions"]
        days = week_info["strength_days"]
        
        generated_files = []
        
        # Get template keys for this phase
        phase_templates = phase_to_template_map.get(phase, {})
        session_labels = ["A", "B", "C"][:sessions]
        
        # Select template keys based on week progression within phase
        # Simple rotation: alternate between available templates
        for i, (day, label) in enumerate(zip(days, session_labels)):
            template_keys = phase_templates.get(label, [])
            if not template_keys:
                continue
            
            # Select template based on week (rotate through available templates)
            template_idx = (week - 1) % len(template_keys)
            template_key = template_keys[template_idx]
            
            if template_key not in strength_templates:
                print(f"  ⚠️  Template {template_key} not found, skipping")
                continue
            
            description = strength_templates[template_key]
            
            # Generate filename
            pathway_name = get_pathway_name(template_key)
            session_letter = get_session_letter(template_key)
            filename = f"W{week:02d}_STR_{pathway_name.replace(' ', '_')}_{session_letter}.zwo"
            output_path = output_dir / filename
            
            # Apply exercise exclusions if provided
            if self.exercise_exclusions:
                description = self._apply_exercise_exclusions(description, self.exercise_exclusions)
            
            # Create ZWO file
            create_strength_zwo_file(
                week=week,
                template_key=template_key,
                description=description,
                output_path=output_path,
                plan_weeks=self.plan_weeks
            )
            
            generated_files.append(str(output_path))
        
        return generated_files
    
    def _build_calendar_week(self, week_info: Dict, strength_workouts: List) -> Dict:
        """Build calendar representation of a training week."""
        template = week_info["weekly_template"]
        week_start = week_info["week_start_date"]
        
        calendar = {
            "week": week_info["week"],
            "cycling_phase": week_info["cycling_phase"],
            "strength_phase": week_info["strength_phase"],
            "strength_sessions": week_info["strength_sessions"],
            "start_date": week_start.strftime("%Y-%m-%d"),
            "days": {}
        }
        
        day_names = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
        
        # Map strength workouts to days
        strength_by_day = {}
        for workout_path in strength_workouts:
            filename = Path(workout_path).name
            # Extract day from filename or use position in list
            # For now, use order: first workout = first strength day, etc.
            pass
        
        for i, day in enumerate(day_names):
            date = week_start + timedelta(days=i)
            day_template = template["days"][day]
            
            # Check if this day has a strength workout
            strength_file = None
            if day_template.get("am") == "strength" or day_template.get("pm") == "strength":
                # Find matching strength workout
                day_idx = week_info["strength_days"].index(day) if day in week_info["strength_days"] else None
                if day_idx is not None and day_idx < len(strength_workouts):
                    strength_file = Path(strength_workouts[day_idx]).name
            
            calendar["days"][day] = {
                "date": date.strftime("%Y-%m-%d"),
                "am": day_template.get("am"),
                "pm": day_template.get("pm"),
                "is_key_day": day_template.get("is_key_day", False),
                "notes": day_template.get("notes", ""),
                "strength_file": strength_file
            }
        
        return calendar
    
    def _apply_exercise_exclusions(self, description: str, exclusions: list) -> str:
        """
        Remove or replace excluded exercises from workout description.
        
        Args:
            description: Workout description text
            exclusions: List of exercise names to exclude
        
        Returns:
            Modified description with excluded exercises removed/replaced
        """
        import re
        
        # Normalize exclusion names for matching (case-insensitive, handle variations)
        exclusion_patterns = []
        for exclusion in exclusions:
            # Create pattern that matches exercise name (handles variations)
            pattern = re.escape(exclusion)
            # Match exercise name at start of line or after bullet/number
            exclusion_patterns.append(
                re.compile(
                    rf'(?i)(?:^|\n)\s*[A-Z]?\d*\s*{pattern}[^→\n]*→[^\n]*',
                    re.MULTILINE
                )
            )
        
        # Remove excluded exercises
        modified_description = description
        for pattern in exclusion_patterns:
            modified_description = pattern.sub('', modified_description)
        
        # Clean up extra blank lines
        modified_description = re.sub(r'\n{3,}', '\n\n', modified_description)
        
        # Add note about exclusions if any were removed
        if modified_description != description:
            exclusion_note = f"\n\n⚠️  Note: Some exercises have been excluded based on your injury history/limitations.\n"
            # Find a good place to insert the note (after header, before first section)
            header_end = modified_description.find('\n\n★')
            if header_end > 0:
                modified_description = (
                    modified_description[:header_end] + 
                    exclusion_note + 
                    modified_description[header_end:]
                )
        
        return modified_description
    
    def _generate_calendar_file(self, calendar: List[Dict], output_dir: Path):
        """Generate calendar file (JSON and markdown)."""
        # JSON calendar
        with open(output_dir / "training_calendar.json", "w") as f:
            json.dump(calendar, f, indent=2)
        
        # Markdown calendar
        md_content = self._render_calendar_markdown(calendar)
        with open(output_dir / "training_calendar.md", "w") as f:
            f.write(md_content)
    
    def _render_calendar_markdown(self, calendar: List[Dict]) -> str:
        """Render calendar as markdown."""
        lines = [
            f"# Training Calendar: {self.race_profile['name']}",
            f"**Tier:** {self.tier['name']}",
            f"**Duration:** {self.plan_weeks} weeks",
            f"**Race Date:** {self.race_date.strftime('%B %d, %Y')}",
            "",
            "---",
            ""
        ]
        
        for week in calendar:
            lines.append(f"## Week {week['week']}: {week['cycling_phase'].replace('_', ' ').title()}")
            lines.append(f"*Strength: {week['strength_phase']} ({week['strength_sessions']}x/week)*")
            lines.append("")
            lines.append("| Day | Date | AM | PM | Strength | Notes |")
            lines.append("|-----|------|----|----|----------|-------|")
            
            for day, info in week["days"].items():
                am = info["am"] or "—"
                pm = info["pm"] or "—"
                strength = info.get("strength_file", "—")
                key = "🔑" if info["is_key_day"] else ""
                lines.append(f"| {day.title()} {key} | {info['date']} | {am} | {pm} | {strength} | {info['notes']} |")
            
            lines.append("")
        
        return "\n".join(lines)
    
    def _generate_plan_summary(self, generated: Dict, output_dir: Path) -> Dict:
        """Generate plan summary document."""
        summary = {
            "race": self.race_profile["name"],
            "tier": self.tier["name"],
            "plan_weeks": self.plan_weeks,
            "race_date": self.race_date.strftime("%Y-%m-%d"),
            "start_date": self.start_date.strftime("%Y-%m-%d"),
            "phase_breakdown": {},
            "workout_counts": {
                "cycling": len(generated["cycling_workouts"]),
                "strength": len(generated["strength_workouts"])
            },
            "strength_customization": {
                "emphasized_exercises": self.race_profile.get("emphasized_exercises", []),
                "notes": self.race_profile.get("notes", "")
            }
        }
        
        # Count weeks per phase
        for week_info in self.phase_schedule:
            phase = week_info["cycling_phase"]
            summary["phase_breakdown"][phase] = summary["phase_breakdown"].get(phase, 0) + 1
        
        # Write summary
        with open(output_dir / "plan_summary.json", "w") as f:
            json.dump(summary, f, indent=2)
        
        return summary


def generate_unified_plan(
    race_id: str,
    tier_id: str,
    plan_weeks: int,
    race_date: str,
    output_dir: str,
    race_data: dict = None,
    plan_template: dict = None,
    weekly_structure_override: dict = None,
    exercise_exclusions: list = None,
    equipment_available: list = None
) -> Dict:
    """
    Main entry point for unified plan generation.
    
    Args:
        race_id: Race identifier (e.g., "unbound_gravel_200")
        tier_id: Tier identifier (e.g., "compete")
        plan_weeks: Number of weeks in plan
        race_date: Race date as "YYYY-MM-DD"
        output_dir: Output directory path
        race_data: Optional race data dict
        plan_template: Optional cycling plan template
        weekly_structure_override: Optional custom weekly structure (from athlete preferences)
        exercise_exclusions: Optional list of exercises to exclude (from injuries/limitations)
        equipment_available: Optional list of available equipment
    
    Returns:
        Generation summary dict
    """
    generator = UnifiedPlanGenerator(
        race_id=race_id,
        tier_id=tier_id,
        plan_weeks=plan_weeks,
        race_date=race_date,
        race_data=race_data,
        weekly_structure_override=weekly_structure_override,
        exercise_exclusions=exercise_exclusions,
        equipment_available=equipment_available
    )
    return generator.generate_plan(output_dir, plan_template)


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate unified training plan")
    parser.add_argument("--race", required=True, help="Race ID (e.g., unbound_gravel_200)")
    parser.add_argument("--tier", required=True, help="Tier ID (e.g., compete)")
    parser.add_argument("--weeks", type=int, required=True, help="Plan duration in weeks")
    parser.add_argument("--race-date", required=True, help="Race date (YYYY-MM-DD)")
    parser.add_argument("--output", required=True, help="Output directory")
    
    args = parser.parse_args()
    
    result = generate_unified_plan(
        race_id=args.race,
        tier_id=args.tier,
        plan_weeks=args.weeks,
        race_date=args.race_date,
        output_dir=args.output
    )
    
    print(f"Generated {result['files_generated']['cycling']} cycling workouts")
    print(f"Generated {result['files_generated']['strength']} strength workouts")
    print(f"Output: {result['output_dir']}")

