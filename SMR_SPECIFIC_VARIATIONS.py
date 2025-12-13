# SAVE MY RACE SPECIFIC VARIATIONS
# Purpose: Salvage/urgency positioning for 6-week emergency plans
# User instruction: "Even if life got in the way and you haven't been training 
# (or you've been lazy), you'd be surprised how much your body can improve in 
# six weeks. Don't defer your entry, cram some training and make it happen."
#
# KEY POSITIONING:
# - Salvage/urgency, not performance/progression
# - 6 weeks mentioned prominently
# - Triage approach: what matters most, what you can skip
# - Minimum viable fitness, not optimal
# - Life got in the way, don't defer

SMR_OPENINGS = [
    # Variation 1: Salvage/urgency
    "Six weeks before {race_name} isn't ideal preparation time. But it's salvageable. Life got in the way—training didn't happen. Don't defer your entry. You'd be surprised how much your body can improve in six weeks if you focus on what actually matters.",
    
    # Variation 2: Life got in the way
    "Even if life got in the way and you haven't been training (or you've been lazy), you'd be surprised how much your body can improve in six weeks. Don't defer your entry. Cram some training and make it happen. This plan shows you how.",
    
    # Variation 3: Emergency salvage
    "Six weeks. That's what you've got. Life got in the way. Training didn't happen. But you're not deferring. This plan is for people who refuse to wait another year. You'd be surprised how much you can build in six weeks if you focus on what actually matters.",
    
    # Variation 4: Don't defer
    "You're six weeks out and behind on training. Don't defer your entry. Don't wait for perfect preparation that never comes. Life will get in the way again. This plan builds minimum viable fitness to finish—not optimal, but sufficient.",
    
    # Variation 5: Cram and make it happen
    "Six weeks before {race_name}. You haven't been training. Life got in the way. But you're showing up anyway. This plan is for people who refuse to defer. Cram the training. Make it happen. You'd be surprised what six weeks of focused work can do.",
]

SMR_STORIES = [
    # Variation 1: Triage approach (NO "life got in the way" - already in opening)
    """This isn't about unlocking peak performance. It's about building minimum viable fitness to finish. The {plan_name} triages: race-critical skills first, mental preparation second, base fitness third. Not perfect preparation. Sufficient preparation.""",
    
    # Variation 2: What matters most (NO "life got in the way")
    """Six weeks isn't enough for perfect preparation. But it's enough for sufficient preparation. The {plan_name} focuses on what matters most: fueling that works, pacing that prevents bonking, mental protocols for when it gets hard. Everything else is optional.""",
    
    # Variation 3: Emergency protocols (NO "life got in the way" - rephrased)
    """Training fell apart. Work got busy. Kids got sick. But you're not deferring. The {plan_name} is built for this exact situation: compressed timeline, race-critical focus, emergency protocols. You won't build peak fitness in six weeks. But you'll build enough to finish.""",
    
    # Variation 4: Minimum viable (NO "life got in the way")
    """This isn't about building optimal fitness. It's about building enough fitness to finish. The {plan_name} uses a triage approach: what you must have (fueling, pacing, mental toughness), what you can skip (volume, perfect progression). Six weeks. Focused work. Make it happen.""",
    
    # Variation 5: Haven't been training (NO "life got in the way")
    """You haven't been training. But you're not deferring. The {plan_name} is built for this exact situation: compressed timeline, race-critical focus, emergency protocols. Six weeks isn't much time. But the plan makes it work.""",
    
    # Variation 6: Six weeks focus (NO "life got in the way")
    """Six weeks isn't much time. But the plan makes it work: compressed timeline, race-critical focus, emergency protocols. You won't build peak fitness in six weeks. But you'll build enough to finish.""",
]

SMR_FEATURES = [
    "**6-week compressed timeline: race-critical focus only, everything else optional**",
    "**Triage system: what matters most (fueling, pacing), what you can skip (volume)**",
    "**Emergency mental preparation: practiced protocols for when suffering hits**",
    "**Minimum viable fitness: enough to finish, not enough to compete**",
    "**Race-critical skills only: fueling that works, pacing that prevents bonking**",
    "**Compressed preparation: six weeks of focused work, not perfect progression**",
    "**Emergency protocols: what you must have to finish, what you can skip**",
    "**Life got in the way? This plan is built for that exact situation**",
]

SMR_GUIDE_TOPICS = [
    "**Your 6-Week Arc** — Compressed timeline focusing on race-critical fitness only",
    "**Triage Approach** — What matters most (fueling, pacing), what you can skip (volume)",
    "**Emergency Mental Preparation** — Protocols for when it gets hard, practiced in training",
    "**Minimum Viable Fitness** — Enough to finish, not enough to compete",
    "**Race-Critical Skills** — Fueling that works, pacing that prevents bonking",
    "**6-Week Compressed Timeline** — Focused work, not perfect progression",
    "**Emergency Protocols** — What you must have to finish, what you can skip",
    "**Life Got in the Way?** — This guide is built for that exact situation",
]

SMR_ALTERNATIVES = [
    "Or defer to next year. Skip the race. Wait for perfect preparation that never comes. Life will get in the way again.",
    "Or show up undertrained and survive through suffering alone. Hope adrenaline and determination are enough.",
    "Or wait for perfect preparation. Defer your entry. Life will get in the way again next year too.",
    "Or skip the race entirely. Defer to next year. Wait for training that never happens because life always gets in the way.",
    "Or show up completely unprepared. Hope grit alone gets you through 200 miles. It won't.",
]

SMR_CLOSINGS = [
    "Built for {race_name}. For people who haven't been training but refuse to defer. Six weeks. Cram the training and make it happen.",
    "For people with six weeks before {race_name}. Life got in the way. Training didn't happen. But you're not deferring—you're cramming and making it work.",
    "Six weeks before race day. Behind on training. Not deferring. This is the plan for making it happen anyway.",
    "Built for {race_name}. For people who haven't been training but refuse to postpone. Six weeks. Cram the work. Make it happen.",
    "This is {race_name}. For people who refuse to wait another year. Six weeks. Behind on training. Not deferring. Make it happen.",
]

# SMR-SPECIFIC VALUE PROP BOXES
# Purpose: Urgency/salvage positioning, NOT performance/progression
# Must emphasize: minimum viable, sufficient not perfect, triage approach

SMR_VALUE_PROP_BOXES = [
    {
        "philosophy": "Six weeks isn't enough for perfect preparation. But it's enough to finish. Emergency protocols for mental preparation. Triage focus on race-critical skills.",
        "props": ["Emergency mental preparation protocols", "Triage system: what matters most", "Minimum viable fitness approach", "Six-week compressed timeline"]
    },
    {
        "philosophy": "Salvage mission, not optimization. Focus on what gets you across the line: fueling, mental prep, pacing. Everything else is optional.",
        "props": ["Race-critical skills only", "Emergency protocols for when it gets hard", "Triage approach: what you can skip", "Sufficient preparation, not perfect"]
    },
    {
        "philosophy": "Minimum viable fitness—not optimal, sufficient. You won't build peak fitness in six weeks. But you'll build enough.",
        "props": ["Compressed timeline: six weeks", "Race-critical focus only", "Emergency mental preparation", "Triage system: what matters most"]
    },
    {
        "philosophy": "Life got in the way. Training didn't happen. This plan is built for that exact situation: salvage what you can, focus on what matters.",
        "props": ["Six-week emergency protocols", "Triage approach to training", "Minimum viable fitness", "Race-critical skills first"]
    },
]

