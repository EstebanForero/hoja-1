# Abstract
# Types
from typing import Any, List, Optional

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
        """See base class."""
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
        raise NotImplementedError("Method get_winner must be implemented.")

    def is_col_free(self, col: int) -> bool:
        """
        Checks if a tile can be placed in the specified column.

        Parameters
        ----------
        col : int
            Index of the column.

        Returns
        -------
        bool
            True if the column has space for a tile; False otherwise.
        """
        raise NotImplementedError("Method is_col_free must be implemented.")

    def get_heights(self) -> List[int]:
        """
        Gets the number of tiles placed in each column.

        Returns
        -------
        List[int]
            A list of integers indicating the number of tiles per column.
        """

        heights = [self.height for i in range(self.width)]

        for col in range(self.width):
            for row in range(self.height):
                if self.state[row][col] == 0:
                    heights[col] -= 1
                else:
                    break

        return heights

    def get_free_cols(self) -> List[int]:
        """
        Gets the list of columns where a tile can still be placed.

        Returns
        -------
        List[int]
            Indices of columns with at least one free cell.
        """
        raise NotImplementedError("Method get_free_cols must be implemented.")

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


def main():
    cns = ConnectState(np.array([[0 for i in range(7)] for i in range(6)]))
    print(cns.state)
    cns.show()


main()
