# TIER-SPECIFIC GUIDE TOPICS
# Phase 3: Guide section highlights with tier-appropriate framing
# Purpose: Show what's in the 18,000-word guide, framed for THEIR tier
# Variations: 8 per tier (32 total)

# VERIFIED GUIDE SECTIONS (from screenshot):
# 1. Training Plan Brief
# 2. Before You Start
# 3. Training Fundamentals ← HIGH VALUE (first principles)
# 4. Your 12-Week Arc
# 5. Training Zones ← HIGH VALUE (stops guessing)
# 6. Workout Execution ← HIGH VALUE (how to do it right)
# 7. Technical Skills for Unbound Gravel 200
# 8. Fueling & Hydration
# 9. Mental Training
# 10. Race Tactics
# 11. Race-Specific Preparation (includes heat protocols)
# 12. Race Week Protocol
# 13. Women-Specific Considerations
# 14. FAQ
# + Masters (conditional)
# + Altitude (conditional)

GUIDE_TOPICS = {
    "ayahuasca": [
        "**Training Fundamentals** — First principles that work with limited hours, not against them",
        "**Training Zones** — FTP-based targets with RPE guidance—no power meter required",
        "**Workout Execution** — How to nail each session type in under 90 minutes",
        "**Technical Skills** — Cornering, descending, rough terrain—skills that prevent race-ending mechanicals",
        "**Fueling & Hydration** — 60-80g carbs/hour protocol tested on limited training volume",
        "**Mental Training** — Suffering management for 10+ hour efforts when your body isn't fully trained",
        "**Race Week Protocol** — Final prep that doesn't assume you have time for elaborate tapers",
        "**FAQ** — Answers to 'can I really finish with 4 hours/week?' and other honest questions",
        "**Masters-Specific Considerations (Section 13)** — Recovery protocols for 50+ athletes, age-appropriate training load",
        "**Recovery Architecture** — Longer adaptation timelines, strategic rest that prevents breakdown at 45+",
        "**Age-Appropriate Training** — Moderate volume with emphasis on recovery, training load matched to adaptation capacity",
        "**Race Tactics: Three-Act Structure** — When to push, when to sit, when to survive—mapped across race timeline with specific decision points",
        "**Recovery Monitoring** — Objective readiness scores guide training adjustments—data replaces guesswork on recovery status"
    ],
    
    "finisher": [
        "**Training Fundamentals** — Polarized principles that build both endurance and speed",
        "**Your 12-Week Arc** — How base, build, and peak phases stack together for race day",
        "**Training Zones** — Precise power targets and RPE guidance for structured progression",
        "**Workout Execution** — How to execute intervals, tempo rides, and endurance sessions correctly",
        "**Technical Skills** — Bike handling that keeps you upright and moving when others crash",
        "**Race Tactics** — Pacing strategy for 10-14 hours—how to start conservatively and finish strong",
        "**Race-Specific Preparation** — Heat adaptation weeks (6-10) delivering 5-8% performance gains",
        "**Race Week Protocol** — Proven taper sequence that peaks fitness without losing form",
        "**Masters-Specific Considerations (Section 13)** — Recovery protocols for 50+ athletes, age-appropriate training load, injury prevention strategies",
        "**Recovery Architecture** — Longer adaptation timelines, recovery monitoring, strategic rest that prevents breakdown at 45+",
        "**Age-Appropriate Training** — Moderate volume with emphasis on recovery, training load matched to adaptation capacity",
        "**Race Tactics: Three-Act Structure** — Conservative start, strategic middle, survival finish mapped to race timeline",
        "**Fueling Protocols: 60-80g Carbs/Hour** — High-carb fueling strategy with practice protocols—automatic execution under stress",
        "**Hydration Strategy** — Electrolyte timing (500-1000mg sodium/hour), fluid intake targets, heat adaptation protocols",
        "**Mental Training Under Stress** — Reframing techniques and suffering management practiced during hard sessions—not just theory",
        "**Technical Skills Practice** — Progressive drills for cornering, descending, rough terrain—weekly practice building competence"
    ],
    
    "compete": [
        "**Training Fundamentals (Section 3)** — Periodization principles that create predictable performance",
        "**Your 12-Week Arc (Section 4)** — Progressive overload system with clear intensity targets",
        "**Workout Execution (Section 6)** — How to nail VO2max, threshold, and race-pace sessions",
        "**Technical Skills (Section 7)** — Advanced bike handling for aggressive racing on rough terrain",
        "**Fueling & Hydration (Section 8)** — Race-pace fueling protocols that work under fatigue",
        "**Mental Training (Section 9)** — Tactical decision-making and suffering management systems",
        "**Race Tactics (Section 10)** — Execution playbook covering pacing, group dynamics, and attack timing",
        "**Race-Specific Preparation (Section 11)** — Heat protocols, altitude adaptation (if needed), equipment choices",
        "**Masters-Specific Considerations (Section 13)** — Recovery protocols acknowledging longer adaptation windows, age-appropriate training load",
        "**Recovery Management** — Data-guided autoregulation, compressed periodization (2-3 week cycles), injury prevention at 45+",
        "**Age-Appropriate Periodization** — Training adapted for slower recovery, moderate volume respecting adaptation timelines",
        "**Race Tactics: Three-Act Structure** — Conservative start, strategic middle, survival finish mapped to race timeline",
        "**Fueling Protocols: 60-80g Carbs/Hour** — High-carb fueling strategy with practice protocols—automatic execution under stress",
        "**Hydration Strategy** — Electrolyte timing (500-1000mg sodium/hour), fluid intake targets, heat adaptation protocols",
        "**Mental Training Under Stress** — Reframing techniques and suffering management practiced during hard sessions—not just theory",
        "**Technical Skills Practice** — Progressive drills for cornering, descending, rough terrain—weekly practice building competence"
    ],
    
    "podium": [
        "**Training Fundamentals** — Elite training principles: 80% Zone 2, 20% Zone 4-5",
        "**Your 12-Week Arc** — Periodized progression with threshold blocks and VO2max phases",
        "**Workout Execution** — Recovery metrics that prevent overtraining while maximizing adaptation",
        "**Technical Skills** — Race-winning bike handling—cornering speeds and descending lines that matter",
        "**Fueling & Hydration** — 60-80g/hour protocols tested at race intensity, not training pace",
        "**Mental Training** — Tactical systems for high-pressure racing and suffering management",
        "**Race Tactics** — Execution strategies for podium-level competition—when to attack, when to wait",
        "**Race Week Protocol** — Taper discipline that delivers peak performance, not panic training",
        "**Race Tactics: Three-Act Structure** — Conservative start, strategic middle, survival finish mapped to race timeline",
        "**Fueling Protocols: 60-80g Carbs/Hour** — High-carb fueling strategy with practice protocols—automatic execution under stress",
        "**Hydration Strategy** — Electrolyte timing (500-1000mg sodium/hour), fluid intake targets, heat adaptation protocols",
        "**Mental Training Under Stress** — Reframing techniques and suffering management practiced during hard sessions—not just theory",
        "**Technical Skills Practice** — Progressive drills for cornering, descending, rough terrain—weekly practice building competence"
    ]
}

# VALIDATION
def validate_guide_topics():
    """Ensure all tiers have exactly 8 topics"""
    required_tiers = ["ayahuasca", "finisher", "compete", "podium"]
    
    for tier in required_tiers:
        count = len(GUIDE_TOPICS[tier])
        assert count == 8, f"{tier} has {count} topics, needs 8"
    
    print("✓ All tiers have 8 guide topics")
    print(f"✓ Total topics: {sum(len(v) for v in GUIDE_TOPICS.values())}")

if __name__ == "__main__":
    validate_guide_topics()
