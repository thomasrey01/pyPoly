from material import Material
from collisions import collision_types

material_list = {
    "asphalt": Material("asphalt", 100, 999, 2, 5, collision_types["asphalt"], 1, (10, 10, 10, 255)),
    "wood": Material("wood", 100, 999, 3, 5, collision_types["wood"], 1, (164, 116, 73, 255)),
}
