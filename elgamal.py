from utility import *
import random

class Elgamal:
    # Konstruktor
    def __init__(self, g, x, p = 257):
        self.p = p
        self.g = g
        self.x = x
        self.y = fast_pow(g, x, p)
    
    def encrypt_int(self, message_int, k) -> [int, int]:
        return [fast_pow(self.g, k, self.p), message_int * fast_pow(self.y, k, self.p) % self.p]
    
    def encrypt_text(self, message):
        chars = list(message)
        ints = [ord(chars[i])+1 for i in range(len(chars))]
        result_int = [self.encrypt_int(ints[i], random.randrange(0, self.p-1)) for i in range(len(ints))]
        print(result_int)
        result_char = [chr(result_int[i//2][i%2] - 1) for i in range(2*len(result_int))]
        return ''.join(result_char)
    
    def decrypt_int(self, a, b):
        return b * inv_mod(fast_pow(a, self.x, self.p), self.p) % self.p

    def decrypt_text(self, message):
        chars = list(message)
        ints = [ord(chars[i])+1 for i in range(len(chars))]
        result_int = [self.decrypt_int(ints[2*i], ints[2*i+1]) for i in range(len(chars)//2)]
        print(result_int)
        result_char = [chr(result_int[i]-1) for i in range(len(result_int))]
        return ''.join(result_char)

'''   
tes = Elgamal(3, 5)
encrypt = tes.encrypt_text("tes")
print(encrypt)
decrypt = tes.decrypt_text(encrypt)
print(decrypt)
'''