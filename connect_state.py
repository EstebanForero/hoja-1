# Abstract
# Types
from typing import Any, List, Optional
# Libraries
import numpy as np

from environment_state import EnvironmentState


class ConnectState(EnvironmentState):
    def __init__(self, board: Optional[np.ndarray] = None):
        if board is None:
            board = np.array([[0 for i in range(7)] for i in range(6)])

        self.board = board
        self.height = len(board)
        self.width = len(board[0])

    def is_final(self) -> bool:
        if len(self.get_free_cols()) == 0 or self.get_winner() != 0:
            return True

        return False

    def is_applicable(self, event: Any) -> bool:
        if not self.is_col_free(event):
            return False
        return True

    def transition(self, event: int) -> "EnvironmentState":
        if not self.is_applicable(event):
            raise ValueError("Invalid move")

        board = self.board.copy()

        num_located_tiles = sum(self.get_heights())
        player = -1 if num_located_tiles % 2 == 0 else 1

        for row in range(self.height):
            if board[self.height - 1 - row][event] == 0:
                board[self.height - 1 - row][event] = player
                break

        return ConnectState(board)

    def get_winner(self) -> int:
        visited = set()

        for row in range(self.height):
            for col in range(self.width):
                cell_pos = (row, col)
                cell_value = self.board[cell_pos[0]][cell_pos[1]]

                if cell_pos in visited or cell_value == 0:
                    continue

                DIRECTIONS = ((0, 1), (1, 0), (1, 1), (-1, 1))

                for direction in DIRECTIONS:

                    direction_inverse = (direction[0] * -1, direction[1] * -1)

                    direction_val = depth_in_direction(
                        cell_pos, cell_value,
                        direction, self.board, visited) - 1
                    direction_inverse_val = depth_in_direction(
                        cell_pos, cell_value,
                        direction_inverse, self.board, visited)

                    if direction_val + direction_inverse_val >= 4:
                        return cell_value

        return 0

    def is_col_free(self, col: int) -> bool:
        if self.board[0][col] == 0:
            return True
        return False

    def get_heights(self) -> List[int]:
        heights = [self.height for i in range(self.width)]

        for col in range(self.width):
            for row in range(self.height):
                if self.board[row][col] == 0:
                    heights[col] -= 1
                else:
                    break

        return heights

    def get_free_cols(self) -> List[int]:
        free_cools = []
        for col in range(self.width):
            if self.board[0][col] == 0:
                free_cools.append(col)

        return free_cools

    def show(self) -> None:
        symbols = {
            1: "Y",
            -1: "R",
            0: "."
        }

        rows, cols = self.board.shape

        print()
        for r in range(rows):
            for c in range(cols):
                print(symbols[self.board[r, c]], end=" ")
            print()

        print("-" * (2 * cols - 1))
        print(" ".join(str(c) for c in range(cols)))


def depth_in_direction(cell_pos, cell_value, direction, board, visited):
    if (cell_pos[0] < 0 or cell_pos[0] >= len(board)
            or cell_pos[1] < 0 or cell_pos[1] >= len(board[0])
            or board[cell_pos[0]][cell_pos[1]] != cell_value):
        return 0

    visited.add(cell_pos)
    cell_pos = (cell_pos[0] + direction[0], cell_pos[1] + direction[1])

    return depth_in_direction(cell_pos, cell_value, direction, board, visited) + 1


def main():
    state = ConnectState(np.array([[0 for i in range(7)] for i in range(6)]))

    while not state.is_final():
        state.show()
        event = int(input("event (1-7): "))
        if state.is_applicable(event):
            state = state.transition(event)
        else:
            print("Invalid event")

    print("Final reached, the winner is: ", state.get_winner())


if __name__ == "__main__":
    main()
