from method.utility import *
import random
import json
import copy
from method.primeGenerator import generateNBitPrime as gen


class ECC:
    def __init__(self, a, b, g, x, p = 32749):
        '''
        Konstruktor kelas ini dibedakan untuk p < 32768 atau sebaliknya, sebut p kecil dan besar
        Untuk p kecil, self.sqrt_mod[i] menyatakan y sehingga y**2 = i mod p
        Untuk p besar, hal diatas tidak bisa dihitung (terlalu lama), melainkan dihitung banyak byte bilangan p
        Untuk p besar juga, simpan self.mul_base yang merupakan perkalian self.base dengan 0 hingga 255
        p sudah diasumsikan prima, g dapat berupa 2 bilangan sebagai point, atau 1 bilangan sebagai generator
        '''
        self.p = p
        self.a = a % p
        self.b = b % p
        g = g.split(" ")
        
        if 2*p < 65536:
            self.sqrt_mod = [-1 for i in range(p)]
            for i in range(p):
                self.sqrt_mod[i*i%p] = i
        else:
            self.nByte = 0
            self.pow256 = 1
            while(p>0):
                self.nByte += 1
                p //= 256
                self.pow256 *= 256

        # print(g)
        if len(g) == 1:
            try:
                self.base = self.generate_point(int(g[0]))
            except:
                self.base = None
        elif len(g) == 2:
            try:
                self.base = [int(g[0]), int(g[1])]
            except:
                self.base = None
        else:
            self.base = None
        
        self.key_x = x
        if(self.base != None):
            self.key_y = self.mul_point(x, self.base)
            self.mul_base = [[-1,-1], self.base]
            for i in range(255):
                self.mul_base.append(self.mul_point(i+2, self.base))
        
        
    
    def isViolate(self):
        '''
        Menentukan apakah parameter kunci publik dan privat yang dimasukkan memenuhi batasan atau tidak
        Dapat dilihat semua kasusnya dalam kode di bawah
        '''
        if (4*self.a*self.a*self.a + 27*self.b*self.b) % self.p == 0:
            return "4a**3 + 27b**2 == 0"
        if(self.base == None):
            return "Base point input not valid"
        xeq = self.base[0]
        yeq = self.base[1]
        if ((xeq*xeq*xeq + self.a*xeq + self.b - yeq*yeq) % self.p != 0):
            return "Base point is not in the curve"
        
        return ""

    def add_point(self, tuple1, tuple2):
        '''
        Menambahkan point berkoordinat tuple1 dan tuple2 sesuai definisi penambahan pada kurva
        Point inf adalah [-1,-1]
        '''
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
        '''
        Mengalikan skalar scalar dengan point berkoordinat tup dengan penambahan biner pada kurva
        Point inf adalah [-1,-1]
        '''
        tup_cpy = copy.deepcopy(tup)
        result = [-1, -1]
        while(scalar > 0):
            if(scalar%2):
                result = self.add_point(result, tup_cpy)
            scalar //= 2
            tup_cpy = self.add_point(tup_cpy, tup_cpy)
        return result
    
    def encrypt_int(self, message_int, k) -> [int, int]:
        '''
        Mengenkripsi 1 karakter menjadi 2 point sesuai prosedur ECC
        Bila p kecil membangkitkan point, sebaliknya ambil dari mul_base karena waktu terbatas
        '''
        if(2*self.p < 65536):
            point = self.generate_point(message_int)
            return [self.mul_point(k, self.base), self.add_point(point, self.mul_point(k, self.key_y))]
        else: # Big p, cannot generate
            point = self.mul_base[message_int+1]
            return [self.mul_point(k, self.base), self.add_point(point, self.mul_point(k, self.key_y))]
    
    def encrypt_text(self, message):
        '''
        Tiap karakter dienkripsi jadi 2 point. Sebenarnya terdapat opsi lain diantaranya:
        - Tiap karakter jadi 1 point, dengan menambahkan k*base 1 point terdepan (tidak perlu random tiap karakter, cukup sekali)
        - Fungsi mengembalikan points ketimbang characters
        '''
        chars = list(message)
        ints = [ord(chars[i]) for i in range(len(chars))]
        result_int = [self.encrypt_int(ints[i], random.randrange(0, self.p-1)) for i in range(len(ints))]
        # print(result_int)
        result = ""
        if(2*self.p<65536):
            '''
            Tiap points dipetakan jadi 2 karakter saja cukup
            Ini dikarenakan 0 < x < 32768 dan hanya ada 2 kemungkinan y tiap nilai x
            Sehingga banyak kemungkinan kurang dari 65536 yakni tepat 2 byte atau 2 karakter
            Point [-1,-1] dipetakan ke 65535
            '''
            for i in range(len(result_int)):
                for j in range(2):
                    if(result_int[i][j][0] < 0):
                        result += chr(255)
                        result += chr(255)
                    else:
                        twochar = result_int[i][j][0]*2 + (result_int[i][j][1] > (self.p//2))
                        result += chr(twochar // 256)
                        result += chr(twochar % 256)
        else:
            '''
            Tiap points dipetakan jadi nBytes karakter saja cukup, menggunakan fungsi int_to_str
            '''
            for i in range(len(result_int)):
                # print(result_int[i])
                for j in range(2):
                    for k in range(2):
                        if result_int[i][j][k]<0:
                            result += int_to_str(self.nByte, self.pow256-1)
                        else:
                            result += int_to_str(self.nByte, result_int[i][j][k])
        return result


    def decrypt_int(self, int0, int1, int2, int3):
        '''
        Bagi kasus p kecil/besar, sesuaikan dengan enkripsi
        Bila p kecil, cukup kembalikan floor((x-1)/256)
        Bila p besar, kembalikan mul_base yang sesuai
        Untuk menegasikan tuple pertama cukup ganti ordinatnya(y) dengan p-y
        '''
        if 2*self.p < 65536:
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
        else:
            tuple1 = [(int0+1)%self.pow256-1, (int1+1)%self.pow256-1]
            tuple2 = [(int2+1)%self.pow256-1, (int3+1)%self.pow256-1]

            if(tuple1[1] >= 0):
                tuple1[1] = (self.p - tuple1[1]) % self.p

            result = self.add_point(self.mul_point(self.key_x, tuple1), tuple2)
            for i in range(256):
                if result == self.mul_base[i+1]:
                    return i
            return -1

    def decrypt_text(self, message):
        '''
        Sesuaikan p kecil/besar dengan algoritma enkripsi
        Untuk p kecil, lakukan decrypt_int tiap 4 karakter, sebaliknya tiap 4*nByte karakter dengan str_to_int
        '''
        if 2*self.p < 65536:
            chars = list(message)
            ints = [ord(chars[i]) for i in range(len(chars))]
            result_int = [self.decrypt_int(ints[4*i], ints[4*i+1], ints[4*i+2], ints[4*i+3]) for i in range(len(chars)//4)]
            # print(result_int)
            result_char = [chr(result_int[i]) for i in range(len(result_int))]
            return ''.join(result_char)
        else:
            chars = [message[self.nByte*i : min(self.nByte*(i+1), len(message))] for i in range((len(message) + self.nByte-1)//self.nByte)]
            ints = [str_to_int(self.nByte, chars[i]) for i in range(len(chars))]
            
            result_int = [self.decrypt_int(ints[4*i], ints[4*i+1], ints[4*i+2], ints[4*i+3]) for i in range(len(chars)//4)]
            print(result_int)
            result = ""
            for i in range(len(result_int)):
                if result_int[i] < 0:
                    return "Wrong ciphertext"
                result += chr(result_int[i])
            return result
    
    def generate_point(self, m):
        '''
        Memilih point pada kurva dengan mencari solusi kurva dengan mencoba dari x=mk+1 hingga ketemu
        '''
        k = self.p // 256
        y = -1
        x = m*k
        while(y < 0):
            x += 1
            y = self.sqrt_mod[(x*x*x + self.a*x + self.b) % self.p]
        return [x, y]

    def generate_pair(self,save=False):
        '''
        Membangkitkan prima 1024 bit dengan fungsi dari primeGenerator.py
        '''
        p = gen(64)
        
        g = [random.randrange(0, p-1), random.randrange(0, p-1)]
        x = random.randrange(2, p-2)
        y = self.mul_point(x, g)

        a = random.randrange(0, p-1)
        b = ((g[1]*g[1] - g[0]*g[0]*g[0] - a*g[0]) % p + p) % p

        # Creating Key Dictionary
        pub_key = {'p':p,'a': a, 'b': b, 'g':g, 'y': y}
        pri_key = {'p':p,'x':x}

        if save:
            json.dump(pub_key, open('./key/ecc_key.pub','w'))
            json.dump(pri_key, open('./key/ecc_key.pri','w'))

        self.p = p
        self.g = g
        self.a = a
        self.b = b
        self.x = x
        self.y = y
    
        return p, a, b, g, x
    
    def open_key(self, dir:str):
        with open(dir) as f:
            data = f.read()
            key = json.loads(data)
            if dir.endswith('.pub'):
                self.p = key['p']
                self.a = key['a']
                self.b = key['b']
                self.g = key['g']
            elif dir.endswith('.pri'):
                self.p = key['p']
                self.x = key['x']
            return key
        
"""
tes = ECC(3, 5, 131, 45)
encrypt = tes.encrypt_text('''
Halo nama saya kinantan arya,
ini beneran sekali compile jadi?
moga gausah debug lagi, demaps aowkaowkaow...
''')
print(encrypt)
decrypt = tes.decrypt_text(encrypt)
print(decrypt)
"""
