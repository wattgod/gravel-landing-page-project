#!/usr/bin/env python3
"""
FTP Test Converter
Converts TrainingPeaks FTP test format to GG format
"""

import xml.etree.ElementTree as ET
from pathlib import Path

def convert_ftp_test(ftp_test_path, week_num):
    """
    Convert FTP test from TrainingPeaks format to GG format
    
    Args:
        ftp_test_path: Path to FTP test ZWO file
        week_num: Week number for naming
    
    Returns:
        dict with 'name', 'description', 'blocks' for GG format
    """
    try:
        tree = ET.parse(ftp_test_path)
        root = tree.getroot()
    except Exception as e:
        print(f"Error loading FTP test: {e}")
        return None
    
    # Extract workout blocks
    workout_elem = root.find('workout')
    if workout_elem is None:
        return None
    
    blocks = []
    total_duration = 0
    
    # Convert FreeRide + textevents to SteadyState blocks
    for child in workout_elem:
        if child.tag == 'FreeRide':
            duration = int(child.get('Duration', 0))
            total_duration += duration
            
            # Check for textevents to determine power/RPE
            textevents = child.findall('textevent')
            if textevents:
                rpe_text = textevents[0].get('message', '').replace('RPE ', '')
                
                # Convert RPE to power zones
                rpe_power_map = {
                    '2': 0.50,  # Z1 - Easy recovery
                    '3': 0.55,  # Z1 - Easy
                    '4': 0.60,  # Z1-Z2 - Easy
                    '5': 0.65,  # Z2 - Moderate
                    '6': 0.75,  # Z2-Z3 - Moderate-hard
                    '7': 0.85,  # Z3 - Hard
                    '8': 1.00,  # Z4 - Threshold
                    '9': 1.10,  # Z5 - VO2max
                    '10': 1.20  # Z5+ - Max
                }
                
                power = rpe_power_map.get(rpe_text, 0.60)
                
                # Add cadence for certain zones
                if power >= 1.00:
                    blocks.append(f'    <SteadyState Duration="{duration}" Power="{power:.2f}" Cadence="88"/>\n')
                else:
                    blocks.append(f'    <SteadyState Duration="{duration}" Power="{power:.2f}"/>\n')
            else:
                # No textevents - assume easy recovery
                blocks.append(f'    <SteadyState Duration="{duration}" Power="0.55"/>\n')
        else:
            # Keep other elements as-is
            tag = child.tag
            attrs = ' '.join([f'{k}="{v}"' for k, v in child.attrib.items()])
            blocks.append(f'    <{tag} {attrs}/>\n')
    
    blocks_str = "".join(blocks)
    
    # Create GG-formatted description
    description = f"""WARM-UP:
• 12min progressive warmup building from Z1 to Z2

MAIN SET:
• 5min @ RPE 6/10 (moderate effort, Z2-Z3)
• 5min @ RPE 2 (easy recovery, Z1)
• 5min ALL OUT (RPE 8-10). Go as hard as you can for 5 minutes. Start firm but hard for the first 2 minutes, then adjust your effort up or down.
• 5min @ RPE 2 (easy recovery, Z1)
• 20min ALL OUT. Start the effort conservatively at about RPE 8/10 - 20 minutes is a LONG time. This sets your FTP.

COOL-DOWN:
• 10min easy spin Z1-Z2

PURPOSE:
FTP Assessment. This test sets your training zones for the next 6 weeks. Accurate testing = accurate training zones. Write down your average power for the 20-minute effort, multiply by 0.95. That's your FTP.

EXECUTION:
• TERRAIN: You'll want the terrain to be unbroken flat or slightly uphill - you don't want to get caught at a stop light or intersection in the middle of your effort.
• TIMING: Do this test when fresh (not after a hard week). Schedule it for a day when you're well-rested.
• PACING: The 20-minute effort is the key. Start conservatively - you can always push harder in the last 5 minutes. If you blow up early, you'll get an inaccurate FTP.
• RECORDING: Write down your average power for the 20-minute effort immediately after finishing. Multiply by 0.95 to get your FTP."""
    
    return {
        "name": f"W{week_num:02d} Tue - FTP Test",
        "description": description,
        "blocks": blocks_str,
        "week_number": week_num
    }

if __name__ == "__main__":
    # Test conversion
    test_path = Path("/Users/mattirowe/Downloads/2026-01-30_TheAssessm.zwo")
    if test_path.exists():
        result = convert_ftp_test(test_path, 1)
        if result:
            print("✅ FTP Test Conversion Successful")
            print(f"Name: {result['name']}")
            print(f"Blocks length: {len(result['blocks'])} chars")
            print(f"Description length: {len(result['description'])} chars")
        else:
            print("❌ Conversion failed")
    else:
        print(f"⚠️  Test file not found: {test_path}")

