from utility import *
import random
import copy

class ECC:
    def __init__(self, a, b, g, x, p = 32749):
        self.p = p
        self.sqrt_mod = [-1 for i in range(p)]
        for i in range(p):
            self.sqrt_mod[i*i%p] = i
        # 4a**3 + 27b**2 != 0
        self.a = a % p
        self.b = b % p
        self.base = self.generate_point(g)
        self.key_x = x
        self.key_y = self.mul_point(x, self.base)
    
    def add_point(self, tuple1, tuple2):
        if (tuple1[0] < 0):
            return copy.deepcopy(tuple2)
        m = 0
        if(tuple1[0] == tuple2[0]):
            if(tuple1[1] == tuple2[1] and tuple1[1]>0):
                m_top = (3*tuple1[0]*tuple1[0] + self.a) % self.p
                m_bot = (2*tuple1[1]) % self.p
                m = m_top * inv_mod(m_bot, self.p) % self.p
            else:
                return [-1, -1]
        else:
            m_top = (tuple1[1] - tuple2[1] + self.p) % self.p
            m_bot = (tuple1[0] - tuple2[0] + self.p) % self.p
            m = m_top * inv_mod(m_bot, self.p) % self.p
        
        xr = (m*m-tuple1[0]-tuple2[0]+2*self.p) % self.p
        yr = ((tuple1[0]-xr+self.p) % self.p * m - tuple1[1] + self.p) % self.p
        return [xr, yr]
    
    def mul_point(self, scalar, tup):
        tup_cpy = copy.deepcopy(tup)
        result = [-1, -1]
        while(scalar > 0):
            if(scalar%2):
                result = self.add_point(result, tup_cpy)
            scalar //= 2
            tup_cpy = self.add_point(tup_cpy, tup_cpy)
        return result
    
    def encrypt_int(self, message_int, k) -> [int, int]:
        point = self.generate_point(message_int)
        return [self.mul_point(k, self.base), self.add_point(point, self.mul_point(k, self.key_y))]
        
    
    def encrypt_text(self, message):
        chars = list(message)
        ints = [ord(chars[i]) for i in range(len(chars))]
        result_int = [self.encrypt_int(ints[i], random.randrange(0, self.p-1)) for i in range(len(ints))]
        # print(result_int)
        result = ""
        for i in range(len(result_int)):
            for j in range(2):
                if(result_int[i][j][0] < 0):
                    result += chr(255)
                    result += chr(255)
                else:
                    twochar = result_int[i][j][0]*2 + (result_int[i][j][1] > (self.p//2))
                    result += chr(twochar // 256)
                    result += chr(twochar % 256)
        return result

    def decrypt_int(self, int0, int1, int2, int3):
        x1 = (int0*256 + int1)//2 % self.p
        y1 = self.sqrt_mod[(x1*x1*x1 + self.a*x1 + self.b) % self.p]
        if(int1%2):
            y1 = (self.p - y1) % self.p
        tuple1 = [x1, y1]
        if(int0*256 + int1 == 255*256 + 255):
            tuple1 = [-1, -1]
        
        x2 = (int2*256 + int3)//2 % self.p
        y2 = self.sqrt_mod[(x2*x2*x2 + self.a*x2 + self.b) % self.p]
        if(int3%2 == 0):
            y2 = (self.p - y2) % self.p
        tuple2 = [x2, y2]
        if(int2*256 + int3 == 255*256 + 255):
            tuple2 = [-1, -1]

        result = self.add_point(self.mul_point(self.key_x, tuple1), tuple2)
        return (result[0]-1) // (self.p//256)

    def decrypt_text(self, message):
        chars = list(message)
        ints = [ord(chars[i]) for i in range(len(chars))]
        result_int = [self.decrypt_int(ints[4*i], ints[4*i+1], ints[4*i+2], ints[4*i+3]) for i in range(len(chars)//4)]
        # print(result_int)
        result_char = [chr(result_int[i]) for i in range(len(result_int))]
        return ''.join(result_char)
    
    def generate_point(self, m):
        k = self.p // 256
        y = -1
        x = m*k
        while(y < 0):
            x += 1
            y = self.sqrt_mod[(x*x*x + self.a*x + self.b) % self.p]
        return [x, y]

  
tes = ECC(3, 5, 131, 45)
encrypt = tes.encrypt_text('''
Halo nama saya kinantan arya,
ini beneran sekali compile jadi?
moga gausah debug lagi, demaps aowkaowkaow...
''')
print(encrypt)
decrypt = tes.decrypt_text(encrypt)
print(decrypt)
