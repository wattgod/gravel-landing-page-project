# Nate's Workout Dimensions - What We're Missing

## Comparison: Nate's Workouts vs Our Current Implementation

### ✅ WHAT WE'RE DOING WELL

1. **Cadence Prescriptions** - We have cadence guidance by archetype
2. **Position Guidance** - We have position prescriptions (seated, hoods, drops)
3. **Durability Workouts** - We now correctly identify them (Z2 → intervals)
4. **Clean XML Structure** - Following Nate's architecture standards
5. **PURPOSE Section** - We have archetype-specific PURPOSE explanations

### ❌ WHAT WE'RE MISSING

#### 1. **In-Saddle vs Out-of-Saddle Specifications**

**Nate's Examples:**
- "alternate roughly 2. 5min seated, 30 sec standing"
- "alternate one seated, one standing"
- "out of the saddle sprint intervals"
- "seated accelerations"
- "10x10sec out of the saddle sprint intervals"

**Our Current Implementation:**
- We have position prescriptions but they're general ("Seated, hoods")
- We don't explicitly specify when to stand vs sit
- We don't have alternating seated/standing patterns

**What We Should Add:**
- Explicit "seated" vs "out of saddle" guidance for:
  - Sprint intervals (out of saddle)
  - Climbing efforts (alternating seated/standing)
  - Surge efforts (alternating seated/standing)
  - Accelerations (seated for leg speed, standing for power)

#### 2. **More Specific Cadence Targets**

**Nate's Examples:**
- "mostly done @ 95+ rpm"
- "100+ rpm" (high cadence work)
- "110+ rpm" (leg speed work)
- "50-60 rpm" (SFR/force work)
- "100-120rpm" (high cadence Z3)

**Our Current Implementation:**
- We have cadence ranges (e.g., "90-100rpm")
- But we don't always specify "95+ rpm" for high cadence emphasis
- We don't have "110+ rpm" for leg speed work

**What We Should Add:**
- More specific cadence targets when cadence is a focus:
  - High cadence work: "100+ rpm" or "100-120rpm"
  - Leg speed: "110+ rpm"
  - Force work: "50-60rpm"
  - Recovery spins: "95+ rpm"

#### 3. **Position-Specific Instructions in Descriptions**

**Nate's Examples:**
- "Get in the drops when possible"
- "Try and do as much of this 60min block in the drops as you can"
- "alternate roughly 2. 5min seated, 30 sec standing"

**Our Current Implementation:**
- We have position prescriptions in PURPOSE section
- But we don't have specific instructions like "get in the drops" in the MAIN SET description
- We don't have "try to do X in the drops" guidance

**What We Should Add:**
- Specific position instructions in MAIN SET:
  - "Get in the drops when possible"
  - "Try to do as much of this block in the drops"
  - "Alternate: 5min seated, 30sec standing"

#### 4. **Cadence in XML Attributes (More Consistent Use)**

**Nate's Examples:**
- `<SteadyState Duration="300" Power="0.87" CadenceLow="100" CadenceHigh="120" />`
- `<IntervalsT ... Cadence="88" ... />`
- `<IntervalsT ... Cadence="55" CadenceResting="65" />`

**Our Current Implementation:**
- We use CadenceLow/CadenceHigh for Z3 SteadyState
- We use Cadence/CadenceResting for SFR IntervalsT
- But we might not be using Cadence attribute for all intervals where it's relevant

**What We Should Add:**
- Cadence attribute for IntervalsT when cadence is a training focus:
  - VO2max intervals: `Cadence="90"` or `Cadence="100"`
  - Threshold intervals: `Cadence="88"`
  - Tempo intervals: `Cadence="88"`
  - Recovery: `CadenceResting="65"` or similar

#### 5. **Surge/Acceleration Patterns**

**Nate's Examples:**
- "every 10min do a hard 10 sec standing acceleration"
- "every 5min do a hard 10-15 sec surge - alternate one seated, one standing"
- "15sec 'on' (150% FTP) and 15 sec 'off' (50% FTP)"

**Our Current Implementation:**
- We don't have specific surge patterns
- We don't have "every X minutes do Y" patterns
- We don't have alternating seated/standing surge patterns

**What We Should Add:**
- Surge patterns in endurance rides:
  - "Every 10min: 10sec standing acceleration"
  - "Every 5min: 10-15sec surge (alternate seated/standing)"
  - These could be in the MAIN SET description

#### 6. **Cadence Play/Variations**

**Nate's Examples:**
- "Z1/Z2 warmup, mostly done @ 95+ rpm"
- "4x30 sec seated accelerations @ 110+ rpm / 60 sec recovery - make these about leg speed more than power"

**Our Current Implementation:**
- We don't have "cadence play" as a specific dimension
- We don't have leg speed accelerations separate from power work

**What We Should Add:**
- Cadence play instructions:
  - "Mostly done @ 95+ rpm" for warmups
  - "Seated accelerations @ 110+ rpm - leg speed focus, not power"
  - Cadence variations within workouts

#### 7. **Progressive Cadence/Power Changes**

**Nate's Examples:**
- "start low and increase over the course the effort, accelerate the last 30 sec"
- "1min VO2 power (400-450), 9min tempo (300-330), 5min LT (350-380)"

**Our Current Implementation:**
- We have progressive threshold work
- But we don't always specify "start low and build" or "accelerate the last 30 sec"

**What We Should Add:**
- Progressive effort instructions:
  - "Start low and increase over the course"
  - "Accelerate the last 30 seconds"
  - Progressive cadence changes

---

## RECOMMENDATIONS

### High Priority (Should Add):

1. **In-Saddle vs Out-of-Saddle Specifications**
   - Add explicit "seated" vs "out of saddle" for sprints, climbs, surges
   - Add alternating patterns (seated/standing)

2. **More Specific Cadence Targets**
   - Use "100+ rpm" instead of just "90-100rpm" when emphasizing high cadence
   - Add "110+ rpm" for leg speed work
   - Add "95+ rpm" for recovery spins

3. **Position Instructions in MAIN SET**
   - Add "Get in the drops when possible"
   - Add "Try to do X in the drops"
   - Add specific position alternation patterns

### Medium Priority (Nice to Have):

4. **Cadence in XML Attributes**
   - Use Cadence attribute more consistently for IntervalsT
   - Add CadenceResting for recovery periods

5. **Surge/Acceleration Patterns**
   - Add "every X minutes do Y" patterns
   - Add alternating seated/standing surge patterns

### Low Priority (Future Enhancement):

6. **Cadence Play/Variations**
   - Add cadence play as a specific dimension
   - Add leg speed accelerations separate from power work

7. **Progressive Instructions**
   - Add "start low and build" instructions
   - Add "accelerate the last 30 seconds" instructions

---

## IMPLEMENTATION PLAN

### Step 1: Update Position Prescriptions
- Add "out of saddle" for sprint/neuromuscular work
- Add "alternating seated/standing" for climbing/surge work
- Add specific position instructions in MAIN SET descriptions

### Step 2: Update Cadence Prescriptions
- Make cadence targets more specific when cadence is a focus
- Add "100+ rpm" for high cadence emphasis
- Add "110+ rpm" for leg speed work

### Step 3: Add Surge Patterns
- Detect surge patterns in workout descriptions
- Add "every X minutes do Y" instructions
- Add alternating seated/standing patterns

### Step 4: Update XML Generation
- Add Cadence attribute to IntervalsT more consistently
- Add CadenceResting for recovery periods
- Ensure CadenceLow/CadenceHigh for all Z3 SteadyState

---

*Analysis Date: December 26, 2025*  
*Source: Nate's workout-archetypes repository*

