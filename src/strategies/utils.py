def reverse(map: list[list[int]]) -> list[list[int]]:
    result: list[list[int]] = []
    for i in range(len(map[0])):
        tmp = []
        for j in range(len(map)):
            tmp.append(map[j][i])
        result.append(tmp)
    return result


def get_adj(pos: tuple[int, int],
            map: list[list[int]]
            ) -> list[tuple[int, int]]:
    #  west, south, east, north
    result = []
    x, y = pos
    value = format(map[x][y], '04b')
    if value[0] == '0':
        result.append((x - 1, y))
    if value[1] == '0':
        result.append((x, y + 1))
    if value[2] == '0':
        result.append((x + 1, y))
    if value[3] == '0':
        result.append((x, y - 1))
    return result
