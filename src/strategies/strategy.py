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
    def is_away(cls, start: tuple[int, int], current: tuple[int, int]) -> bool:
        par_x, par_y = start
        curr_x, curr_y = current
        play_x, play_y = cls.player_pos
        min_x = min(par_x, play_x)
        max_x = max(par_x, play_x)
        min_y = min(par_y, play_y)
        max_y = max(par_y, play_y)
        range_x = [min_x + i for i in range(max_x - min_x + 1)]
        range_y = [min_y + i for i in range(max_y - min_y + 1)]
        # if curr_x not in range_x or curr_y not in range_y:
        # print("start", (par_x, par_y))
        # print("current", (curr_x, curr_y))
        # print("player", cls.player_pos)
        # print("range x", range_x)
        # print("range y", range_y)
        if (curr_y not in range_y) ^ (curr_x not in range_x):
            # print('result', True)
            return True
        # print('result', False)
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
        i = 0
        while open_heap:
            i += 1
            cost, current = heapq.heappop(open_heap)
            if (goal != start and current == goal):  # or stop_retreat is True:
                break
            lst_adj = self.get_adj(current, self.map_grid)
            # print(f"============={i}")
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
                    heapq.heappush(open_heap, (tentative_g, adj))
                    if strat == 'retreat' and Strategy.is_away(start, adj) and not stop_retreat:
                        # stop_retreat = True
                        goal = adj
            # print("current", current)
            # print("adj", lst_adj)
            if strat == 'retreat':
                break
        #  if any de lst adj not, return none et reste sur place puis reactualise
        print(parent.get(current))
        result = self.build_path(current, parent)
        if result[0] == start:
            result.pop(0)
        if not stop_retreat:
            result.append(goal)
            return result
        else:
            # result = self.build_path(goal, parent)
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
        i = 0
        print("DICT PARENT = ", parents)
        while parents.get(tmp) is not None:
            tmp = parents.get(tmp)
            print(f"REBUILD {i} = {tmp}")
            i += 1
            result.append(tmp)
        result.reverse()
        print(f"FINAL RESULT (reversed) {result}")
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
