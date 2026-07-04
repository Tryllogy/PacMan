from abc import ABC, abstractmethod
import math
import heapq


class Strategy(ABC):
    def __init__(
            self,
            map_grid: list[list[int]],
            name: str
    ):
        self.name: str = name
        self.map_grid: list[list[int]] = self.reverse(map_grid)
        # self.map_grid: list[list[int]] = map_grid

    def get_path(
        self,
        start: tuple[int, int],
        goal: tuple[int, int] | None = None
    ) -> list[tuple[int, int]]:
        open_heap: list[tuple[float, tuple[int, int]]] = []
        heapq.heappush(open_heap, (0.0, start))
        g_cost: dict[tuple[int, int], float] = {start: 0.0}
        parent: dict[tuple[int, int], tuple[int, int]] = {}
        while open_heap:
            cost, current = heapq.heappop(open_heap)
            if current == goal:
                break
            lst_adj = self.get_adj(current, self.map_grid)
            for adj in lst_adj:
                cost_adj = self.get_cost(adj)
                tentative_g = g_cost[current] + cost_adj
                if (adj not in g_cost or tentative_g < g_cost[adj]):
                    g_cost[adj] = tentative_g
                    parent[adj] = current
                    heapq.heappush(open_heap, (tentative_g, adj))
        result = self.build_path(current, parent)
        result.append(goal)
        print("werers", result)
        result = list(map(lambda x: (x[1], x[0]), result)) #  not sure
        print(result)
        return result

    def build_path(
        self,
        pos: tuple[int, int],
        parents: dict[
            tuple[int, int],
            tuple[int, int]]
    ) -> list[tuple[int, int]]:
        result = []
        tmp = pos
        while parents.get(tmp) is not None:
            tmp = parents.get(tmp)
            result.append(tmp)
        result.reverse()
        return result

    @staticmethod
    def reverse(
        map: list[list[int]]
    ) -> list[list[int]]:
        result: list[list[int]] = []
        for i in range(len(map[0])):
            tmp = []
            for j in range(len(map)):
                tmp.append(map[j][i])
            result.append(tmp)
        return result

    def get_adj(
        self,
        pos: tuple[int, int],
        map_maze: list[list[int]]
    ) -> list[tuple[int, int]]:
        result = []
        x, y = pos
        value = format(map_maze[x][y], '04b')
        if value[0] == '0':
            result.append((x - 1, y))
        if value[1] == '0':
            result.append((x, y + 1))
        if value[2] == '0':
            result.append((x + 1, y))
        if value[3] == '0':
            result.append((x, y - 1))
        return result

    def get_cost(
        self,
        case: tuple[int, int]
    ) -> float:
        x, y = case
        value = format(self.map_grid[x][y], '04b')
        n_wall = sum([int(c) for c in value])
        if n_wall == 2:
            return 1.2
        elif n_wall == 1:
            return 1.1
        elif n_wall == 0:
            return 1.0
        return math.inf

    # Will go to his spawnpoint if killed by player
    def to_spawn(
        self,
        start: tuple[int, int],
        spawnpoint: tuple[int, int]
    ) -> list[tuple[int, int]]:
        return self.get_path(start, spawnpoint)

    @abstractmethod
    def movement(
        self,
        start: tuple[int, int],
        goal: tuple[int, int]
    ) -> list[tuple[int, int]]:
        pass
