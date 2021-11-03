def euler_totient(x):
    '''
    Banyak bilangan positif kurang dari sama dengan x yang relatif prima dengan x
    Tidak digunakan karena time complexity yang besar yakni O(sqrt(x))
    '''
    idx = 2
    x_cpy = x
    result = x
    while(idx*idx <= x):
        if(x_cpy%idx == 0):
            result = result//idx*(idx-1)
            while(x_cpy%idx == 0):
                x_cpy //= idx
        idx += 1
    if(x_cpy > 1): # x prima
        return x_cpy-1
    return result

def fast_pow(a, b, mod):
    '''
    a pangkat b dalam modulo mod, menggunakan binary exponentiation
    '''
    result = 1
    while(b>0):
        if(b%2):
            result = (result * a) % mod
        a = (a*a) % mod
        b //= 2
    return result

def inv_mod(x, mod):
    '''
    Inverse x dalam modulo mod
    mod diasumsikan prima, jika tidak mod-2 -> euler_totient(mod)-1
    '''
    return fast_pow(x, mod-2, mod)

def str_to_int(nByte, string):
    '''
    Mengubah string menjadi int, byte demi byte
    '''
    res = 0
    for i in range(nByte):
        res *= 256
        if i<len(string):
            res += ord(string[i])
    return res
            

def int_to_str(nByte, x):
    '''
    Mengubah int menjadi string, byte demi byte
    '''
    res = ""
    for i in range(nByte):
        res += chr(x % 256)
        x //= 256
    return res[::-1]

'''
def test():
    print(euler_totient(100))
    print(euler_totient(1000000007))
    print(fast_pow(3, 5, 100))
    print(inv_mod(3, 100))
    print(inv_mod(3, 1000000007))

test()
'''