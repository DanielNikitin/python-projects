# -------- CIRCLE/RECTANGLE COLLISION DETECT
def rectangle_collision(obj1, obj2):  # obj1 obj2 условные аргументы
    # Rectangle collision
    return obj1.x < obj2.x + obj2.width and \
           obj1.x + obj1.width > obj2.x and \
           obj1.y < obj2.y + obj2.height and \
           obj1.y + obj1.height > obj2.y

def circle_collision(obj1, obj2):
    # Circle-rectangle collision
    obj1_center = (obj1.x + obj1.width // 2, obj1.y + obj1.height // 2)
    obj2_center = (obj2.x + obj2.width // 2, obj2.y + obj2.height // 2)
    distance_squared = (obj1_center[0] - obj2_center[0])**2 + (obj1_center[1] - obj2_center[1])**2
    radius_sum_squared = (obj1.collision_radius + obj2.collision_radius)**2
    return distance_squared < radius_sum_squared


# -------- RECTANGLE CHECK TOUCHING
def get_touching_side(player, obj):
    # calculate the coordinates of the sides for player1 and obj2
    player_left = player.x
    player_right = player.x + player.width
    player_top = player.y
    player_bottom = player.y + player.height

    obj_left = obj.x
    obj_right = obj.x + obj.width
    obj_top = obj.y
    obj_bottom = obj.y + obj.height

    # Check if rectangles are touching
    # сравниваем координаты и размеры двух обьектов
    if (
        player_left < obj_right and
        player_right > obj_left and
        player_top < obj_bottom and
        player_bottom > obj_top
    ):

        # Calculate overlapping area
        # если прямоугольники пересекаются, то рассчитывается область перекрытия
        overlap_left = max(player_left, obj_left)
        overlap_right = min(player_right, obj_right)
        overlap_top = max(player_top, obj_top)
        overlap_bottom = min(player_bottom, obj_bottom)

        # Calculate side lengths of the overlapping area
        # рассчитываются длины сторон этой области перекрытия
        overlap_width = overlap_right - overlap_left
        overlap_height = overlap_bottom - overlap_top

        # Determine which side has more overlap
        # определяется, по какой стороне больше перекрытия
        if overlap_width > overlap_height:
            # В зависимости от того, с какой стороны больше перекрытие,
            # и с какой стороны объекта находится игрок, возвращается соответствующая сторона столкновения
            if player.y > obj.y:
                return "top"
            else:
                return "bottom"
        else:
            if player.x > obj.x:
                return "left"
            else:
                return "right"
    else:
        return None

def is_touching(obj1, obj2):
    touching_side = get_touching_side(obj1, obj2)
    if touching_side:
        print(f"Touching: Игрок {obj1.name} касается объекта {obj2.id} стороной {touching_side}")