import sys
import numpy as np

def solve(matrix, results, guess, epsilon=1e-10, max_iterations=500):
    diagonal = np.diag(np.diag(matrix))
    lowerAndUpper =  matrix - diagonal
    diagonalInverse = np.diag(1/np.diag(diagonal))
    for _ in range(max_iterations):
        x = np.dot(diagonalInverse, results - np.dot(lowerAndUpper, guess))
        if np.linalg.norm(x - guess) < epsilon:
            return x
        guess = x
    return guess

def main():
    A = np.array([
        [5, 2, 1, 1],
        [2, 6, 2, 1],
        [1, 2, 7, 1],
        [1, 1, 2, 8]
    ])
    b = np.array([29, 31, 26, 19])
    init = np.zeros(len(b))
    x = solve(A, b, init)
    print("x:", x)
    print("computed b:", np.dot(A, x))
    print("real b:", b)

if __name__ == "__main__":
    main()