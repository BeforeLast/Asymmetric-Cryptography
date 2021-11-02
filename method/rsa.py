from math import floor, sqrt, gcd
import json
from random import randrange
from primeGenerator import generateNBitPrime as gen


class RSA:
    RSA_BIT_SIZE = 1024
    RSA_BLOCK_SIZE = RSA_BIT_SIZE//8 # How many byte can be grouped = RSA_N_bit/8
    RSA_PAD_INFO = 4 # ALLOCATE 4 byte for padding info (Max padding = 4-byte-value of byte)
    public_key = {'n':None,'e':None}
    private_key = {'n':None,'e':None}

    def __init__(self, pub_key={'n':None,'e':None}, priv_key={'n':None,'e':None}):
        self.public_key = pub_key
        self.private_key = priv_key

    def encrypt(self, plaintext: bytearray):
        # Splitting and Adding Guard
        plain_blocks = [b'\x00' + plaintext[i:i+self.RSA_BLOCK_SIZE-1] for i in range(0,len(plaintext),self.RSA_BLOCK_SIZE-1)]
        
        # Padding length check
        pad_length = self.RSA_BLOCK_SIZE-len(plain_blocks[-1])
        if pad_length:
            plain_blocks[-1] = b'\x00' * pad_length + plain_blocks[-1]
        
        # Converting blocks to integer
        plain_blocks = [int.from_bytes(byte, byteorder='big', signed=False) for byte in plain_blocks]

        # Encrypting
        cipher_blocks = []
        for i in range(len(plain_blocks)):
            cipher_blocks.append(pow(plain_blocks[i],self.public_key['e'],self.public_key['n']))
        
        # Converting blocks to Byte
        cipher_blocks = [block.to_bytes(length=self.RSA_BLOCK_SIZE, byteorder='big',signed=False) for block in cipher_blocks]

        # Generating ciphertext
        ciphertext = b''
        for block in cipher_blocks:
            ciphertext += block
        ciphertext += pad_length.to_bytes(length=self.RSA_PAD_INFO,byteorder='big',signed=False)

        return bytearray(ciphertext)

    def decrypt(self,ciphertext: bytearray):
        # Splitting ciphertext with padding info
        cipher_blocks, padding = ciphertext[:-self.RSA_PAD_INFO], int.from_bytes(ciphertext[-self.RSA_PAD_INFO:],byteorder='big',signed=False)

        # Splitting blocks
        cipher_blocks = [cipher_blocks[i:i+self.RSA_BLOCK_SIZE] for i in range(0,len(cipher_blocks),self.RSA_BLOCK_SIZE)]

        # Converting blocks to integer
        cipher_blocks = [int.from_bytes(byte, byteorder='big', signed=False) for byte in cipher_blocks]


        # Decrypting
        plain_blocks = []
        for i in range(len(cipher_blocks)):
            plain_blocks.append(pow(cipher_blocks[i],self.private_key['d'],self.private_key['n']))
        
        # Converting blocks to Byte
        plain_blocks = [block.to_bytes(length=self.RSA_BLOCK_SIZE, byteorder='big',signed=False) for block in plain_blocks]

        # Removing padding
        plain_blocks[-1] = plain_blocks[-1][padding:]
        
        # Removing guard
        plain_blocks = [block[1:] for block in plain_blocks]

        # Generating plaintext
        plaintext = b''
        for block in plain_blocks:
            plaintext += block

        return bytearray(plaintext)

    def generate_pair(self,save=False):
        p = gen(self.RSA_BIT_SIZE//2)
        q = gen(self.RSA_BIT_SIZE//2)
        n = p*q
        tot_n = (p-1)*(q-1)
        
        # GENERATING PUBLIC KEY
        def coprime(a,b):
            return gcd(a,b) == 1

        e = randrange(2,floor(sqrt(tot_n)))
        while not coprime(e,tot_n):
            e += 1

        # GENERATING PRIVATE KEY
        d = pow(e,-1,tot_n)

        # Creating Key Dictionary
        pub_key = {'n':n,'e':e}
        pri_key = {'n':n,'d':d}

        if save:
            json.dump(pub_key, open('rsa_key.pub','w'))
            json.dump(pri_key, open('rsa_key.pri','w'))

        self.public_key = pub_key
        self.private_key = pri_key
    
        return pub_key, pri_key
    
    def open_key(self, dir:str, pub_key:bool):
        with open(dir) as f:
            data = f.read()
            key = json.loads(data)
            if pub_key:
                self.public_key = key
            else:
                self.private_key = key


if __name__ == '__main__':
    tools = RSA()
    tools.open_key('rsa_key.pub',True)
    tools.open_key('rsa_key.pri',False)
    # tools.generate_pair(save=True)

    string = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.'
    str_b = bytearray(string.encode())
    r1 = tools.encrypt(str_b)
    print(r1)
    res = ''.join('{:02x}'.format(byte) for byte in r1)
    print(res)
    back = bytearray.fromhex(res)
    print(back)

        
    # r2 = tools.decrypt(bytearray(res.encode()))
    # print(r2)