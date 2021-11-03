import json
from method.primeGenerator import generateNBitPrime as gen
from math import gcd, lcm, log
import random
class Paillier:
    PAIL_BIT_SIZE = 256
    PAIL_PAD_INFO = 4 # Reserve 4 byte for padding info
    public_key = {'g':1,'n':1}
    private_key = {'g':1,'n':1,'lmd':1,'mu':1}

    def __init__(self,pub_key={'g':1,'n':1},priv_key={'g':1,'n':1,'lmd':1,'mu':1}):
        self.public_key = pub_key
        self.private_key = priv_key

    def get_int_byte_length(self,num):
        return 1 if not num else int(log(num,256)) + 1

    def encrypt(self,plaintext:bytearray):
        block_length = self.get_int_byte_length(self.public_key['n']**2)
        group_length = block_length//2
        
        # Splitting into groups
        plain_blocks = [plaintext[i:i+group_length] for i in range(0,len(plaintext),group_length)]

        # Getting padding info
        pad_length = group_length-len(plain_blocks[-1])

        # Converting blocks to integer
        plain_blocks = [int.from_bytes(byte, byteorder='big', signed=False) for byte in plain_blocks]

        # Encrypting
        cipher_blocks = []
        for block in plain_blocks:
            cipher_blocks.append(self.encrypt_block(block))
        
        # Converting blocks to Byte
        cipher_blocks = [block.to_bytes(length=block_length, byteorder='big',signed=False) for block in cipher_blocks]

        # Generating ciphertext
        ciphertext = b''
        for block in cipher_blocks:
            ciphertext += block
        ciphertext += pad_length.to_bytes(length=self.PAIL_PAD_INFO,byteorder='big',signed=False)

        return ciphertext

    def decrypt(self,ciphertext:bytearray):
        block_length = self.get_int_byte_length(self.private_key['n']**2)
        group_length = block_length//2
        # Splitting ciphertext with padding info
        cipher_blocks, padding = ciphertext[:-self.PAIL_PAD_INFO], int.from_bytes(ciphertext[-self.PAIL_PAD_INFO:],byteorder='big',signed=False)

        # Splitting blocks
        cipher_blocks = [cipher_blocks[i:i+block_length] for i in range(0,len(cipher_blocks),block_length)]

        # Converting blocks to integer
        cipher_blocks = [int.from_bytes(byte, byteorder='big', signed=False) for byte in cipher_blocks]

        # Decrypting
        plain_blocks = []
        for block in cipher_blocks:
            plain_blocks.append(self.decrypt_block(block))
        
        # Converting blocks to Byte
        plain_blocks = [block.to_bytes(length=group_length, byteorder='big',signed=False) for block in plain_blocks]

        # Removing padding
        plain_blocks[-1] = plain_blocks[-1][padding:]

        # Generating plaintext
        plaintext = b''
        for block in plain_blocks:
            plaintext += block

        return bytearray(plaintext)

    def encrypt_block(self,plain_block):
        r = random.randrange(0,self.public_key['n']-1)
        while gcd(r,self.public_key['n']) != 1:
            r = random.randrange(0,self.public_key['n']-1)
        return (pow(self.public_key['g'],plain_block,self.public_key['n']**2) * pow(r,self.public_key['n'],self.public_key['n']**2)) % self.public_key['n']**2

    def decrypt_block(self,cipher_block):
        return (self.l(pow(cipher_block,self.private_key['lmd'], self.private_key['n']**2), self.private_key['n'])*self.private_key['mu']) % self.private_key['n']

    def l(self,x,n):
        return (x-1)//n

    def generate_pair(self,save=False):
        p,q = 0,0
        while True:    
            p = gen(self.PAIL_BIT_SIZE)
            q = gen(self.PAIL_BIT_SIZE)
            if gcd(p*q,((p-1)*(q-1)))==1:
                break
        
        n = p*q
        lmd = lcm(p-1,q-1)
        g = random.randrange(2,(n**2)-1)

        x = pow(g,lmd,n**2)

        mu = pow(self.l(x,n),-1, n)
        
        pub_key = {"g":g, "n":n}
        pri_key = {"lmd":lmd, "mu":mu, "g":g, "n":n}

        if save:
            json.dump(pub_key, open('./key/paillier_key.pub','w'))
            json.dump(pri_key, open('./key/paillier_key.pri','w'))
        
        self.public_key = pub_key
        self.private_key = pri_key

        return pub_key,pri_key
    
    def open_key(self, dir:str):
        with open(dir) as f:
            data = f.read()
            key = json.loads(data)
            if dir.endswith('.pub'):
                self.public_key = key
            elif dir.endswith('.pri'):
                self.private_key = key
            return key

if __name__ == '__main__':
    key = {'lmd': 7475076894602614220, 'mu': 12577573489665403120, 'g': 50101817992855509688926408138863197681, 'n': 14950153796977498039}
    tools = Paillier()
    tools.generate_pair()
    test = 'Nice nice nice nice nice nice nice nice nice bad nice nice nice'
    str_b = bytearray(test.encode())
    r1 = tools.encrypt(str_b)
    print(r1)
    res = ''.join('{:02x}'.format(byte) for byte in r1)
    print(res)
    back = bytearray.fromhex(res)
    r2 = tools.decrypt(back)
    print(r2.decode('utf-8'))