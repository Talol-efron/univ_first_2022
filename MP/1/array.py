from numpy.linalg import solve

left = [[2, 8, 4],
        [6, 4,  6],
        [2,3,8]]

right = [12, 24, 20]

print(solve(left, right))
