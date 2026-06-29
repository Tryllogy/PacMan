from base_strategy import Strategy
from utils import reverse, get_adj
from collections import deque


class RetreatStrategy(Strategy):
    def __init__(
            self,
            map_grid: list[list[int]],
            name: str = "Retreat"
    ) -> None:
        super().__init__(name)
        self.map_grid = reverse(map_grid)

    def build_rev_path(
            self,
            pos: tuple[int, int],
            parents: dict[
                tuple[int, int],
                tuple[int, int]]
            ) -> list[tuple[int, int]]:
        result = []
        tmp = pos
        rev_parents = {v: k for k, v in parents.items()}
        while rev_parents.get(tmp) is not None:
            tmp = rev_parents.get(tmp)
            result.append(tmp)
        return result

    def get_path(
            self,
            player: tuple[int, int],
            current: tuple[int, int]
            ) -> list[tuple[int, int]]:
        width = len(self.map_grid)
        heigh = len(self.map_grid[0])
        x, y = player
        visited = [[False] * heigh for i in range(width)]
        visited[x][y] = True
        q = deque()
        q.append(player)
        result = []
        parents = {}

        while q:
            curr = q.popleft()
            result.append(curr)
            lst_adj = get_adj(curr, self.map_grid)
            for adj in lst_adj:
                x, y = adj
                if not visited[x][y]:
                    parents.update({adj: curr})
                    visited[x][y] = True
                    q.append(adj)
        result = self.build_rev_path(current, parents)
        return result

    # Will go away as far as possible from the player
    def mouvement(self):
        pass


if __name__ == '__main__':
    map_grid = [[13, 3, 9, 1, 3], [11, 10, 10, 10, 10], [10, 10, 14, 8, 2], [8, 2, 9, 6, 10], [12, 4, 4, 5, 6]]
    ret = RetreatStrategy(map_grid)
    print(ret.get_path((0, 0), (2, 4)))
