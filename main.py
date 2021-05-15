import math
import matplotlib.pyplot as plt
import numpy as np
from numpy import genfromtxt
from tabulate import tabulate
from termcolor import cprint


##############################
#       APPROXIMATION        #
##############################
def parse():
    print('\nВведите путь к файлу:')
    a = genfromtxt(input(), delimiter=',')
    return a


def equation():
    print("\nВыберите уравнение:\n"
          "\t1. sin(x)\n"
          "\t2. sqrt(x)\n"
          "\t3. x^3 + x^2 + 3\n"
          "\t4. e^x\n")
    method = int(input())
    cprint("\nВыберите границу (через пробел):")
    borders = list(input().split(" "))
    a = float(borders[0].strip())
    b = float(borders[1].strip())
    print("\nКоличество точек интерполирования: ")
    number_of_data = int(input())
    x = np.linspace(a, b, number_of_data)
    data = []
    if method == 1:
        for i in range(number_of_data):
            data.append([x[i], math.sin(x[i])])
    elif method == 2:
        for i in range(number_of_data):
            data.append([x[i], math.sqrt(x[i])])
    elif method == 3:
        for i in range(number_of_data):
            data.append([x[i], math.pow(x[i], 3) + math.pow(x[i], 2) + 3])
    elif method == 4:
        for i in range(number_of_data):
            data.append([x[i], math.pow(math.e, x[i])])
    return np.array(data).transpose()


def write_values():
    print('\nВведите количество значений: ')
    n = int(input())
    a = []
    for i in range(n):
        print('\nВведите x: ')
        x = float(input())
        print('Введите y: ')
        y = float(input())
        a.append([x, y])
    return np.array(a).transpose()


def check_and_draw(x, y, approximate_function, title, point):
    fig, ax = plt.subplots()
    xnew = np.linspace(np.min(x), np.max(x), 100)
    ynew = [approximate_function(x, y, i)[0] for i in xnew]
    plt.plot(x, y, 'o', color='r', label='input data')
    plt.plot(xnew, ynew, color='b', label='approximate function')
    plt.plot(point[0], point[1], '*', color='g', markersize=12, label='answer')
    plt.title(title)
    ax.legend()
    plt.grid(True)
    plt.show()


##############################
#          LAGRANGE          #
##############################
def lagrange(array_x, array_y, cur_x):
    array_x.astype(float)
    array_y.astype(float)
    lag = 0
    lagrangians = []
    for j in range(len(array_y)):
        multiplying = 1
        for i in range(len(array_x)):
            if i != j:
                multiplying *= (cur_x - array_x[i]) / (array_x[j] - array_x[i])
        lagrangians.append(array_y[j] * multiplying)
        lag += array_y[j] * multiplying
    return lag, lagrangians


##############################
#           NEWTON           #
##############################
def newton_matrix(array_y):
    n = len(array_y)
    res_arr = [[0] * n for i in range(n)]
    res_arr[0] = array_y
    for i in range(1, len(array_y)):
        for j in range(0, len(array_y) - i):
            res_arr[i][j] = res_arr[i - 1][j + 1] - res_arr[i - 1][j]
    '''
    for i in range(len(array_y)):
        for j in range(len(array_y)):
            print(str(res_arr[i][j]) + ' ', end='')
        print()
    '''
    return res_arr


def newton_polynomial(array_x, array_y, cur_x):
    n = len(array_x)
    nm = newton_matrix(array_y)
    Nn = 0
    h = array_x[1] - array_x[0]
    if x < (array_x[n - 1] + array_x[0]) / 2:
        i = 0
        while x > array_x[i]:
            i += 1
        i -= 1
        t = (cur_x - array_x[i]) / h
        counter = 1
        z = 0
        for j in range(0, len(nm[i])):
            Nn += nm[j][i] * counter / math.factorial(j)
            counter *= (t - z)
            z += 1
    else:
        i = n - 1
        while x < array_x[i]:
            i -= 1
        i += 1
        t = (cur_x - array_x[i]) / h
        counter = 1
        z = 0
        for j in range(0, len(nm[i])):
            if (i - j >= 0):
                Nn += nm[j][i-j] * counter / math.factorial(j)
            counter *= (t + z)
            z += 1
    return Nn, None


##############################
#            MAIN            #
##############################
print('Выберите, введете ли вы данные или будете использовать готовые уравнения (да/нет):')
if input() == 'да':
    print('\nВвод с клавиатуры или с файла? (да/нет):')
    if input() == 'да':
        data = write_values()
    else:
        data = parse()
else:
    data = equation()
print('\nДанные:')
cprint(tabulate(data, tablefmt="fancy_grid", floatfmt="2.5f"))
print('\nВведите число, которое хотите интерполировать: ')
x = float(input())
if (x > data[0][0] and x < data[0][len(data[0]) - 1]):
    lag, lagrangians = lagrange(data[0], data[1], x)
    print('\nМетодом Лагранжа: ' + str(lag))
    check_and_draw(data[0], data[1], lagrange, 'LAGRANGE', [x, lag])

    dr = newton_polynomial(data[0], data[1], x)[0]
    print('\nМетодом Ньютона: ' + str(dr))
    check_and_draw(data[0], data[1], newton_polynomial, 'NEWTON', [x, dr])
else:
    cprint('\nНеправильный промежуток', color='red')
