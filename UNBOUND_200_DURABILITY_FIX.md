# Durability Workouts - Corrected Understanding

## ✅ CORRECTED: Durability Workout Structure

**❌ BEFORE (Incorrect):**
- Durability workouts = long endurance rides with position alternation
- Just long Z2 rides

**✅ AFTER (Corrected):**
- **Durability workouts = Long Z2 ride FIRST → THEN intervals while fatigued**
- This simulates race conditions where you need to perform intervals after hours of riding

## Structure

### Pattern:
```
First X hours Z2 (builds fatigue)
    ↓
Intervals (performed while already tired)
    ↓
Final Y hours Z2 (optional, completes ride)
```

### Example from Finisher Beginner Plan:
**"W05 Sat - Long Endurance with Intensity"**
- **Structure**: First 90 min Z2 → 3x15 min @ 87-92% FTP (5 min easy between) → Final 60 min Z2
- **Purpose**: Building your ability to hit intensity when already tired. This is race simulation.

### Example from Podium GOAT Plan:
**"W03 Sat - Peak Long Pyramidal"**
- **Structure**: First 3.5 hours Z2 → 6x15 min @ 80-85% FTP → 5x4 min @ 105-110% FTP → Final 1.5 hours Z2
- **Purpose**: Peak long ride with integrated intensity. This is what elite gravel preparation looks like.

## Why This Matters

1. **Race Simulation**: In a 12-16 hour gravel race, you need to push hard after hours of riding
2. **Fatigue Management**: Teaches your body to sustain power when tired
3. **Metabolic Efficiency**: Builds ability to perform intervals with accumulated fatigue
4. **Mental Toughness**: Prepares you for the reality of racing when you're already tired

## Implementation in Generator

The workout description generator now:
1. **Detects durability workouts**: Z2 blocks (0.65-0.72 power) BEFORE intervals
2. **Formats correctly**: "First X hours Z2 → intervals → Final Y hours Z2"
3. **Explains purpose**: "Building your ability to perform intervals when already fatigued—this is race simulation"
4. **Position guidance**: 
   - Z2 sections: Position alternation every 30 min (drops ↔ hoods)
   - Intervals: Position as specified for interval type (seated, hoods, etc.)

## Updated Documentation

All plans now correctly identify and format durability workouts with:
- Proper structure description
- Race simulation explanation
- Position alternation guidance for Z2 sections
- Interval-specific position guidance
- Purpose explanation emphasizing fatigue management

---

*Corrected: December 26, 2025*  
*Understanding: Durability = Long ride FIRST, THEN intervals while fatigued*

