from method.utility import *
import random
import json
from method.primeGenerator import generateNBitPrime as gen

class Elgamal:
    # Konstruktor
    def __init__(self, g, x, p = 257):
        '''
        Konstruktor ini mengasumsikan p prima, serta membuat field-field sesuai parameter dan elgamal pada umumnya
        self.nByte adalah banyak Byte dari representasi biner p
        '''
        self.p = p
        self.g = g % p
        self.x = x % p
        self.y = fast_pow(g, x, p)
        self.nByte = 0
        p -= 1
        while (p>1):
            self.nByte += 1
            p //= 256
        print(self.nByte)
        self.EG_BIT_SIZE = 1024

    def encrypt_int(self, message_int, k) -> [int, int]:
        '''
        Enkripsi 1 karakter menjadi 2 karakter dengan parameter tambahan k, yang diimplementasikan bil random
        '''
        return [fast_pow(self.g, k, self.p), message_int * fast_pow(self.y, k, self.p) % self.p]
    
    def encrypt_text(self, message):
        '''
        Seperti ECC, terdapat opsi lain yakni message n karakter cukup dienkripsi jadi n+1 karakter saja dengan
        membangkitkan bil random k sekali saja.
        Namun implementasi ini tetap menggunakan 1 karakter -> 2 karakter
        '''
        chars = [message[self.nByte*i : min(self.nByte*(i+1), len(message))] for i in range((len(message) + self.nByte-1)//self.nByte)]
        ints = [str_to_int(self.nByte, chars[i])+1 for i in range(len(chars))]
        result_int = [self.encrypt_int(ints[i], random.randrange(0, self.p-1)) for i in range(len(ints))]
        print(result_int)
        result_char = [int_to_str(self.nByte, result_int[i//2][i%2] - 1) for i in range(2*len(result_int))]
        return ''.join(result_char)
    
    def decrypt_int(self, a, b):
        '''
        Dekripsi sesuai metode elgamal
        '''
        return b * inv_mod(fast_pow(a, self.x, self.p), self.p) % self.p

    def decrypt_text(self, message):
        '''
        Dekripsi sesuai metode enkripsi, memanfaatkan str_to_int, int_to_str, 
        dan memisah text jadi string-string sepanjang self.nByte
        '''
        chars = [message[self.nByte*i : min(self.nByte*(i+1), len(message))] for i in range((len(message) + self.nByte-1)//self.nByte)]
        ints = [str_to_int(self.nByte, chars[i])+1 for i in range(len(chars))]
        result_int = [self.decrypt_int(ints[2*i], ints[2*i+1]) for i in range(len(chars)//2)]
        print(result_int)
        result_char = [int_to_str(self.nByte, result_int[i]-1) for i in range(len(result_int))]
        return ''.join(result_char)
    
    def generate_pair(self,save=False):
        '''
        Membangkitkan prima 1024 bit dengan fungsi dari primeGenerator.py
        '''
        p = gen(self.EG_BIT_SIZE)

        g = random.randrange(2, p-1)
        x = random.randrange(2, p-2)
        y = fast_pow(g, x, p)

        # Creating Key Dictionary
        pub_key = {'p':p,'g':g, 'y': y}
        pri_key = {'p':p,'x':x}

        if save:
            json.dump(pub_key, open('./key/eg_key.pub','w'))
            json.dump(pri_key, open('./key/eg_key.pri','w'))

        self.p = p
        self.g = g
        self.x = x
        self.y = y
    
        return p, g, x

    def open_key(self, dir:str):
        with open(dir) as f:
            data = f.read()
            key = json.loads(data)
            if dir.endswith('.pub'):
                self.p = key['p']
                self.g = key['g']
                self.y = key['y']
            elif dir.endswith('.pri'):
                self.p = key['p']
                self.x = key['x']
            return key

'''   
tes = Elgamal(3, 5)
encrypt = tes.encrypt_text("tes")
print(encrypt)
decrypt = tes.decrypt_text(encrypt)
print(decrypt)
'''