from connect_state import ConnectState
import numpy as np


def test_get_height():
    cns = ConnectState(np.array([[0 for i in range(7)] for i in range(6)]))
    assert cns.get_heights() == [0 for i in range(cns.width)]

    for i in range(cns.width):
        cns.state[cns.height - 1][i] = 1
    assert cns.get_heights() == [1 for i in range(cns.width)]

    cns.state[cns.height - 2][0] = -1
    cns.state[cns.height - 3][0] = -1
    assert cns.get_heights() == [3, *[1 for i in range(cns.width - 1)]]


def test_free_cols():
    cns = ConnectState(np.array([[0 for i in range(7)] for i in range(6)]))
    assert cns.get_free_cols() == [i for i in range(cns.width)]

    cns = ConnectState(np.array([[1 for i in range(7)] for i in range(6)]))
    assert cns.get_free_cols() == []

    cns.state[0][0] = 0
    cns.state[0][2] = 0
    assert cns.get_free_cols() == [0, 2]


def test_is_col_free():
    cns = ConnectState(np.array([[0 for i in range(7)] for i in range(6)]))
    for col in range(cns.width):
        assert cns.is_col_free(col)

    cns = ConnectState(np.array([[1 for i in range(7)] for i in range(6)]))
    for col in range(cns.width):
        assert not cns.is_col_free(col)

    cns.state[0][0] = 0
    cns.state[0][2] = 0
    assert cns.is_col_free(0)
    assert cns.is_col_free(2)

    assert not cns.is_col_free(1)
    assert not cns.is_col_free(3)


def test_get_winner():
    cns = ConnectState(np.array([[0 for i in range(7)] for i in range(6)]))
    assert cns.get_winner() == 0

    # Diagonal (\) check

    cns = ConnectState(np.array([[0 for i in range(7)] for i in range(6)]))
    for i in range(4):
        cns.state[i][i] = 1
    assert cns.get_winner() == 1

    cns = ConnectState(np.array([[0 for i in range(7)] for i in range(6)]))
    for i in range(4):
        cns.state[i][i] = -1
    assert cns.get_winner() == -1

    # Diagonal (/) check

    cns = ConnectState(np.array([[0 for i in range(7)] for i in range(6)]))
    for i in range(4):
        cns.state[cns.height - 1 - i][i] = -1
    assert cns.get_winner() == -1

    # Horizontal (-) check

    cns = ConnectState(np.array([[0 for i in range(7)] for i in range(6)]))
    for i in range(4):
        cns.state[cns.height - 1][i] = 1
    assert cns.get_winner() == 1

    cns = ConnectState(np.array([[0 for i in range(7)] for i in range(6)]))
    for i in range(3):
        cns.state[cns.height - 1][i] = 1
    assert cns.get_winner() == 0

    # Vertical (|) check

    cns = ConnectState(np.array([[0 for i in range(7)] for i in range(6)]))
    for i in range(4):
        cns.state[i][cns.width // 2] = -1
    assert cns.get_winner() == -1

    # Full board check

    cns = ConnectState(np.array([[1 for i in range(7)] for i in range(6)]))
    assert cns.get_winner() == 1

    cns = ConnectState(np.array([[-1 for i in range(7)] for i in range(6)]))
    assert cns.get_winner() == -1

    # Custom array check

    board = np.array([
        [0, 0, -1, 0, 0, -1, 0],
        [0, 0,  0, 1, 1,  1, 1],
        [0, 0,  0, 0, 0,  0, 0],
        [0, 0,  0, 0, 0,  0, 0],
        [0, 0,  0, 0, 0,  0, 0],
        [0, 0,  0, 0, 0,  0, 0],
    ])

    cns = ConnectState(board)
    assert cns.get_winner() == 1


def test_transition():
    cns = ConnectState(np.array([[0 for i in range(7)] for i in range(6)]))

    cns.show()
    cns = cns.transition(0)
    cns.show()
    assert cns.state[cns.height - 1][0] == 1
    assert cns.state[cns.height - 2][0] == 0

    cns = cns.transition(0)
    cns.show()
    assert cns.state[cns.height - 2][0] == -1
    assert cns.state[cns.height - 3][0] == 0

    cns = cns.transition(2)
    cns.show()
    assert cns.state[cns.height - 1][2] == 1
