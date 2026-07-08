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

    @classmethod
    def set_player_pos(cls, pos: tuple[int, int]) -> None:
        cls.player_pos = pos

    @classmethod
    def set_rand_pos(cls, pos: tuple[int, int]) -> None:
        cls.rand_pos = pos

    @classmethod
    def is_away(cls, parent: tuple[int, int], current: tuple[int, int]) -> bool:
        par_x, par_y = parent
        curr_x, curr_y = current
        play_x, play_y = cls.player_pos
        min_x = min(par_x, play_x)
        max_x = max(par_x, play_x)
        min_y = min(par_y, play_y)
        max_y = max(par_y, play_y)
        range_x = [min_x + i for i in range(0, max_x - min_x)]
        range_y = [min_y + i for i in range(max_y - min_y)]
        if curr_x not in range_x:
            return True
        elif curr_y not in range_y:
            return True
        return False

    def get_path(
        self,
        start: tuple[int, int],
        strat: str
    ) -> list[tuple[int, int]]:
        open_heap: list[tuple[float, tuple[int, int]]] = []
        heapq.heappush(open_heap, (0.0, start))
        g_cost: dict[tuple[int, int], float] = {start: 0.0}
        parent: dict[tuple[int, int], tuple[int, int]] = {}
        goal = start
        if strat == 'aggro':
            goal = Strategy.player_pos
        elif strat == 'rand':
            goal = Strategy.rand_pos
        stop_retreat = False
        visited = [[False] * len(self.map_grid) for i in range(len(self.map_grid[0]))]
        visited[start[0]][start[1]] = True
        tmp = start
        while open_heap:
            cost, current = heapq.heappop(open_heap)
            if (goal != start and current == goal) or stop_retreat is True:
                break
            lst_adj = self.get_adj(current, self.map_grid)
            for adj in lst_adj:
                # if tmp != start and tmp == adj:
                #     print("test")
                #     continue
                cost_adj = self.get_cost(adj)
                tentative_g = g_cost[current] + cost_adj
                if (adj not in g_cost or tentative_g < g_cost[adj]) or not visited[adj[0]][adj[1]]:
                    visited[adj[0]][adj[1]] = True
                    g_cost[adj] = tentative_g
                    parent[adj] = current
                    if strat == 'retreat' and Strategy.is_away(start, current):
                        stop_retreat = True
                        break
                    heapq.heappush(open_heap, (tentative_g, adj))
            tmp = current
        result = self.build_path(current, parent)
        if goal != start:
            result.append(goal)
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
        start: tuple[int, int]
    ) -> list[tuple[int, int]]:
        pass
