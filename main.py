import random

import scipy.stats as sps
import numpy as np
import matplotlib.pyplot as plt


class Target:
    def __init__(self):
        self.__complexity = 10
        self.__isReady = False
        self.__Nmax = random.randint(1, 3)
        self.__Executors = np.array([], dtype='object')

    def changeComplexity(self, performance):
        self.__complexity = self.__complexity - performance

    def getComplexity(self):
        return self.__complexity

    def getNmax(self):
        return self.__Nmax

    def isOverflow(self):
        if self.__Executors.size < self.__Nmax:
            return False
        else:
            return True

    def setExecutor(self, robot):
        if self.isReady():
            print("Задача уже выполнена")
        if not self.isOverflow():
            self.__Executors = np.append(self.__Executors, robot)

    def getExecutors(self):
        return self.__Executors

    def isReady(self):
        return self.__isReady


class Robot:
    def __init__(self, numberOfTargets):
        self.__powerD = np.array([random.random() for i in range(numberOfTargets)])
        self.__free = True
        self.__target = None

    def setTarget(self, target):
        if self.__target is None:
            self.__target = target
            self.setEmployment()

    def isFree(self):
        return self.__free

    def getPower(self):
        return self.__powerD

    def setEmployment(self):
        self.__free = not self.__free

    def getTarget(self):
        return self.__target


def algorithm():
    targets = np.array([Target() for i in range(random.randint(1, 10))]) # Создаём цели от 1 до 10
    robots = np.array([Robot(len(targets)) for i in range(random.randint(1, 10))]) # Создаём роботов от 1 до 10
    D = np.vstack([i.getPower() for i in robots]) # Получаем общую матрицу эффективности роботов над задачами
    Nmax = np.array([i.getNmax() for i in targets]) # Получаем общий вектор максимально возможного количества роботов, работающих над задачей

    print("Количество роботов: " + str(len(robots)) + "\nКоличество целей: " + str(len(targets)))
    print("\nМатрица D:")
    print(D)
    print("\nВектор Nmax:")
    print(Nmax)

    # Пока все цели не выполнены, пытаемся их выполнить
    while(not all([x.isReady() for x in targets])):

        # Распределение целей между роботами
        for i in range(0, len(robots)):
            # Проверяем, необходимо ли распределять цели между роботами
            if (np.all(D<=0.0001) or np.all(Nmax<=0.0001)):
                print("\nМатрица D или Nmax содержат все нули")
                break
            else:
                print("\nРаспределение целей между свободными роботами")
                if robots[i].isFree():
                    col = np.argmax(D[i])
                    row = np.argmax(D[:, col])
                    print("Поиск задания для " + str(i) + " робота")
                    print("Поиск индекса максимального элемента в " + str(i) + "-ой строке: " + str(col))
                    print(f"Поиск индекса максимального элемента в {col}-м стобце: " + str(row))

                    # Если данный робот эффективен для выбранной цели, то закрепляем её за ним
                    if row == i:
                        robots[i].setTarget(targets[col])  # Указываем роботу цель для выполнения
                        targets[col].setExecutor(robots[i])  # Устанавливаем исполнителя для задачи

                        # Уменьшаем Nmax
                        Nmax[col] = Nmax[col] - 1

                        # Нулим строку робота в матрице D
                        D[i] = 0

                        # Нулим столбец, если набралось максимальное кол-во исполнителей
                        if Nmax[col] == 0:
                            D[:, col] = 0

                        print("\nМатрица D:")
                        print(D)
                        print("\nВектор Nmax:")
                        print(Nmax)

        # Выполнение распределённых задач
        


if __name__ == '__main__':
    np.set_printoptions(precision=4, floatmode='fixed')
    algorithm()

