from liealg import Lie
def g6(p):
    br = {(0, 1): {2: 1}, (0, 2): {3: 1}, (0, 3): {4: 1}, (0, 4): {5: 1},
          (1, 2): {4: 1}, (1, 3): {5: 1}, (1, 4): {5: -1}, (2, 3): {5: 1}}
    return Lie.from_dict(6, p, br)
def five(p):
    br = {(0, 1): {2: 1}, (0, 2): {3: 1}, (0, 3): {4: 1}, (1, 2): {4: 1}}
    return Lie.from_dict(5, p, br)
def filiform(m, p):
    br = {(0, i): {i + 1: 1} for i in range(1, m - 1)}
    return Lie.from_dict(m, p, br)
def heis(p):
    return Lie.from_dict(3, p, {(0, 1): {2: 1}})
