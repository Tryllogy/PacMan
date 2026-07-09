from .strategy import Strategy
import random


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

    def is_away(cls, start: tuple[int, int], current: tuple[int, int], player_pos: tuple[int, int]) -> bool:
        par_x, par_y = start
        curr_x, curr_y = current
        play_x, play_y = player_pos
        min_x = min(par_x, play_x)
        max_x = max(par_x, play_x)
        min_y = min(par_y, play_y)
        max_y = max(par_y, play_y)
        range_x = [min_x + i for i in range(max_x - min_x + 1)]
        range_y = [min_y + i for i in range(max_y - min_y + 1)]
        if curr_y not in range_y or curr_x not in range_x:
            return True
        return False

    def get_path(
        self,
        phantom_pos: tuple[int, int],
        player_pos: tuple[int, int],
        prev_phantom_pos: tuple[int, int]
    ) -> list[tuple[int, int]]:
        lst_adj = self.get_adj(phantom_pos, self.map_grid)
        for adj in lst_adj:
            if self.is_away(phantom_pos, adj, player_pos):
                return [adj]
        if len(lst_adj) > 1:
            lst_adj.pop(lst_adj.index(prev_phantom_pos))
        return [random.choice(lst_adj)]

    # Will go away as far as possible from the player
    def movement(
        self,
        phantom_pos: tuple[int, int],
        player_pos: tuple[int, int],
        prev_phantom_pos: tuple[int, int] | None = None
    ) -> list[tuple[int, int]]:
        return self.get_path(phantom_pos, player_pos, prev_phantom_pos)
