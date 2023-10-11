collision_types = {
    "ground": 0, 
    "car": 1, 
    "asphalt": 2, 
    "wood": 3, 
    "joint": 4
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

