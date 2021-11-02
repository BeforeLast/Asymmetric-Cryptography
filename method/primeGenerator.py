import random

def getNBitNumber(n):
    return random.randrange((2**(n-1)), (2**n)-1)

def simplePrimalityTest(number):
    PRIME_TEST = [2,   3,   5,   7,   11,  13,  17,  19,  23,  29,  31,  37,  41,  43,  47,  53,  59,  61,  67,  71,
                  73,  79,  83,  89,  97,  101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173]

    for prime in PRIME_TEST:
        if number % prime == 0:
            return False
    return True

def millerRabinTest(number):
    ITERATION = 40
    
    even_num = number-1
    repeat = 0

    while even_num % 2 == 0:
        even_num //= 2
        repeat += 1
    
    for i in range(ITERATION):
        test = random.randrange(2,number-1)
        if pow(test,even_num,number) == 1:
            continue

        cont = False
        for j in range(repeat):
            if pow(test, 2**j*even_num, number) == number-1:
                cont = True
                break
        if cont :
            continue

        return False
    return True

def generateNBitPrime(n):
    num = getNBitNumber(n)
    while True:
        if simplePrimalityTest(num) and millerRabinTest(num):
            break
        num = getNBitNumber(n)
        # print(num)
    return num

# print(generateNBitPrime())