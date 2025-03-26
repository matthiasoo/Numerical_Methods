import numpy as np

def rank(matrix) :
    R = matrix.shape[0]
    rank = 0
    reducedMatrix = gauss(matrix)
    print(reducedMatrix)

    for i in range(R):
        if not np.all(reducedMatrix[i] == 0):
            rank += 1

    return rank

def gauss(matrix) :
    R = matrix.shape[0]
    p = 0 # pivot

    # macierz trójkątna
    while p < R :
        if matrix[p][p] == 0 :
            for i in range(p+1, R) :
                if matrix[i][p] != 0 :
                    matrix[[p, i]] = matrix[[i, p]]
                    i = R

        for i in range(p+1, R) :
            multiplier = matrix[i][p] / matrix[p][p]
            matrix[i] -= (multiplier * matrix[p])
            # print(matrix)

        p += 1

    return matrix

def solve(matrixX) :
    R = matrixX.shape[0]
    x = np.zeros(R)
    matrix = gauss(matrixX)

    x[R-1] = matrix[R-1][R] / matrix[R-1][R-1]

    for i in range(R-2, -1, -1) :
        x[i] = matrix[i][R]

        for j in range(i + 1, R) :
            x[i] -= matrix[i][j] * x[j]

        x[i] /= matrix[i][i]

    return x

# TODO walidacja

def main() :
    matrixA = np.array([
        [3, 3, 1],
        [2, 5, 7],
        [1, 2, 1]
    ], dtype=float)

    matrixB = np.array([
        [12],
        [33],
        [8]
    ], dtype=float)

    matrixAB = np.concatenate((matrixA, matrixB), axis=1)
    count = matrixA.shape[0]
    rankA = rank(matrixA)
    rankAB = rank(matrixAB)

    # TODO walidacja

    if rankA != rankAB :
        print("Układ równań liniowych jest sprzeczny")
        return
    elif rankAB < count :
        print(f"Układ równań liniowych jest nieoznaczony (rozwiązania układu zależą od liczby parametrów równej {count - rankA})")
    else :
        xs = solve(matrixAB)
        print("Rozwiązania:")
        for i in range(count):
            print(f"x{i} = {xs[i]}")

main()