from world import stringify_properties


def split_environment(environment, agents, length=40):

    coords = get_coords_by_agents(agents, length)
    split_env = []

    for i in range(agents):

        corner_left = coords[i]['left']
        corner_right = coords[i]['right']

        split_walls = []
        split_specials = []

        for (x, y) in environment.walls:
            if corner_right[0] >= x >= corner_left[0]:
                if corner_right[1] >= y >= corner_left[1]:
                    split_walls.append((x, y))

        for (x, y, c, w) in environment.specials:
            if corner_right[0] >= x >= corner_left[0]:
                if corner_right[1] >= y >= corner_left[1]:
                    split_specials.append((x, y, c, w))

        for i in range(0, length):
            for j in range(0, length):
                if not (corner_right[0] >= i >= corner_left[0]) or not (corner_right[1] >= j >= corner_left[1]):
                    split_walls.append((i, j))

        split_env.append(stringify_properties(
            length,
            length,
            None,
            environment.actions,
            split_specials,
            split_walls,
            environment.walk_reward,
            environment.reset_score
        ))

    return split_env


def get_coords_by_agents(agents, length):

    coords = []

    if agents == 4:
        # Split environment to 4 agents
        coords.append(
            {
                "left": (0, 0),
                "right": (length / 2 - 1, length / 2 - 1),
            }
        )
        coords.append(
            {
                "left": (length/2, 0),
                "right": (length-1, length / 2 - 1),
            }
        )
        coords.append(
            {
                "left": (0, length/2),
                "right": (length / 2 - 1, length - 1),
            }
        )
        coords.append(
            {
                "left": (length/2, length/2),
                "right": (length - 1, length - 1),
            }
        )

    elif agents == 3:
        coords.append(
            {
                "left": (0, 0),
                "right": (length - 1, length / 2 - 1),
            }
        )
        coords.append(
            {
                "left": (0, length / 2),
                "right": (length / 2 - 1, length - 1),
            }
        )
        coords.append(
            {
                "left": (length / 2, length / 2),
                "right": (length - 1, length - 1),
            }
        )

    elif agents == 2:
        coords.append(
            {
                "left": (0, 0),
                "right": (length - 1, length / 2 - 1),
            }
        )
        coords.append(
            {
                "left": (0, length / 2),
                "right": (length - 1, length - 1),
            }
        )

    elif agents == 1:
        coords.append(
            {
                "left": (0, 0),
                "right": (length - 1, length - 1),
            }
        )

    return coords