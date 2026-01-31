# Abstract
# Types
from typing import Any, List, Optional
from collections import deque

import matplotlib.pyplot as plt

# Libraries
import numpy as np

from environment_state import EnvironmentState

E = (1, 2, 3, 4, 5, 6, 7)


class ConnectState(EnvironmentState):
    def __init__(self, board: Optional[np.ndarray] = None):
        self.state = board
        self.height = len(board)
        self.width = len(board[0])

    def is_final(self) -> bool:
        """See base class."""
        raise NotImplementedError("Method is_final must be implemented.")

    def is_applicable(self, event: Any) -> bool:
        raise NotImplementedError("Method is_applicable must be implemented.")

    def transition(self, col: int) -> "EnvironmentState":
        """See base class."""
        raise NotImplementedError("Method put must be implemented.")

    def get_winner(self) -> int:
        """
        Determines the winner in the current state.

        Returns
        -------
        int
            -1 if red has won, 1 if yellow has won, 0 if no winner.
        """

        print("Executing get winner")
        self.show()

        visited = set()

        for row in range(self.height):
            for col in range(self.width):
                cell_pos = (row, col)
                cell_value = self.state[cell_pos[0]][cell_pos[1]]

                if cell_pos in visited or cell_value == 0:
                    continue

                DIRECTIONS = ((0, 1), (1, 0), (1, 1), (-1, 1))

                for direction in DIRECTIONS:

                    direction_inverse = (direction[0] * -1, direction[1] * -1)

                    direction_val = depth_in_direction(
                        cell_pos, cell_value,
                        direction, self.state, visited)
                    direction_inverse_val = depth_in_direction(
                        cell_pos, cell_value,
                        direction_inverse, self.state, visited)

                    print(f"For direction: {direction} the total val was: {
                        direction_val + direction_inverse_val}")
                    if direction_val + direction_inverse_val >= 4:
                        return cell_value

        return 0

    def is_col_free(self, col: int) -> bool:
        if self.state[0][col] == 0:
            return True
        return False

    def get_heights(self) -> List[int]:
        heights = [self.height for i in range(self.width)]

        for col in range(self.width):
            for row in range(self.height):
                if self.state[row][col] == 0:
                    heights[col] -= 1
                else:
                    break

        return heights

    def get_free_cols(self) -> List[int]:
        free_cools = []
        for col in range(self.width):
            if self.state[0][col] == 0:
                free_cools.append(col)

        return free_cools

    def show(self) -> None:
        symbols = {
            1: "Y",
            -1: "R",
            0: "."
        }

        rows, cols = self.state.shape

        print()
        for r in range(rows):
            for c in range(cols):
                print(symbols[self.state[r, c]], end=" ")
            print()

        print("-" * (2 * cols - 1))
        print(" ".join(str(c) for c in range(cols)))


def depth_in_direction(cell_pos, cell_value, direction, board, visited):
    if (cell_pos[0] < 0 or cell_pos[0] >= len(board)
            or cell_pos[1] < 0 or cell_pos[1] >= len(board[0])
            or board[cell_pos[0]][cell_pos[1]] != cell_value):
        return 0

    cell_pos = (cell_pos[0] + direction[0], cell_pos[1] + direction[1])
    visited.add(cell_pos)

    return depth_in_direction(cell_pos, cell_value, direction, board, visited) + 1


def main():
    cns = ConnectState(np.array([[0 for i in range(7)] for i in range(6)]))
    print(cns.state)
    cns.show()


main()
