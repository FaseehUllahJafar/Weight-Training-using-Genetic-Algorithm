import random
import numpy as np
import math

population = []

w1Rows = 4
w1Colums = 16
w2Rows = 16
w2Colums = 3
b1Rows = 16
b1Colums = 1
b2Rows = 3
b2Colums = 1


def readFile(filename):
    with open(filename, 'r') as file:
        list = []
        # reading each line
        for line in file:
            # reading each word
            for word in line.split(','):
                # displaying the words
                list.append(word)
    return list


def convert_2D(list):
    temp = []
    out = []
    for i in list:
        if i[len(i) - 1] == '\n':
            temp.append(i)
            out.append(temp)
            temp = []
        else:
            temp.append(i)

    return out


file = readFile('iris dataset.csv')
file = convert_2D(file)


def z_Values(weights, input, baises):
    WArray = np.transpose(weights)
    IArray = np.array(input)
    BArray = np.array(baises)
    dot_result = np.dot(WArray, IArray)
    ZValue = np.add(dot_result, baises)
    return ZValue


def Sigmoid(ZValue):  # this Function will take Values of Z in thr Form of List and will return list of A Values
    AValue = []
    for x in ZValue:
        AValue.append(1 / (1 + np.exp(-1 * x)))
    return AValue


def class_Label(Yhat_value):
    # return (1 if (Yhat_value > 0.5) else 2)
    if (Yhat_value[0] > Yhat_value[1] and Yhat_value[0] > Yhat_value[2]):
        return 1
    elif (Yhat_value[1] > Yhat_value[0] and Yhat_value[1] > Yhat_value[2]):
        return 2
    else:
        return 3

    # labe1 = [0, 0]
    # labe2 = [0, 1]
    # ret = []
    # for i in range(len(Yhat_value)):
    #     if (Yhat_value[i] > 0.5):
    #         ret.append(0)
    #     else:
    #         ret.append(1)
    #
    # if labe1 == ret:
    #     return 1
    # elif labe2 == ret:
    #     return 2
    # else:
    #     return 3


def Return_Input(values):  # this Function Will Return Input In Correct Format
    list1 = []
    for x in range(4):
        list1.append([])
        list1[x].append(values[x])

    return list1


# r...range
def create_population(size):
    sizeOfInd = ((w1Rows * w1Colums) + (w2Rows * w2Colums) + (b1Rows * b1Colums) + (b2Rows * b2Colums))

    for i in range(size):
        temp = []
        for j in range(sizeOfInd):
            temp.append(random.randint(-50, 50))
        population.append(temp)


def separateLists(ind):
    ret = []
    weights1 = []
    weights2 = []
    bias1 = []
    bias2 = []

    index = 0
    for i in range(w1Rows):
        temp = []
        for j in range(w1Colums):
            temp.append(ind[index])
            index += 1
        weights1.append(temp)

    for i in range(w2Rows):
        temp = []
        for j in range(w2Colums):
            temp.append(ind[index])
            index += 1
        weights2.append(temp)

    for i in range(b1Rows):
        temp = []
        for j in range(b1Colums):
            temp.append(ind[index])
            index += 1
        bias1.append(temp)

    for i in range(b2Rows):
        temp = []
        for j in range(b2Colums):
            temp.append(ind[index])
            index += 1
        bias2.append(temp)

    ret.append(weights1)
    ret.append(weights2)
    ret.append(bias1)
    ret.append(bias2)

    return ret


def print_2D(arr):
    for i in arr:
        print(i)
    print("\n")


def fitness(ind):
    ret = separateLists(ind)
    # level 1
    weights1 = ret[0]
    # level 2
    weights2 = ret[1]
    # bias level 1
    bias1 = ret[2]
    # level 2
    bias2 = ret[3]
    # bias = bias[0]

    # print_2D(weights1)
    # print_2D(weights2)
    # print_2D(bias1)
    # print_2D(bias2)
    # print(bias)

    predictedTrue = 0
    # label 3
    ignoreLabel = 0

    i = 1
    while i < len(file):
        # input layer
        input = []
        for element in file[i]:
            input.append(float(element))
        temp = []
        temp.append(input[len(input) - 1])
        input.pop(len(input) - 1)

        orignalOutput = temp[0]

        # ignoring label 3
        # if orignalOutput == 3:
        #     ignoreLabel += 1
        #     i += 1
        #     continue

        # hidden layer
        input = Return_Input(input)
        a = Sigmoid(z_Values(weights1, input, bias1))
        # ouput layer

        y = class_Label(z_Values(weights2, a, bias2))

        if y == orignalOutput:
            predictedTrue += 1

        i += 1

    # return ((predictedTrue / (len(file) - 1 - ignoreLabel) * 100))
    return ((predictedTrue / (len(file) - 1) * 100))


def sort():
    for i in range(len(population)):
        for j in range(i + 1, len(population)):
            if fitness(population[i]) < fitness(population[j]):
                population[i], population[j] = population[j], population[i]


def print_Population(list):
    for i in list:
        print(i, fitness(i))


# list containing list of population
# per(%) is % of selection
# returns selected + updated list
def selector(list, per):
    selected = []

    # number of individual to select
    # percentage calculator(80 percent of 5 = 4)
    num = len(list) / 100
    num = int(num * per)

    r = 0
    # selects num number of individual
    for i in range(num):
        selected.append(list[i])
        list.pop(i)

    # returning selected population
    return selected


def cross(chromose1, chromose2):
    crossOver_point1 = random.randint(0, len(chromose1) - 1)
    crossOver_point2 = random.randint(crossOver_point1, len(chromose2) - 1)
    index = 0

    for x in range(crossOver_point1, crossOver_point2):
        temp = chromose2[index]
        chromose2[index] = chromose1[x]
        chromose1[x] = temp
        index += 1

    return chromose1, chromose2


def crossOver(list, per):
    crossed = []
    num = int(len(list) / 2)

    # num = len(population) / 100
    # num = int((num * per) / 2)
    j = 1
    if (num % 2) != 0:
        num -= 1
    for i in range(num):
        r = random.randint(0, (len(list) - 1))
        chromo1 = list[r]
        list.pop(r)
        if (num - (i + j)) > 0:
            r = random.randint(0, (len(list) - 1 - (i + j)))
        else:
            r = 0
        chromo2 = list[r]
        list.pop(r)
        ret = cross(chromo1, chromo2)
        crossed.append(ret[0])
        crossed.append(ret[1])
        j += 1

    return crossed


def mutate(ind):
    ind[random.randint(0, len(ind) - 1)] = random.randint(-50, 50)
    ind[random.randint(0, len(ind) - 1)] = random.randint(-50, 50)
    ind[random.randint(0, len(ind) - 1)] = random.randint(-50, 50)

    return ind


def mutation(list):
    num = len(list)
    mutated = []
    for i in range(num):
        ind = mutate(list[i])
        list.pop(i)
        list.append(ind)

    return mutated


# creating population of 20
create_population(20)
print("-------------------------------------------------")
print("Before Genetic Algo")
print("-------------------------------------------------")
sort()

i = 0
print("Max Fitness = ", fitness(population[0]))
print("\n-------------------------------------------------")
while i < 500 and fitness(population[0]) < 100:
    selected = selector(population, 40)
    crossed = crossOver(population, 40)
    mutated = mutation(population)

    population.extend(selected)
    population.extend(crossed)
    population.extend(mutated)

    sort()
    print("Generation = ", i, "\tMax Fitness = ", fitness(population[0]))
    i += 1

print("\n-------------------------------------------------")
print("After Genetic Algo")
print("-------------------------------------------------")
print("Generation = ", i)
print("Max Fitness = ", fitness(population[0]))
print("Min Fitness = ", fitness(population[len(population) - 1]))
# print(len(population))
# print_Population(population)