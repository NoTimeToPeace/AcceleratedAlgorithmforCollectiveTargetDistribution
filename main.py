import random

import scipy.stats as sps
import numpy as np
import matplotlib.pyplot as plt


class Target:
    def __init__(self):
        self.__complexity = 10
        self.__isReady = False
        self.__Nmax = random.randint(1, 3)

    def changeComplexity(self, performance):
        self.__complexity = self.__complexity - performance

    def getComplexity(self):
        return self.__complexity

    def getNmax(self):
        return self.__Nmax

    def isReady(self):
        return self.__isReady


class Robot:
    def __init__(self, numberOfTargets):
        self.__powerD = np.array([random.random() for i in range(numberOfTargets)])
        self.__free = True
        self.__target = None

    def setTarget(self, target):
        self.__target = target

    def isFree(self):
        return self.__free

    def getPower(self):
        return self.__powerD

    def setEmployment(self):
        self.__free = not self.__free


def algorithm():
    targets = np.array([Target() for i in range(random.randint(1, 10))])
    robots = np.array([Robot(len(targets)) for i in range(random.randint(1, 10))])
    D = np.column_stack([i.getPower() for i in robots])
    Nmax = np.array([i.getNmax() for i in targets])

    print("Количество целей: " + str(len(targets)))
    print("Количество роботов: " + str(len(robots)))
    print("\nМатрица D:")
    print(D)
    print("\nВектор Nmax:")
    print(Nmax)



if __name__ == '__main__':
    algorithm()

