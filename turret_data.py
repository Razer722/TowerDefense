TURRET_DATA = {
    "basic": [  # Shot by shot
        {"range": 125, "cooldown": 700, "cost": 200, "damage": 5},
        {"range": 150, "cooldown": 500, "cost": 300, "damage": 7},
        {"range": 175, "cooldown": 300, "cost": 400, "damage": 10},
        {"range": 200, "cooldown": 300, "cost": 500, "damage": 12},
    ],
    "sniper": [  # Best for bosses
        {"range": 350, "cooldown": 1500, "cost": 250, "damage": 25},
        {"range": 400, "cooldown": 1200, "cost": 350, "damage": 35},
    ],
    "bomb": [
        {"range": 100, "cooldown": 1000, "cost": 300, "damage": 10},
        {"range": 150, "cooldown": 800, "cost": 400, "damage": 7},
        {"range": 175, "cooldown": 700, "cost": 500, "damage": 15},
        {"range": 200, "cooldown": 600, "cost": 600, "damage": 20},
    ],
    "ice": [{"range": 150, "cooldown": 1200, "cost": 400, "damage": 2}],    # Slows enemies
    "tesla": [{"range": 100, "cooldown": 500, "cost": 600, "damage": 8}],   # Arcs to multiple targets
    "laser": [{"range": 200, "cooldown": 100, "cost": 800, "damage": 1}],   # High fire rate, low damage
    "poison": [{"range": 150, "cooldown": 1500, "cost": 500, "damage": 5}],  # Damage over time
    "railgun": [{"range": 500, "cooldown": 3000, "cost": 1000, "damage": 100}],  # Global range, slow reload
    "minigun": [{"range": 180, "cooldown": 50, "cost": 700, "damage": 2}],  # Rapid fire
    "flamethrower": [{"range": 120, "cooldown": 200, "cost": 550, "damage": 4}],  # Area of effect
    "cannon": [{"range": 200, "cooldown": 1500, "cost": 450, "damage": 20}]  # Heavy physical hitter
}
