#импортируем встроенные библиотеки
import math
import numpy as np

#функция для подсчёта альфа, бета и гамма
#принимает на вход обработанную матрицу
def alphabet(matrix):
    matrix_len = len(matrix)
    alpha_mas = [0] * matrix_len
    beta_mas = [0] * matrix_len
    gamma = 0
    for i in range(matrix_len):
        for j in range(matrix_len):
            gamma += matrix[i][j] ** 2
            alpha_mas[i] += abs(matrix[i][j])
            beta_mas[j] += abs(matrix[i][j])

    alpha = max(alpha_mas)
    beta = max(beta_mas)
    return (alpha, beta, gamma)

#функция, вычисляющая необходимое количество итераций
#принимает на вход коэффициенты (альфа, бета, гамма), x1, то есть вектор b и точность, с которой требуется вычислить корни
def iterations_number(tpl, x1, epsilon):
    space = tpl.index(min(tpl))
    p = 0
    #если альфа меньше всего, то пространство R_n бесконечность
    if space == 0:
        tmp = []
        for i in x1:
            tmp.append(abs(i))
        p = max(tmp)
    # если бета меньше всего, то пространство R^1_n
    elif space == 1:
        for i in x1:
            p += abs(i)

    # если гамма меньше всего, то пространство R^2_n
    elif space == 2:
        for i in x1:
            p += i ** 2
        p = math.sqrt(p)

    number = math.log((epsilon * (1 - tpl[space])) / p, tpl[space])
    return int(number) + 1

#Функция, которая проделывает итерации, принимает на вход матрицу коэффициентов(свободные коэффицинты и при иксах вместе)
# и точность вычислений
def SimpleIterationMethod(matrix, epsilon):
    #блок кода, меняющий местами строки матрицы, если требуется
    matrix_len = len(matrix)
    tmp = [None] * matrix_len
    for i in range(matrix_len):
        tmp[i] = [abs(elem) for elem in matrix[i]]
    tmp2 = [None] * matrix_len
    for i in range(len(matrix)):
        tmp3 = tmp[i][:matrix_len]
        tmp2[tmp[i].index(max(tmp3))] = matrix[i]

    # приводим к виду x = Ax + b
    A = []
    for i in range(matrix_len):
        A.append([])
        for j in range(matrix_len + 1):
            if i == j:
                A[i].append(0)
            else:
                A[i].append(tmp2[i][j] / tmp2[i][i])
    mas = []
    x = []
    for line in A:
        mas.append([-elem for elem in line[:len(line) - 1]])
        x.append(line[len(line) - 1])
    mas_np = np.matrix(mas)
    b = np.matrix(x).transpose()
    x_np = b[:]

    #если вектор свободных коэффициентов нулевой, то решения нулевые и только
    flag = True
    for i in x:
        if i != 0:
            flag = False
    if flag:
        return [0] * len(x)
    #проводим итерации на две больше для уверенности
    for i in range(iterations_number(alphabet(mas), x, epsilon) + 1):
        x_np = mas_np * x_np + b
    answer = [0] * len(x_np)
    for i in range(len(x_np)):
        answer[i] += float(x_np[i][0])
    return answer

print("Введите количество уравнений")
N = int(input())
print("Введите требуемую точность")
e = float(input())
print("Введите матрицу построчно")
matrix = []
for i in range(N):
    matrix.append([float(elem) for elem in input().split()])

print(SimpleIterationMethod(matrix, e))
input("Для завершения работы нажмите Enter")


'''3
0.01
5 0.2 -0.7 1
1 3.8 -1.5 -1
1 -1 7.3 0'''

"""3
0.00000000000000000000001
-4 1 2 20
-1 5 3 5
-1 2 5 10"""

"""3
0.0001
1.1 5.3 2 3
9.8 6.2 -0.7 21
2.6 0.9 10 17"""
"""[2.4458613215714275, -0.3551952278342634, 1.0960436268965124]"""

"""4
0.0001
3 0.1 -0.2 2 100
-0.1 23 4.103 -6.48 22.8
9 32 -0.1 100 2
3 2 10 1 0"""

"""5
0.0001
7 44 2 1 5 3
10 2 3 1 2 100
10 133 2 22 1000 1
22 3 441 89 1 90
9 2 4 432 1 98
"""
"""
4
0.0001
53 0.01 244 2 0
22 1 3 0.32 -1
-67 -787 77 65 81
1 2 3 123 123123
"""