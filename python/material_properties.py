from material import Material

material_list = {
    "asphalt": Material("asphalt", 100, 999, 2, 5, 1, (10, 10, 10, 255)),
    "wood": Material("wood", 100, 999, 3, 5, 1, (164, 116, 73, 255)),
}

collision_categories = {
    "ground": 0b00001,
    "car": 0b00010,
    "asphalt": 0b00100,
    "wood": 0b01000,
    "joint": 0b10000
}


collision_masks = {
    "ground": 0b10011,
    "car": 0b00111,
    "asphalt": 0b00010,
    "wood": 0b00000,
    "joint": 0b00001
    }
