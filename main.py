import random

import scipy.stats as sps
import numpy as np
import matplotlib.pyplot as plt


class Target:
    def __init__(self):
        self.__complexity = random.uniform(1, 100)
        self.__isReady = False
        self.__N_max = random.randint(1, 3)
        self.__Executors = np.array([], dtype='object')

    def changeComplexity(self, performance):
        if self.__complexity > 0:
            self.__complexity = self.__complexity - performance
        else:
            self.__isReady = True

    def getComplexity(self):
        return self.__complexity

    def getN_max(self):
        return self.__N_max

    def isOverflow(self):
        if self.__Executors.size < self.__N_max:
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
        self.__powerUsed = 0

    def setTarget(self, target, power):
        if self.__target is None and self.isFree():
            self.__target = target
            self.__powerUsed = power
            self.setEmployment()

    def resetTarget(self):
        self.__target = None
        self.__free = True

    def isFree(self):
        return self.__free

    def getPowerD(self):
        return self.__powerD

    def getPowerUsed(self):
        return self.__powerUsed

    def setEmployment(self):
        self.__free = not self.__free

    def getTarget(self):
        return self.__target


def UpdateMatrixD(D, N_max, robots, targets):
    for i in range(0, len(robots)):
        if robots[i].isFree():
            D[i] = robots[i].getPowerD()

    for i in range(0, len(targets)):
        if targets[i].isReady() or N_max[i] == 0:
            D[:, i] = 0


def algorithm():
    targets = np.array([Target() for i in range(random.randint(1, 15))])  # Создаём цели от 1 до 15
    robots = np.array([Robot(len(targets)) for i in range(random.randint(1, 15))])  # Создаём роботов от 1 до 15
    D = np.vstack([i.getPowerD() for i in robots])  # Получаем общую матрицу эффективности роботов над задачами
    N_max = np.array([i.getN_max() for i in
                      targets])  # Получаем общий вектор максимально возможного количества роботов, работающих над задачей

    print("Количество роботов: " + str(len(robots)) + "\nКоличество целей: " + str(len(targets)))
    print("\nМатрица D:")
    print(D)
    print("\nВектор N_max:")
    print(N_max)

    # Пока все цели не выполнены, пытаемся их выполнить
    while not all([x.isReady() for x in targets]):

        # Распределение целей между роботами
        for i in range(0, len(robots)):
            # Проверяем, необходимо ли распределять цели между роботами
            if np.all(D <= 0.0001) or np.all(N_max <= 0.0001):
                print("\nМатрица D или N_max содержат все нули")
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
                        robots[i].setTarget(targets[col],
                                            robots[i].getPowerD()[col])  # Указываем роботу цель для выполнения
                        targets[col].setExecutor(robots[i])  # Устанавливаем исполнителя для задачи

                        # Уменьшаем N_max
                        N_max[col] = N_max[col] - 1

                        # Нулим строку робота в матрице D
                        D[i] = 0

                        # Нулим столбец, если набралось максимальное кол-во исполнителей
                        if N_max[col] == 0:
                            D[:, col] = 0

                        print("\nМатрица D:")
                        print(D)
                        print("\nВектор N_max:")
                        print(N_max)

        # Выполнение распределённых задач
        for i in range(0, len(robots)):
            if not robots[i].isFree():
                robots[i].getTarget().changeComplexity(robots[i].getPowerUsed())
                print("Оставшаяся сложность задачи " + str(robots[i].getTarget()) + ": " +
                      str(robots[i].getTarget().getComplexity()))

                # Если задача выполнена, освобождаем робота и обновляем матрицу D и N_max
                if robots[i].getTarget().isReady():
                    colUpdate = 0
                    # Ищем позицию задачи
                    for x in range(len(targets)):
                        if targets[x] == robots[i].getTarget():
                            colUpdate = x
                            break

                    robots[i].resetTarget()
                    UpdateMatrixD(D, N_max, robots, targets)
                    print(f"Обновленная матрица D после освобождения {i}-го робота:")
                    print(D)
                    N_max[colUpdate] = N_max[colUpdate] + 1


if __name__ == '__main__':
    np.set_printoptions(precision=2, floatmode='fixed')
    np.set_printoptions(threshold=np.inf)
    algorithm()
