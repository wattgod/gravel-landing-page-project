# TIER-SPECIFIC CHOICE FEATURES
# Phase 2: Tier-specific methodology solutions
# Purpose: What you get that solves YOUR tier-specific problem
# Variations: 8 per tier (32 total)

CHOICE_FEATURES = {
    "ayahuasca": [
        "**High-efficiency workouts** designed for maximum adaptation in minimal time—every session under 90 minutes",
        "**Skills-first approach** that prevents mechanical failures and crashes from killing your race (Section 7)",
        "**Fueling protocols** tested on limited training volume—60-80g carbs/hour without GI distress (Section 8)",
        "**Race-pace power targets** calibrated for your available training time, not fantasy watts",
        "**Outdoor options** for every workout—no trainer required, just structured execution",
        "**Strategic recovery** that doesn't assume you have 12+ hours to absorb training stress",
        "**Taper protocol** designed for athletes who can't afford to lose fitness in rest weeks",
        "**Dress rehearsal rides** at manageable duration (5 hours max) that still validate your race-day systems",
        "**Recovery protocols for 50+ athletes**—longer recovery windows, strategic rest that prevents breakdown",
        "**Age-appropriate training load**—moderate volume respecting longer adaptation timelines at 45+",
        "**Injury prevention through recovery**—training matched to adaptation capacity, not chronological age"
    ],
    
    "finisher": [
        "**Polarized training distribution** that builds both durability (Zone 2) and speed (Zone 4-5)—no more junk miles",
        "**Progressive overload system** with clear weekly targets—intensity increases predictably, not randomly",
        "**Race-specific power zones** calibrated from YOUR FTP, with RPE guidance when power isn't available (Section 5)",
        "**Technical skills curriculum** covering cornering, descending, and rough-terrain bike handling (Section 7)",
        "**Structured taper** in final 2 weeks—proven protocol that peaks fitness without losing form",
        "**Heat adaptation weeks** (6-10) that improve performance 5-8% through controlled exposure (Section 11)",
        "**Dress rehearsal ride** at 7 hours validating fueling, pacing, and equipment choices",
        "**Pacing strategy guide** for 10-14 hour efforts—how to start conservatively and finish strong (Section 10)",
        "**Recovery protocols for 50+ athletes**—longer recovery windows, HRV monitoring, age-appropriate adaptation timelines",
        "**Injury prevention through strategic recovery**—training load matched to recovery capacity, not chronological age",
        "**Age-appropriate training volume**—moderate hours that respect longer adaptation timelines without sacrificing performance"
    ],
    
    "compete": [
        "**Periodized intensity** with dedicated base, build, and peak phases—no more year-round threshold hammering",
        "**VO2max intervals** that actually improve race performance—not just training-day suffering",
        "**G Spot work** (88-92% FTP)—gravel-specific race-pace training superior to generic Sweet Spot",
        "**Recovery architecture** designed for 12-18 hour weeks—enough stress to adapt, enough rest to absorb",
        "**Precision taper protocol** with deload timing proven for competitive athletes (Section 12)",
        "**Mental training system** for suffering management and tactical decision-making (Section 9)",
        "**Race execution playbook** covering pacing, fueling under fatigue, and group dynamics (Section 10)",
        "**9-hour dress rehearsal** validating everything from nutrition to power distribution at race intensity",
        "**Recovery-first training architecture**—longer rest between hard sessions, HRV-based autoregulation for 45+ athletes",
        "**Age-appropriate periodization**—compressed recovery cycles (2-3 weeks) that respect slower adaptation at 50+",
        "**Injury prevention protocols**—training load matched to recovery capacity, strategic rest that prevents breakdown"
    ],
    
    "podium": [
        "**Polarized volume distribution** with 80% Zone 2, 20% Zone 4-5—proven elite training principle",
        "**Threshold blocks** that build sustainable race pace without overtraining",
        "**VO2max sessions** calibrated for repeatability over 10+ hours—not just 5-minute power",
        "**Heat adaptation protocol** (Weeks 6-10) delivering 5-8% performance gains through systematic exposure",
        "**Recovery metrics** that prevent overtraining—when to push, when to back off (Section 6)",
        "**Altitude protocols** for high-elevation races—if Unbound location demands it (conditional section)",
        "**10-hour dress rehearsal** at race intensity—full validation of systems, fueling, pacing, equipment",
        "**Taper discipline** that prevents panic-training and delivers peak performance on race day"
    ]
}

# VALIDATION
def validate_choice_features():
    """Ensure all tiers have exactly 8 features"""
    required_tiers = ["ayahuasca", "finisher", "compete", "podium"]
    
    for tier in required_tiers:
        count = len(CHOICE_FEATURES[tier])
        assert count == 8, f"{tier} has {count} features, needs 8"
    
    print("✓ All tiers have 8 choice features")
    print(f"✓ Total features: {sum(len(v) for v in CHOICE_FEATURES.values())}")

if __name__ == "__main__":
    validate_choice_features()
