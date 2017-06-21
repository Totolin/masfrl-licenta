from world import Environment, stringify_properties


def split_environment(environment, agents):
    split_x = 20
    split_y = 20

    corner_left = (0, 20)
    corner_right = (20, 10)

    split_walls = []
    split_specials = []

    for (x, y) in environment.walls:
        if corner_right[0] >= x >= corner_left[0]:
            if corner_left[1] >= y >= corner_right[1]:
                split_walls.append((x, y))

    for (x, y, c, w) in environment.specials:
        if corner_right[0] >= x >= corner_left[0]:
            if corner_left[1] >= y >= corner_right[1]:
                split_specials.append((x, y, c, w))

    # manually split for now
    return stringify_properties(
        split_x,
        split_y,
        None,
        environment.actions,
        split_specials,
        split_walls,
        environment.walk_reward,
        environment.reset_score
    )
