#!/usr/bin/env python3
"""
COMPETE SAVE MY RACE - 6 WEEK EMERGENCY PLAN
Working ZWO Generation Script - ALL 42 FILES + 3 BLOCK OPTIONS

Compressed block periodization for race-fit athletes needing final sharpening
Imports all workout data from ALL_WORKOUTS_DATA_SAVEMYRACE.py
"""
import sys
import os

# Import all workout data
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:
    from ALL_WORKOUTS_DATA_SAVEMYRACE import (
        week_1, week_2_vo2max, week_2_threshold, week_2_durability,
        week_3_vo2max, week_3_threshold, week_3_durability,
        week_4, week_5, week_6
    )
except ImportError as e:
    print(f"ERROR: Could not import workout data: {e}")
    print("Make sure ALL_WORKOUTS_DATA_SAVEMYRACE.py is in the same directory.")
    exit(1)

def create_workout(template_path, name, description, workout_blocks, output_path):
    """
    Create TrainingPeaks-compatible ZWO file
    
    Args:
        template_path: Path to your working template (W01_Tue_-_FTP_Test.zwo)
        name: Workout name (e.g., "W01 Mon - Rest")
        description: Full description with • headers
        workout_blocks: XML workout structure with 4-space indent
        output_path: Where to save the new file
    """
    import html
    
    # Load template in binary mode
    with open(template_path, 'rb') as f:
        content = f.read()
    
    # Escape XML special characters in name and description
    # XML requires: < -> &lt;, > -> &gt;, & -> &amp;
    name_escaped = html.escape(name, quote=False)
    description_escaped = html.escape(description, quote=False)
    
    # Replace NAME tag - template uses <name>W01 Tue - FTP Test</name>
    old_name = b'<name>W01 Tue - FTP Test</name>'
    new_name = f'<name>{name_escaped}</name>'.encode('utf-8')
    content = content.replace(old_name, new_name)
    
    # Replace description
    desc_start = content.find(b'<description>')
    desc_end = content.find(b'</description>')
    if desc_start != -1 and desc_end != -1:
        desc_end += len(b'</description>')
        old_desc = content[desc_start:desc_end]
        new_desc = f'<description>{description_escaped}</description>'.encode('utf-8')
        content = content.replace(old_desc, new_desc)
    
    # Replace workout section
    # Template structure: 6 spaces before <workout>, 4 spaces for content, 2 spaces before </workout>
    workout_start = content.find(b'<workout>')
    workout_end = content.find(b'</workout>')
    if workout_start != -1 and workout_end != -1:
        # Find newline before workout tag to include in replacement
        newline_pos = content.rfind(b'\n', max(0, workout_start - 20), workout_start)
        if newline_pos == -1:
            newline_pos = workout_start - 10  # Fallback
        
        workout_end += len(b'</workout>')
        # Replace from newline (to include proper indentation) to end tag
        old_workout = content[newline_pos + 1:workout_end]  # +1 to skip the newline itself
        # Use exact template indentation: 6 spaces for opening tag, 2 for closing
        new_workout = f'      <workout>\n{workout_blocks}  </workout>'.encode('utf-8')
        content = content[:newline_pos + 1] + new_workout + content[workout_end:]
    
    # Write in binary mode
    with open(output_path, 'wb') as f:
        f.write(content)
    
    print(f"✓ Created: {name}")
    return True


# ============================================================================
# WORKOUT DATA IMPORTED FROM ALL_WORKOUTS_DATA_SAVEMYRACE.py
# ============================================================================
# All workout definitions are now imported at the top of the file


# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    # Configuration - UPDATE THESE PATHS FOR YOUR SYSTEM
    script_dir = os.path.dirname(os.path.abspath(__file__))
    template_path = os.path.join(script_dir, 'W01_Tue_-_FTP_Test.zwo')  # Update this path
    output_dir = os.path.join(script_dir, 'generated_workouts_savemyrace')
    
    # Verify template exists
    if not os.path.exists(template_path):
        print(f"ERROR: Template not found at {template_path}")
        print("\nPlease update template_path in the script to point to your working template file.")
        print("The template should be a ZWO file with the structure:")
        print("  <name>W01 Tue - FTP Test</name>")
        print("  <description>...</description>")
        print("  <workout>...</workout>")
        exit(1)
    
    # Create output directory if needed
    os.makedirs(output_dir, exist_ok=True)
    
    print("=" * 60)
    print("COMPETE SAVE MY RACE - 6 WEEK EMERGENCY PLAN")
    print("Generating ALL workout files...")
    print("=" * 60)
    print("\nNOTE: Weeks 2-3 have 3 block options (VO2max, Threshold, Durability)")
    print("All three options will be generated. Choose the one matching your limiter.")
    print("=" * 60)
    
    total_workouts = 0
    
    # Week 1: Rapid Assessment (7 workouts)
    print("\n🔧 WEEK 1: Rapid Assessment & Block Planning")
    for workout in week_1:
        output_path = os.path.join(output_dir, f"{workout['name'].replace(' ', '_').replace('/', '_').replace('#', '')}.zwo")
        create_workout(
            template_path=template_path,
            name=workout['name'],
            description=workout['description'],
            workout_blocks=workout['blocks'],
            output_path=output_path
        )
        total_workouts += 1
    print(f"✓ Week 1 complete: {len(week_1)} files generated")
    
    # Week 2: OPTION A - VO2max Block (7 workouts)
    print("\n🔧 WEEK 2: OPTION A - VO2max Block")
    for workout in week_2_vo2max:
        base_name = workout['name'].replace(' ', '_').replace('/', '_').replace('#', '')
        if '_VO2MAX' not in base_name:
            base_name += '_VO2max'
        output_path = os.path.join(output_dir, f"{base_name}.zwo")
        create_workout(
            template_path=template_path,
            name=workout['name'],
            description=workout['description'],
            workout_blocks=workout['blocks'],
            output_path=output_path
        )
        total_workouts += 1
    print(f"✓ Week 2 VO2max complete: {len(week_2_vo2max)} files generated")
    
    # Week 2: OPTION B - Threshold Block (7 workouts)
    print("\n🔧 WEEK 2: OPTION B - Threshold Block")
    for workout in week_2_threshold:
        base_name = workout['name'].replace(' ', '_').replace('/', '_').replace('#', '')
        if '_THRESHOLD' not in base_name:
            base_name += '_Threshold'
        output_path = os.path.join(output_dir, f"{base_name}.zwo")
        create_workout(
            template_path=template_path,
            name=workout['name'],
            description=workout['description'],
            workout_blocks=workout['blocks'],
            output_path=output_path
        )
        total_workouts += 1
    print(f"✓ Week 2 Threshold complete: {len(week_2_threshold)} files generated")
    
    # Week 2: OPTION C - Durability Block (7 workouts)
    print("\n🔧 WEEK 2: OPTION C - Durability Block")
    for workout in week_2_durability:
        base_name = workout['name'].replace(' ', '_').replace('/', '_').replace('#', '')
        if '_DURABILITY' not in base_name:
            base_name += '_Durability'
        output_path = os.path.join(output_dir, f"{base_name}.zwo")
        create_workout(
            template_path=template_path,
            name=workout['name'],
            description=workout['description'],
            workout_blocks=workout['blocks'],
            output_path=output_path
        )
        total_workouts += 1
    print(f"✓ Week 2 Durability complete: {len(week_2_durability)} files generated")
    
    # Week 3: OPTION A - VO2max Block Peak (7 workouts)
    print("\n🔧 WEEK 3: OPTION A - VO2max Block Peak Loading")
    for workout in week_3_vo2max:
        base_name = workout['name'].replace(' ', '_').replace('/', '_').replace('#', '')
        if '_VO2MAX' not in base_name:
            base_name += '_VO2max'
        output_path = os.path.join(output_dir, f"{base_name}.zwo")
        create_workout(
            template_path=template_path,
            name=workout['name'],
            description=workout['description'],
            workout_blocks=workout['blocks'],
            output_path=output_path
        )
        total_workouts += 1
    print(f"✓ Week 3 VO2max complete: {len(week_3_vo2max)} files generated")
    
    # Week 3: OPTION B - Threshold Block Peak (7 workouts)
    print("\n🔧 WEEK 3: OPTION B - Threshold Block Peak Loading")
    for workout in week_3_threshold:
        base_name = workout['name'].replace(' ', '_').replace('/', '_').replace('#', '')
        if '_THRESHOLD' not in base_name:
            base_name += '_Threshold'
        output_path = os.path.join(output_dir, f"{base_name}.zwo")
        create_workout(
            template_path=template_path,
            name=workout['name'],
            description=workout['description'],
            workout_blocks=workout['blocks'],
            output_path=output_path
        )
        total_workouts += 1
    print(f"✓ Week 3 Threshold complete: {len(week_3_threshold)} files generated")
    
    # Week 3: OPTION C - Durability Block Peak (7 workouts)
    print("\n🔧 WEEK 3: OPTION C - Durability Block Peak Loading")
    for workout in week_3_durability:
        base_name = workout['name'].replace(' ', '_').replace('/', '_').replace('#', '')
        if '_DURABILITY' not in base_name:
            base_name += '_Durability'
        output_path = os.path.join(output_dir, f"{base_name}.zwo")
        create_workout(
            template_path=template_path,
            name=workout['name'],
            description=workout['description'],
            workout_blocks=workout['blocks'],
            output_path=output_path
        )
        total_workouts += 1
    print(f"✓ Week 3 Durability complete: {len(week_3_durability)} files generated")
    
    # Week 4: Recovery & Transmutation (7 workouts)
    print("\n🔧 WEEK 4: Recovery & Transmutation")
    for workout in week_4:
        output_path = os.path.join(output_dir, f"{workout['name'].replace(' ', '_').replace('/', '_').replace('#', '')}.zwo")
        create_workout(
            template_path=template_path,
            name=workout['name'],
            description=workout['description'],
            workout_blocks=workout['blocks'],
            output_path=output_path
        )
        total_workouts += 1
    print(f"✓ Week 4 complete: {len(week_4)} files generated")
    
    # Week 5: Race Sharpening (7 workouts)
    print("\n🔧 WEEK 5: Race Sharpening - Mixed Intensity")
    for workout in week_5:
        output_path = os.path.join(output_dir, f"{workout['name'].replace(' ', '_').replace('/', '_').replace('#', '')}.zwo")
        create_workout(
            template_path=template_path,
            name=workout['name'],
            description=workout['description'],
            workout_blocks=workout['blocks'],
            output_path=output_path
        )
        total_workouts += 1
    print(f"✓ Week 5 complete: {len(week_5)} files generated")
    
    # Week 6: Race Week (7 workouts)
    print("\n🔧 WEEK 6: Race Week - Taper & Compete")
    for workout in week_6:
        output_path = os.path.join(output_dir, f"{workout['name'].replace(' ', '_').replace('/', '_').replace('#', '')}.zwo")
        create_workout(
            template_path=template_path,
            name=workout['name'],
            description=workout['description'],
            workout_blocks=workout['blocks'],
            output_path=output_path
        )
        total_workouts += 1
    print(f"✓ Week 6 complete: {len(week_6)} files generated")
    
    print("\n" + "=" * 60)
    print(f"🎉 GENERATION COMPLETE!")
    print(f"Total files generated: {total_workouts}")
    print(f"Output directory: {output_dir}")
    print("=" * 60)
    print("\nIMPORTANT: You have 3 block options for Weeks 2-3:")
    print("  - VO2max Block: Use files ending in '_VO2max'")
    print("  - Threshold Block: Use files ending in '_Threshold'")
    print("  - Durability Block: Use files ending in '_Durability'")
    print("\nChoose ONE block path based on your Week 1 assessment.")
    print("Delete the other two block options before uploading to TrainingPeaks.")
    print("\nNEXT STEPS:")
    print("1. Review Week 1 assessment results")
    print("2. Choose your block path (VO2max, Threshold, or Durability)")
    print("3. Delete the other two block options from generated files")
    print("4. Test upload ONE file to TrainingPeaks first")
    print("5. If successful, upload all files for your chosen path")
    print("6. Publish your emergency training plan!")

