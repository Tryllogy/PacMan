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
        cell: tuple[int, int],
        parents: dict[
            tuple[int, int],
            tuple[int, int]]
    ) -> list[tuple[int, int]]:
        result = [cell]
        tmp = cell
        rev_parents = {v: k for k, v in parents.items()}
        while tmp in rev_parents:
            tmp = rev_parents[tmp]
            result.append(tmp)
        return result

    def is_away(
        cls,
        start_cell: tuple[int, int],
        current_cell: tuple[int, int],
        player_cell: tuple[int, int]
    ) -> bool:
        start_row, start_col = start_cell
        curr_row, curr_col = current_cell
        play_row, play_col = player_cell
        min_row = min(start_row, play_row)
        max_row = max(start_row, play_row)
        min_col = min(start_col, play_col)
        max_col = max(start_col, play_col)
        range_rows = [min_row + i for i in range(max_row - min_row + 1)]
        range_cols = [min_col + i for i in range(max_col - min_col + 1)]
        if curr_col not in range_cols or curr_row not in range_rows:
            return True
        return False

    def retreat_step(
        self,
        phantom_cell: tuple[int, int],
        player_cell: tuple[int, int],
        prev_phantom_cell: tuple[int, int] | None
    ) -> list[tuple[int, int]]:
        lst_adj = self.get_adj(phantom_cell, self.map_grid)
        for adj in lst_adj:
            if self.is_away(phantom_cell, adj, player_cell):
                return [adj]
        if len(lst_adj) > 1 and prev_phantom_cell in lst_adj:
            lst_adj.remove(prev_phantom_cell)
        if not lst_adj:
            return [phantom_cell]
        return [random.choice(lst_adj)]

    def movement(
        self,
        phantom_cell: tuple[int, int],
        player_cell: tuple[int, int],
        prev_phantom_cell: tuple[int, int] | None = None
    ) -> list[tuple[int, int]]:
        return self.retreat_step(phantom_cell, player_cell, prev_phantom_cell)
