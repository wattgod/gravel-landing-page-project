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

SMR_STORY_JUSTIFICATIONS = {
    'finisher': [
        "Training fell apart. Work got busy. Kids got sick. But you're not deferring. The Finisher Save My Race plan is built for this exact situation—6 weeks to cram the essentials and make it happen.",
        "You haven't been training consistently. Maybe at all. But Unbound Gravel 200 is still happening. Six weeks isn't enough for perfect preparation, but it's enough to finish if you focus on what matters.",
        "Life happened. Training didn't. You've got six weeks. The Finisher Save My Race plan strips away everything except race-critical preparation: fueling protocols, mental strategies, enough volume to survive 200 miles."
    ],
    'compete': [
        "Six weeks before a competitive effort isn't ideal. But it's salvageable. Emergency protocols focus on maintaining existing fitness while adding race-critical sharpness.",
        "You haven't been training. But you still want to compete, not just finish. Six weeks of compressed preparation—intensity over volume, race-specific sharpness over base building.",
        "Training didn't happen. Racing still will. Six weeks to salvage competitive fitness: threshold sharpness, fueling precision, mental protocols that work under pressure."
    ],
    'ayahuasca': [
        "Six weeks. 0-5 hours per week. Still planning to race Unbound Gravel 200. The Ayahuasca Save My Race plan is brutally honest: you won't be fast, but you can finish if you nail the controllables.",
        "Life left you with almost no training time and six weeks before Unbound. Don't defer. The Ayahuasca Save My Race plan focuses entirely on what gets you across the line: mental preparation, fueling strategy, equipment choices.",
        "You've got minimal time and six weeks until Unbound Gravel 200. The plan prioritizes survival essentials: practiced fueling protocols, mental strategies for low points, equipment that won't fail you."
    ],
    'podium': [
        "Six weeks before a podium attempt is a crisis. But competitive fitness doesn't disappear instantly. Emergency protocols maintain sharpness while adding race-critical elements you can't skip.",
        "Training fell apart with six weeks to go. Podium goals haven't changed. The Save My Race plan salvages competitive capacity: threshold precision, race-specific intensity, mental preparation for performing under pressure.",
        "You haven't been training. You still want to podium. Six weeks of compressed race-specific preparation—no base building, just sharpness and race execution under competitive demands."
    ]
}

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

SMR_CLOSINGS = {
    'finisher': [
        "Built for Unbound Gravel 200. For people who haven't been training but refuse to defer. Six weeks. Cram the training and make it happen.",
        "For people with six weeks before Unbound. Life got in the way. Training didn't happen. But you're not deferring—you're cramming and making it work.",
        "Six weeks before Unbound Gravel 200. You haven't been training. Don't defer. Focus on race-critical preparation and finish the race."
    ],
    'compete': [
        "Built for Unbound Gravel 200. For competitive athletes whose training fell apart with six weeks to go. Salvage fitness. Execute anyway.",
        "Six weeks before Unbound. Training didn't happen. Competitive goals haven't changed. Emergency protocols to salvage race-day sharpness.",
        "For people who still want to compete at Unbound despite imperfect preparation. Six weeks. Compressed timeline. Race-critical focus."
    ],
    'ayahuasca': [
        "Built for Unbound Gravel 200. For people with minimal time and six weeks to prepare. You won't be fast. But you can finish.",
        "Six weeks. 0-5 hours per week. Still racing Unbound. Survival preparation: mental protocols, fueling strategy, realistic expectations.",
        "For people with almost no training time before Unbound. Emergency preparation focusing on what you can control: mind, nutrition, equipment."
    ],
    'podium': [
        "Built for Unbound Gravel 200. For competitive athletes with six weeks to salvage podium fitness. Emergency timeline. Execute anyway.",
        "Six weeks before Unbound. Training fell apart. Podium goals haven't. Compressed race-specific preparation for competitive performance despite imperfect prep.",
        "For athletes who still want to podium at Unbound despite training gaps. Six weeks of race-critical sharpness and competitive execution protocols."
    ]
}

# SMR-SPECIFIC VALUE PROP BOXES (tier-specific)
# Purpose: Urgency/salvage positioning, NOT performance/progression
# Must emphasize: minimum viable, sufficient not perfect, triage approach

SMR_VALUE_PROP_BOXES = {
    'finisher': [
        "Six weeks isn't enough for perfect preparation. But it's enough to finish. Emergency protocols for mental preparation when things get hard. Triage focus on race-critical skills: fueling, pacing, survival strategies.",
        "Salvage mission, not optimization. Focus on what gets you across the line: fueling protocols practiced under load, mental strategies for low points, enough volume to survive 200 miles. Everything else is optional.",
        "Compressed timeline requires brutal prioritization. Fueling precision over fitness gains. Mental protocols over volume accumulation. Race-critical preparation over systematic development."
    ],
    'compete': [
        "Six weeks to salvage competitive fitness. Threshold sharpness over base volume. Race execution protocols over systematic progression. Mental preparation for performing when training wasn't ideal.",
        "Emergency timeline demands focus. Maintain existing fitness. Add race-critical sharpness. Practice protocols that work under competitive pressure. Accept limitations, execute anyway.",
        "Compressed preparation for competitive goals. Intensity over volume. Sharpness over endurance. Practiced race execution when preparation time ran out."
    ],
    'ayahuasca': [
        "Six weeks with minimal training time. Focus entirely on controllables: fueling strategy, mental preparation, equipment choices. Fitness won't be high, but you can still finish.",
        "Survival preparation, not performance preparation. Mental protocols for when it gets hard. Practiced fueling at low intensity. Equipment that won't fail. Realistic expectations about pace.",
        "Minimal time requires brutal honesty. You won't be fast. But you can finish if you nail the essentials: fueling every hour, mental strategies for suffering, pacing that prevents blowups."
    ],
    'podium': [
        "Emergency protocols for maintaining competitive capacity. Threshold precision over volume accumulation. Race-specific sharpness over systematic development. Mental preparation for performing despite imperfect preparation.",
        "Six weeks to salvage podium fitness. High-intensity sharpness. Race execution under pressure. Fueling precision at competitive watts. Accept the timeline, execute the plan.",
        "Compressed timeline for competitive goals. Maintain existing threshold capacity. Add race-critical intensity. Practice protocols that work when training fell short."
    ]
}

