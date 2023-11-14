from material import Material
from math import inf
material_list = {
    "asphalt": Material("asphalt", 100, inf, 2, 5, 0.5, 10, (10, 10, 10, 255), 3.5),
    "wood": Material("wood", 100, inf, 3, 5, 0.1, 0, (164, 116, 73, 255), 1.8),
}

collision_categories = {
    "ground": 0b00001,
    "car": 0b00010,
    "asphalt": 0b00100,
    "wood": 0b01000,
    "joint": 0b10000,
}


collision_masks = {
    "ground": 0b10011,
    "car": 0b00111,
    "asphalt": 0b00010,
    "wood": 0b00000,
    "joint": 0b00001,
}
