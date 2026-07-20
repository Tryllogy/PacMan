from abc import ABC, abstractmethod
import math
import heapq


class Strategy(ABC):
    def __init__(
            self,
            map_grid: list[list[int]],
            name: str
    ):
        """Store the maze grid and the strategy's display name."""
        self.name: str = name
        self.map_grid: list[list[int]] = map_grid

    def get_path(
        self,
        phantom_cell: tuple[int, int],
        goal_cell: tuple[int, int]
    ) -> list[tuple[int, int]]:
        """Return the A* shortest path from ``phantom_cell`` to ``goal_cell``.
        """
        start = phantom_cell
        goal = goal_cell
        open_heap: list[tuple[float, tuple[int, int]]] = []
        heapq.heappush(open_heap, (0.0, start))
        g_cost: dict[tuple[int, int], float] = {start: 0.0}
        parent: dict[tuple[int, int], tuple[int, int]] = {}
        while open_heap:
            cost, current = heapq.heappop(open_heap)
            if (goal != start and current == goal):
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
        cell: tuple[int, int],
        parents: dict[
            tuple[int, int],
            tuple[int, int]]
    ) -> list[tuple[int, int]]:
        """Rebuild the ordered path by walking the ``parents`` chain back."""
        result: list[tuple[int, int]] = []
        tmp = cell
        while tmp in parents:
            result.append(tmp)
            tmp = parents[tmp]
        result.reverse()
        return result

    def get_adj(
        self,
        cell: tuple[int, int],
        map_maze: list[list[int]]
    ) -> list[tuple[int, int]]:
        """Return the neighbouring cells reachable from ``cell`` (no wall)."""
        result = []
        row, col = cell
        value = format(map_maze[row][col], '04b')
        if value[0] == '0':
            result.append((row, col - 1))
        if value[1] == '0':
            result.append((row + 1, col))
        if value[2] == '0':
            result.append((row, col + 1))
        if value[3] == '0':
            result.append((row - 1, col))
        return result

    def get_cost(
        self,
        cell: tuple[int, int]
    ) -> float:
        """Return the step cost of ``cell``, favouring more open corridors."""
        row, col = cell
        value = format(self.map_grid[row][col], '04b')
        n_wall = sum([int(c) for c in value])
        if n_wall == 2:
            return 1.2
        elif n_wall == 1:
            return 1.1
        elif n_wall == 0:
            return 1.0
        return math.inf

    def to_spawn(
        self,
        start_cell: tuple[int, int],
        spawn_cell: tuple[int, int]
    ) -> list[tuple[int, int]]:
        """Return the path from ``start_cell`` back to ``spawn_cell``."""
        return self.get_path(start_cell, spawn_cell)

    @abstractmethod
    def movement(
        self,
        phantom_cell: tuple[int, int],
        player_cell: tuple[int, int],
        prev_phantom_cell: tuple[int, int] | None = None
    ) -> list[tuple[int, int]]:
        """Return the ghost's next path for this frame (subclass-specific)."""
        pass
