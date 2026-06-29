from .base_strategy import Strategy
from .utils import reverse, get_adj
import heapq
import math


class AggressiveStrategy(Strategy):
    def __init__(
            self,
            map_grid: list[list[int]],
            name: str = "Aggressive"
    ) -> None:
        super().__init__(name)
        self.map_grid = reverse(map_grid)

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

    def get_cost(self, case: tuple[int, int]) -> float:
        x, y = case
        value = format(self.map_grid[x][y], '04b')
        n_wall = sum([int(c) for c in value])
        if n_wall == 3:
            return math.inf
        elif n_wall == 2:
            return 1.2
        elif n_wall == 1:
            return 1.1
        elif n_wall == 0:
            return 1.0

    def get_path(
            self,
            start: tuple[int, int],
            goal: tuple[int, int] | None = None) -> list[tuple[int, int]]:
        open_heap: list[tuple[float, tuple[int, int]]] = []
        heapq.heappush(open_heap, (0.0, start))
        g_cost: dict[tuple[int, int], float] = {start: 0.0}
        parent: dict[tuple[int, int], tuple[int, int]] = {}
        while open_heap:
            _, current = heapq.heappop(open_heap)
            if current == goal:
                break
            lst_adj = get_adj(current, self.map_grid)
            for adj in lst_adj:
                cost_adj = self.get_cost(adj)
                tentative_g = g_cost[current] + cost_adj
                if (adj not in g_cost or tentative_g < g_cost[adj]):
                    g_cost[adj] = tentative_g
                    parent[adj] = current
                    heapq.heappush(open_heap, (adj, adj))
        result = self.build_path(current, parent)
        return result

    # Will follow the player everytime
    def mouvement(self):
        pass


if __name__ == '__main__':
    map_grid = [[13, 3, 9, 1, 3], [11, 10, 10, 10, 10], [10, 10, 14, 8, 2], [8, 2, 9, 6, 10], [12, 4, 4, 5, 6]]
    aggro = AggressiveStrategy(map_grid)
    print(aggro.get_path((0, 0), (4, 4)))