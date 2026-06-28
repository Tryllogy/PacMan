from collections import deque


class Case():
    def __init__(self, pos: tuple[int, int], wall_dist: int):
        self.pos = pos
        self.wall_dist = wall_dist


class PathFinder():
    def __init__(self,
                 map: list[list[int]]) -> None:
        self.map = self.reverse(map)
        self.parents = {}

    def reverse(self, map: list[list[int]]) -> list[list[int]]:
        result: list[list[int]] = []
        for i in range(len(map[0])):
            tmp = []
            for j in range(len(map)):
                tmp.append(map[j][i])
            result.append(tmp)
        return result

    def get_adj(self, pos: tuple[int, int]) -> list[tuple[int, int]]:
        #  west, south, east, north
        result = []
        x, y = pos
        value = format(self.map[x][y], '04b')
        if value[0] == '0':
            result.append((x - 1, y))
        if value[1] == '0':
            result.append((x, y + 1))
        if value[2] == '0':
            result.append((x + 1, y))
        if value[3] == '0':
            result.append((x, y - 1))
        return result

    def build_path(self, pos: tuple[int, int]) -> list[tuple[int, int]]:
        result = []
        tmp = pos
        while self.parents.get(tmp) is not None:
            tmp = self.parents.get(tmp)
            result.append(tmp)
        return result

    def build_rev_path(
            self,
            pos: tuple[int, int]
            ) -> list[tuple[int, int]]:
        result = []
        tmp = pos
        rev_parents = {v: k for k, v in self.parents.items()}
        while rev_parents.get(tmp) is not None:
            tmp = rev_parents.get(tmp)
            result.append(tmp)
        return result

    def run(self, start: tuple[int, int]) -> None:
        width = len(map)
        heigh = len(map[0])
        x, y = start
        visited = [[False] * heigh for i in range(width)]
        visited[x][y] = True
        q = deque()
        q.append(start)
        result = []
        parents = {}

        while q:
            curr = q.popleft()
            result.append(curr)
            lst_adj = self.get_adj(curr)
            for adj in lst_adj:
                x, y = adj
                if not visited[x][y]:
                    parents.update({adj: curr})
                    visited[x][y] = True
                    q.append(adj)
        self.parents = parents


if __name__ == '__main__':
    map = [[13, 3, 9, 1, 3], [11, 10, 10, 10, 10], [10, 10, 14, 8, 2], [8, 2, 9, 6, 10], [12, 4, 4, 5, 6]]
    bfs = PathFinder(map)
    bfs.get_adj((0, 0))
    bfs.run((0, 0))
    bfs.build_path((2, 4))
    bfs.build_rev_path((2, 4))
