from primeGenerator import generateNBitPrime as gen
from math import gcd, lcm, log
import random

PAIL_PAD_INFO = 4 # Reserve 4 byte for padding info

def get_int_byte_length(num):
    return 1 if not num else int(log(num,256)) + 1

def encrypt(plaintext:bytearray,g,n):
    block_length = get_int_byte_length(n**2)
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
        cipher_blocks.append(encrypt_block(block,g,n))
    
    # Converting blocks to Byte
    cipher_blocks = [block.to_bytes(length=block_length, byteorder='big',signed=False) for block in cipher_blocks]

    # Generating ciphertext
    ciphertext = b''
    for block in cipher_blocks:
        ciphertext += block
    ciphertext += pad_length.to_bytes(length=PAIL_PAD_INFO,byteorder='big',signed=False)

    return ciphertext

def decrypt(ciphertext:bytearray,g,n,lmd,mu):
    block_length = get_int_byte_length(n**2)
    group_length = block_length//2
    # Splitting ciphertext with padding info
    cipher_blocks, padding = ciphertext[:-PAIL_PAD_INFO], int.from_bytes(ciphertext[-PAIL_PAD_INFO:],byteorder='big',signed=False)

    # Splitting blocks
    cipher_blocks = [cipher_blocks[i:i+block_length] for i in range(0,len(cipher_blocks),block_length)]

    # Converting blocks to integer
    cipher_blocks = [int.from_bytes(byte, byteorder='big', signed=False) for byte in cipher_blocks]

    # Decrypting
    plain_blocks = []
    for block in cipher_blocks:
        plain_blocks.append(decrypt_block(block,lmd,mu,g,n))
    
    # Converting blocks to Byte
    plain_blocks = [block.to_bytes(length=group_length, byteorder='big',signed=False) for block in plain_blocks]

    # Removing padding
    plain_blocks[-1] = plain_blocks[-1][padding:]

    # Generating plaintext
    plaintext = b''
    for block in plain_blocks:
        plaintext += block

    return bytearray(plaintext)

def encrypt_block(plain,g,n):
    r = random.randrange(0,n-1)
    while gcd(r,n) != 1:
        r = random.randrange(0,n-1)
    return (pow(g,plain,n**2) * pow(r,n,n**2)) % n**2

def decrypt_block(cipher,lmd,mu,g,n):
    return (l(pow(cipher,lmd,n**2),n)*mu) % n

def l(x,n):
    return (x-1)//n

def generate_pair():
    p,q = 0,0
    while True:    
        p = gen(32)
        q = gen(32)
        if gcd(p*q,((p-1)*(q-1)))==1:
            break
    
    n = p*q
    lmd = lcm(p-1,q-1)
    g = random.randrange(2,(n**2)-1)

    x = pow(g,lmd,n**2)

    mu = pow(l(x,n),-1, n)
    
    pub_key = {"g":g, "n":n}
    pri_key = {"lmd":lmd, "mu":mu, "g":g, "n":n}

    return pub_key,pri_key

if __name__ == '__main__':
    key = {'lmd': 7475076894602614220, 'mu': 12577573489665403120, 'g': 50101817992855509688926408138863197681, 'n': 14950153796977498039}
    test = 'Zingga dingga ding'
    str_b = bytearray(test.encode())
    r1 = encrypt(str_b,key['g'],key['n'])
    print(r1)
    res = ''.join('{:02x}'.format(byte) for byte in r1)
    print(res)
    back = bytearray.fromhex(res)

    r2 = decrypt(back,key['g'],key['n'],key['lmd'],key['mu'])
    print(r2.decode('utf-8'))