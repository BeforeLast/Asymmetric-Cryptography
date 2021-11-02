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

    def encrypt(self, plaintext: bytes):
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

        return ciphertext

    def decrypt(self,ciphertext: bytes):
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

        return plaintext

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
            pb = open('rsa_key.pub','w')
            pb.write(str(pub_key))
            pb.close()

            pr = open('rsa_key.pri','w')
            pr.write(str(pri_key))
            pr.close

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
    tools.generate_pair(save=True)

    string = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Curabitur aliquam ex ac vestibulum ultrices. Phasellus aliquet, ligula eget aliquam pulvinar, nulla augue mollis neque, quis ornare massa metus sit amet metus. Mauris eget iaculis tortor. Proin feugiat lorem quis diam molestie suscipit. Curabitur nunc massa, condimentum non fermentum in, dapibus et velit. Vivamus odio erat, dapibus id lectus ac, ultricies auctor felis. Duis interdum rutrum volutpat. Pellentesque suscipit ante sed suscipit tincidunt. Nunc eu ex eu magna porta dictum sit amet et lorem. Aliquam aliquet risus ac felis tincidunt, id scelerisque enim maximus. Donec sit amet metus quis nulla eleifend ullamcorper hendrerit et enim. Sed ut ultrices leo. Sed volutpat neque mi, vitae finibus dolor consequat ac. Nullam sollicitudin tortor lectus, eu eleifend felis sodales ut. Mauris sed tincidunt lacus.'
    str_b = string.encode('utf-8')
    r1 = tools.encrypt(str_b)
    print(r1)
    r2 = tools.decrypt(r1)
    print(r2)