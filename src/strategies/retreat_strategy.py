from .strategy import Strategy
from collections import deque


class RetreatStrategy(Strategy):
    def __init__(
        self,
        map_grid: list[list[int]],
        name: str = "Retreat"
    ) -> None:
        super().__init__(map_grid=map_grid, name=name)

    def build_path(
        self,
        pos: tuple[int, int],
        parents: dict[
            tuple[int, int],
            tuple[int, int]]
    ) -> list[tuple[int, int]]:
        result = [pos]
        tmp = pos
        rev_parents = {v: k for k, v in parents.items()}
        while rev_parents.get(tmp) is not None:
            tmp = rev_parents.get(tmp)
            result.append(tmp)
        return result

    def get_path(
        self,
        start: tuple[int, int],
        goal: tuple[int, int]
    ) -> list[tuple[int, int]]:
        width = len(self.map_grid)
        heigh = len(self.map_grid[0])
        x, y = goal
        visited = [[False] * heigh for i in range(width)]
        visited[x][y] = True
        q = deque()
        q.append(goal)
        result = []
        parents = {}
        while q:
            curr = q.popleft()
            result.append(curr)
            lst_adj = self.get_adj(curr, self.map_grid)
            for adj in lst_adj:
                x, y = adj
                if not visited[x][y]:
                    parents.update({adj: curr})
                    visited[x][y] = True
                    q.append(adj)
        result = self.build_path(start, parents)
        return result

    # Will go away as far as possible from the player
    def movement(
        self,
        start: tuple[int, int],
        goal: tuple[int, int]
    ) -> list[tuple[int, int]]:
        return self.get_path(start, goal)
