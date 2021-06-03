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
def interpolateForward(t, differencesByOrder, order, previous):
    valueY = differencesByOrder[0][previous]
    print("Строка: ", str(previous + 1))
    for i in range(1, order):
        valueY += ((t / math.factorial(i)) * differencesByOrder[i][previous])
        t *= (t - i)
    return valueY


def interpolateBackward(t, differencesByOrder, order):
    valueY = differencesByOrder[0][order];
    print("Строка: ", str(order + 1))
    for i in range(1, order):
        valueY += (t / math.factorial(i)) * differencesByOrder[i][order - i]
        t *= (t + i);
    return valueY;


def newton_polynomial(array_x, array_y, cur_x):
    m = len(array_x)
    array_x.astype(float)
    array_y.astype(float)
    array_x = np.copy(array_x)
    array_y = np.copy(array_y)

    previous = 0

    for i in range(len(array_x) - 1):
        if (cur_x >= array_x[i] and array_x[i + 1] >= cur_x):
            previous = i
            break
    if (cur_x >= array_x[-1]):
        previous = len(array_x) - 1

    differencesByOrder = list()
    order = 0

    y_i = list()
    for i in range(len(array_y)):
        y_i.append(array_y[i])

    differencesByOrder.append(y_i)

    while order < len(array_y) - 1:
        order += 1
        delta_Y = list()
        previous_delta_Y = differencesByOrder[order - 1]
        for i in range(len((previous_delta_Y)) - 1):
            delta_Y.append(previous_delta_Y[i + 1] - previous_delta_Y[i])
        differencesByOrder.append(delta_Y)

    if (previous < len(array_x) / 2):
        t = (cur_x - array_x[previous]) / (array_x[1] - array_x[0])
        return interpolateForward(t, differencesByOrder, (len(array_y) - previous - 1), previous), None
    else:
        if (previous == (len(array_x) - 1)):
            next = previous
        else:
            next = previous + 1
        t = (cur_x - array_x[next]) / (array_x[1] - array_x[0])
        return interpolateBackward(t, differencesByOrder, next), None


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
