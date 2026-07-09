from abc import ABC, abstractmethod
import math
import heapq


class Strategy(ABC):
    player_pos: tuple[int, int]
    rand_pos: tuple[int, int]

    def __init__(
            self,
            map_grid: list[list[int]],
            name: str
    ):
        self.name: str = name
        self.map_grid: list[list[int]] = map_grid
        self.duration: int = 5000



    def get_path(
        self,
        phantom_pos: tuple[int, int],
        player_pos: str
    ) -> list[tuple[int, int]]:
        start = phantom_pos
        goal = player_pos
        open_heap: list[tuple[float, tuple[int, int]]] = []
        heapq.heappush(open_heap, (0.0, start))
        g_cost: dict[tuple[int, int], float] = {start: 0.0}
        parent: dict[tuple[int, int], tuple[int, int]] = {}
        goal = player_pos
        while open_heap:
            cost, current = heapq.heappop(open_heap)
            if (goal != start and current == goal):  # or stop_retreat is True:
                break
            lst_adj = self.get_adj(current, self.map_grid)
            for adj in lst_adj:
                cost_adj = self.get_cost(adj)
                tentative_g = g_cost[current] + cost_adj
                if adj not in g_cost or tentative_g < g_cost[adj]:
                    g_cost[adj] = tentative_g
                    parent[adj] = current
                    heapq.heappush(open_heap, (tentative_g, adj))
        result = self.build_path(current, parent)
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
            result.append(tmp)
            tmp = parents.get(tmp)
        result.reverse()
        return result

    def get_adj(
        self,
        pos: tuple[int, int],
        map_maze: list[list[int]]
    ) -> list[tuple[int, int]]:
        result = []
        line, col = pos
        value = format(map_maze[line][col], '04b')
        if value[0] == '0':
            result.append((line, col - 1))
        if value[1] == '0':
            result.append((line + 1, col))
        if value[2] == '0':
            result.append((line, col + 1))
        if value[3] == '0':
            result.append((line - 1, col))
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
        phantom_pos: tuple[int, int],
        player_pos: tuple[int, int],
        prev_phantom_pos: tuple[int, int] | None = None
    ) -> list[tuple[int, int]]:
        pass
