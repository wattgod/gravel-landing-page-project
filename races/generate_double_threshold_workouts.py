#!/usr/bin/env python3
"""
Generate double threshold block workout files.

Creates ZWO files for:
- Session 1: Threshold Accumulation (12-15 × 3min @ 100% FTP)
- Session 2: Threshold Steady (3 × 10-12min @ 100% FTP)
- Alternative Session 2 options
"""

import xml.etree.ElementTree as ET
from pathlib import Path
from datetime import datetime

def create_threshold_accumulation_workout(week: int, output_dir: Path) -> str:
    """
    Create Threshold Accumulation workout.
    Week 1: 12×3min, Week 2: 13×3min, Week 3: 14×3min, Week 4: 15×3min
    """
    reps = 11 + week  # Week 1 = 12, Week 2 = 13, etc.
    
    # Warmup: 10min Z1/Z2 + 5min high cadence Z3
    warmup_xml = '''    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="300" Power="0.85" Cadence="100"/>'''
    
    # Main set: reps × 3min @ 100% FTP, 1min Z2 recovery
    main_set_xml = f'    <IntervalsT Repeat="{reps}" OnDuration="180" OnPower="1.00" OffDuration="60" OffPower="0.70"/>'
    
    # Cooldown
    cooldown_xml = '    <Cooldown Duration="600" PowerLow="0.50" PowerHigh="0.65"/>'
    
    # Description
    description = f"""WARM-UP:
• 10min building from Z1 to Z2 (RPE 3-4)
• 5min high cadence Z3 (100+ rpm) to prime efforts (RPE 5-6)

MAIN SET:
• {reps}×3min @ 93-105% FTP, RPE 7-8 (1min Z2 recovery, RPE 3-4)
• Cadence: 85-95rpm (race cadence for threshold work)
• Position: Seated, drops or hoods

COOL-DOWN:
• 10min easy spin Z1-Z2 (RPE 3-4)

PURPOSE:
Threshold accumulation. Many short threshold intervals with brief recovery build high-volume threshold work. This format accumulates more time at threshold than longer intervals allow, building race-pace endurance. Week {week} of 4-week block.

EXECUTION:
• Focus on maintaining consistent power across all intervals
• If power drops >5% in later intervals, reduce volume next session
• Recovery should feel easy—you're ready for the next interval"""
    
    # Create XML
    root = ET.Element("workout_file")
    ET.SubElement(root, "author").text = "Gravel God Training"
    ET.SubElement(root, "name").text = f"Week {week} - Threshold Accumulation ({reps}×3min)"
    ET.SubElement(root, "description").text = description
    ET.SubElement(root, "sportType").text = "bike"
    
    workout = ET.SubElement(root, "workout")
    workout.text = "\n"
    workout.tail = "\n"
    
    # Add blocks
    for line in warmup_xml.split('\n'):
        if line.strip():
            workout.text += line + "\n"
    workout.text += main_set_xml + "\n"
    workout.text += cooldown_xml + "\n"
    
    # Write file
    filename = f"Week_{week}_Threshold_Accumulation_{reps}x3min.zwo"
    filepath = output_dir / filename
    tree = ET.ElementTree(root)
    ET.indent(tree, space="  ")
    tree.write(filepath, encoding="utf-8", xml_declaration=True)
    
    return str(filepath)

def create_threshold_steady_workout(week: int, output_dir: Path) -> str:
    """
    Create Threshold Steady workout.
    Week 1: 3×10min, Week 2: 3×11min, Week 3: 3×12min, Week 4: 2×15min
    """
    if week == 4:
        reps = 2
        duration_min = 15
    else:
        reps = 3
        duration_min = 9 + week  # Week 1 = 10, Week 2 = 11, Week 3 = 12
    
    duration_sec = duration_min * 60
    
    # Warmup: 10min Z1/Z2 + 5min high cadence Z3
    warmup_xml = '''    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="300" Power="0.85" Cadence="100"/>'''
    
    # Main set: reps × duration @ 100% FTP, 5min Z2 recovery
    main_set_blocks = []
    for i in range(reps):
        main_set_blocks.append(f'    <SteadyState Duration="{duration_sec}" Power="1.00"/>')
        if i < reps - 1:
            main_set_blocks.append('    <SteadyState Duration="300" Power="0.70"/>')  # 5min Z2 recovery
    
    # Cooldown
    cooldown_xml = '    <Cooldown Duration="600" PowerLow="0.50" PowerHigh="0.65"/>'
    
    # Description
    if week == 4:
        desc_main = f"• 2×15min @ 93-105% FTP, RPE 7-8 (5min Z2 recovery, RPE 3-4)"
        purpose_note = "Week 4 consolidation: longer intervals to lock in adaptations."
    else:
        desc_main = f"• {reps}×{duration_min}min @ 93-105% FTP, RPE 7-8 (5min Z2 recovery, RPE 3-4)"
        purpose_note = f"Week {week} of 4-week block."
    
    description = f"""WARM-UP:
• 10min building from Z1 to Z2 (RPE 3-4)
• 5min high cadence Z3 (100+ rpm) to prime efforts (RPE 5-6)

MAIN SET:
{desc_main}
• Cadence: 85-95rpm (race cadence for threshold work)
• Position: Seated, drops or hoods

COOL-DOWN:
• 10min easy spin Z1-Z2 (RPE 3-4)

PURPOSE:
Sustained threshold efforts to build race-pace endurance. These longer intervals teach your body to maintain threshold power when fatigued—exactly what you'll need in a gravel race. {purpose_note}

EXECUTION:
• Start conservatively—you should finish the last interval as strong as the first
• If you can't complete all intervals, reduce duration next session
• Focus on smooth, controlled power—no surges"""
    
    # Create XML
    root = ET.Element("workout_file")
    ET.SubElement(root, "author").text = "Gravel God Training"
    ET.SubElement(root, "name").text = f"Week {week} - Threshold Steady ({reps}×{duration_min}min)"
    ET.SubElement(root, "description").text = description
    ET.SubElement(root, "sportType").text = "bike"
    
    workout = ET.SubElement(root, "workout")
    workout.text = "\n"
    workout.tail = "\n"
    
    # Add blocks
    for line in warmup_xml.split('\n'):
        if line.strip():
            workout.text += line + "\n"
    for block in main_set_blocks:
        workout.text += block + "\n"
    workout.text += cooldown_xml + "\n"
    
    # Write file
    filename = f"Week_{week}_Threshold_Steady_{reps}x{duration_min}min.zwo"
    filepath = output_dir / filename
    tree = ET.ElementTree(root)
    ET.indent(tree, space="  ")
    tree.write(filepath, encoding="utf-8", xml_declaration=True)
    
    return str(filepath)

def create_threshold_progressive_workout(week: int, output_dir: Path) -> str:
    """
    Create Threshold Progressive workout (alternative Session 2).
    2 × (10min @ 95% FTP → 10min @ 100% FTP), 5min recovery
    """
    # Warmup: 10min Z1/Z2 + 5min high cadence Z3
    warmup_xml = '''    <Warmup Duration="600" PowerLow="0.50" PowerHigh="0.65"/>
    <SteadyState Duration="300" Power="0.85" Cadence="100"/>'''
    
    # Main set: 2 sets of progressive threshold
    main_set_blocks = []
    for i in range(2):
        main_set_blocks.append('    <SteadyState Duration="600" Power="0.95"/>')  # 10min @ 95%
        main_set_blocks.append('    <SteadyState Duration="600" Power="1.00"/>')  # 10min @ 100%
        if i < 1:
            main_set_blocks.append('    <SteadyState Duration="300" Power="0.70"/>')  # 5min Z2 recovery
    
    # Cooldown
    cooldown_xml = '    <Cooldown Duration="600" PowerLow="0.50" PowerHigh="0.65"/>'
    
    # Description
    description = f"""WARM-UP:
• 10min building from Z1 to Z2 (RPE 3-4)
• 5min high cadence Z3 (100+ rpm) to prime efforts (RPE 5-6)

MAIN SET:
• 2 sets of: (10min @ 88-92% FTP, RPE 6-7 → 10min @ 93-105% FTP, RPE 7-8)
• 5min Z2 recovery between sets (RPE 3-4)
• Cadence: 85-95rpm (race cadence for threshold work)
• Position: Seated, drops or hoods

COOL-DOWN:
• 10min easy spin Z1-Z2 (RPE 3-4)

PURPOSE:
Threshold progressive. Building into threshold teaches pacing and allows you to accumulate more time at threshold than starting at 100%. The progressive nature also simulates race scenarios where you build effort over a climb or section.

EXECUTION:
• Start at 95% FTP—this should feel manageable
• Transition smoothly to 100% FTP—no sudden jump
• Focus on maintaining power through the transition"""
    
    # Create XML
    root = ET.Element("workout_file")
    ET.SubElement(root, "author").text = "Gravel God Training"
    ET.SubElement(root, "name").text = f"Week {week} - Threshold Progressive (2×20min)"
    ET.SubElement(root, "description").text = description
    ET.SubElement(root, "sportType").text = "bike"
    
    workout = ET.SubElement(root, "workout")
    workout.text = "\n"
    workout.tail = "\n"
    
    # Add blocks
    for line in warmup_xml.split('\n'):
        if line.strip():
            workout.text += line + "\n"
    for block in main_set_blocks:
        workout.text += block + "\n"
    workout.text += cooldown_xml + "\n"
    
    # Write file
    filename = f"Week_{week}_Threshold_Progressive_2x20min.zwo"
    filepath = output_dir / filename
    tree = ET.ElementTree(root)
    ET.indent(tree, space="  ")
    tree.write(filepath, encoding="utf-8", xml_declaration=True)
    
    return str(filepath)

def main():
    """Generate all double threshold block workouts."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = Path.home() / "Downloads" / f"double_threshold_block_{timestamp}"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print("=" * 80)
    print("DOUBLE THRESHOLD BLOCK WORKOUT GENERATOR")
    print("=" * 80)
    print(f"\n📁 Output directory: {output_dir}")
    print("\n🔨 Generating workouts...\n")
    
    files_created = []
    
    # Generate Session 1: Threshold Accumulation (all 4 weeks)
    print("Session 1: Threshold Accumulation")
    for week in range(1, 5):
        filepath = create_threshold_accumulation_workout(week, output_dir)
        files_created.append(filepath)
        print(f"  ✓ Week {week}: {Path(filepath).name}")
    
    # Generate Session 2: Threshold Steady (all 4 weeks)
    print("\nSession 2: Threshold Steady")
    for week in range(1, 5):
        filepath = create_threshold_steady_workout(week, output_dir)
        files_created.append(filepath)
        print(f"  ✓ Week {week}: {Path(filepath).name}")
    
    # Generate Alternative Session 2: Threshold Progressive (all 4 weeks)
    print("\nAlternative Session 2: Threshold Progressive")
    for week in range(1, 5):
        filepath = create_threshold_progressive_workout(week, output_dir)
        files_created.append(filepath)
        print(f"  ✓ Week {week}: {Path(filepath).name}")
    
    print(f"\n✅ Generated {len(files_created)} workout files")
    print(f"   Location: {output_dir}")
    print("\n" + "=" * 80)
    print("DOUBLE THRESHOLD BLOCK STRUCTURE:")
    print("=" * 80)
    print("""
Week Structure:
- Monday: Rest or Easy Z1/Z2 (30-60min)
- Tuesday: Threshold Accumulation (Session 1)
- Wednesday: Easy Z1/Z2 (60-90min) or Rest
- Thursday: Threshold Steady OR Threshold Progressive (Session 2)
- Friday: Rest or Easy Z1/Z2 (30-60min)
- Saturday: Long Z2 endurance (2-4 hours)
- Sunday: Easy Z1/Z2 (60-90min) or Rest

Block Duration: 3-4 weeks
Recovery: 48 hours minimum between threshold sessions
""")

if __name__ == "__main__":
    main()

