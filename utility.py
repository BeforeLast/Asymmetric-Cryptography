def euler_totient(x):
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
    b %= euler_totient(mod)
    result = 1
    while(b>0):
        if(b%2):
            result = (result * a) % mod
        a = (a*a) % mod
        b //= 2
    return result

def inv_mod(x, mod):
    return fast_pow(x, euler_totient(mod)-1, mod)

'''
def test():
    print(euler_totient(100))
    print(euler_totient(1000000007))
    print(fast_pow(3, 5, 100))
    print(inv_mod(3, 100))
    print(inv_mod(3, 1000000007))

test()
'''