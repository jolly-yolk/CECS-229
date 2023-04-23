#!/usr/bin/env python
# coding: utf-8

# # CECS 229 Programming Assignment #3
# 
# #### Due Date: 
# 
# Sunday, 3/5 @ 11:59 PM
# 
# #### Submission Instructions:
# 
# To receive credit for this assignment you must submit to CodePost this file converted to a Python script named `pa3.py`
# 
# #### Objectives:
# 
# 1. Find the inverse of a given integer under a given modulo m.
# 2. Encrypt and decrypt text using an affine transformation.
# 3. Encrypt and decrypt text using the RSA cryptosystem.
# 
# 
# 
# 
# ### Programming Tasks
# 
# You may use the utility functions at the end of this notebook to aid you in the implementation of the following tasks:

# ------------------------------------------
# ##### Utility functions (NO EDITS NECESSARY)

def bezout_coeffs(a, b):
    # FIXME: Implement this function
    s0 = 1
    t0 = 0
    s1 = 0
    t1 = 1
    r = b % a
    x = a
    y = b
    
    while (r != 0):
        sk = s0 - (b//a) * s1
        tk = t0 - (b//a) * t1
        b = a
        a = r
        r = b % a
        s0 = s1
        t0 = t1
        s1 = sk
        t1 = tk
        
    return {x : t1, y : s1}  

def gcd(a,b):
    # FIXME: Implement this function
    x = bezout_coeffs(a, b)
    return abs(a * x.get(a) + b * x.get(b))

def primes(a, b):
    if (a < 1):
        raise Exception("Value Error: a is less than 1")
    elif (a > b):
        raise Exception("Value Error: a is greater than b")
    elif (b == 2):
        x = set()
        x.add(2)
        return x
    
    f_primes = set()
    not_primes = set()
    not_primes.add(1)
    interval = set()
    
    for i in range(a, b + 1):
        interval.add(i)
        
    for i in range(2, round(b ** 1/2) + 1):
        f_primes.add(i)
        
    for i in range(a, b + 1):
        for j in f_primes:
            if (i != j):
                if (i % j == 0):
                    not_primes.add(i)
    
    return interval - not_primes

def mod_exp(b, n, m):
    # FIXME: Implement this function
    if (b < 0):
        return 0
    x = 1
    p = b % m
    n = bin(n)[2:]
    n = n[::-1]
    for i in range(len(n)):
        if (int(n[i]) == 1):
            x = (x * p) % m
        p = (p * p) % m
    return x

def blocksize(n):
    """returns the size of a block in an RSA encrypted string"""
    twofive = "25"
    while int(twofive) < n:
        twofive += "25"
    return len(twofive) - 2

def digits2letters(digits):
    letters = ""
    start = 0  #initializing starting index of first digit
    while start <= len(digits) - 2:
        digit = digits[start : start + 2]  # accessing the double digit
        letters += chr( int(digit) +65)   # concatenating to the string of letters
        start += 2                         # updating the starting index for next digit
    return letters

def letters2digits(letters):
    digits = ""
    for c in letters:
        if c.isalpha():
            letter = c.upper()  #converting to uppercase  
            d = ord(letter)-65
            if d < 10:
                digits += "0" + str(d)     # concatenating to the string of digits
            else:
                digits += str(d)
    return digits

# -------------------------------------------
# 
# #### Problem 1: 
# Create a function `modinv(a,m)` that returns the smallest, positive inverse of `a` modulo `m`.  If the gcd of `a` and `m` is not 1, then you must raise a `ValueError` with message `"The given values are not relatively prime"`.  You may NOT use any built-in functions as part of your implementation, but you may use any functions you implemented in previous coding assignments.  Please make sure to copy and paste them into this file, so that they are uploaded to CodePost when you submit your `pa3.py` file.

def modinv(a,m):
    """returns the smallest, positive inverse of a modulo m
    INPUT: a - integer
           m - positive integer
    OUTPUT: an integer in the range [0, m-1]
    """
    if (gcd(a, m) != 1):
        raise ValueError('The given values are not relatively prime')

    for i in range(m - 1, 0, -1):
        if (((a * i)) % m == 1):
            return i
        else:
            continue

# ------------------------------------
# 
# #### Problem 2: 
# Create a function `affineEncrypt(text, a,b)` that returns the cipher text encrypted using key  (`a`, `b`).  You must verify that the gcd(a, 26) = 1 before making the encryption.  If this is not the case, the function must raise a `ValueError` with message `"The given key is invalid. The gcd(a,26) must be 1."`.  You may NOT use any built-in functions as part of your implementation, but you may use any functions you implemented in previous coding assignments.  Please make sure to copy and paste them into this file, so that they are uploaded to CodePost when you submit your `pa3.py` file.

def affineEncrypt(text, a, b):
    """encrypts the plaintext 'text', using an affine transformation key (a, b)
    INPUT:  text - plaintext as a string of letters
            a - integer satisfying gcd(a, 26) = 1.  Raises error if such is not the case
            b - integer 
            
    OUTPUT: The encrypted message as a string of characters
    """
    if (gcd(a, 26) != 1):
        raise Exception('ValueError: The given key is invalid. The gcd(a, 26) must be 1.')
    
    encrypt = ''
    n_text = letters2digits(text)
    slice = ''
    
    for number in n_text:
        if (len(slice) != 2):
            slice += number
            continue
        p = int(slice)
        c = str(((a * p) + b) % 26)
        if (len(c) != 2):
            c = f'0{c}'
        slice = ''
        slice += number
        encrypt += digits2letters(c)

    p = int(slice)
    c = str(((a * p) + b) % 26)
    if (len(c) != 2):
            c = f'0{c}'
    encrypt += digits2letters(c)

    return encrypt

# #### Problem 3: 
# Create a function `affineDecrypt(ciphertext, a,b)` that returns the cipher text encrypted using key  (`a`, `b`). You must verify that the gcd(a, 26) = 1.  If this is not the case, the function must raise `ValueError` with message `"The given key is invalid. The gcd(a,26) must be 1."`.  You may NOT use any built-in functions as part of your implementation, but you may use any functions you implemented in previous coding assignments.  Please make sure to copy and paste them into this file, so that they are uploaded to CodePost when you submit your `pa3.py` file.

def affineDecrypt(ciphertext, a, b):
    """decrypts the string 'ciphertext', which was encrypted using an affine transformation key (a, b)
    INPUT:  ciphertext - a string of encrypted letters
            a - integer satisfying gcd(a, 26) = 1.  
            b - integer 
            
    OUTPUT: The decrypted message as a string of characters
    """
    if (gcd(a, 26) != 1):
        raise Exception('ValueError: The given key is invalid. The gcd(a, 26) must be 1.')
        
    decrypt = ''
    slice = ''
    a_bar = modinv(a, 26)
    n_text = letters2digits(ciphertext)
    
    for number in n_text:
        if (len(slice) != 2):
            slice += number
            continue
        p = int(slice)
        c = str((a_bar * (p - b)) % 26)
        if (len(c) != 2):
            c = f'0{c}'
        slice = ''
        slice += number
        decrypt += digits2letters(c)

    p = int(slice)
    c = str((a_bar * (p - b)) % 26)
    if (len(c) != 2):
            c = f'0{c}'
    decrypt += digits2letters(c)

    return decrypt

# -----------------------------------
# 
# #### Problem 4:
# 
# Implement the function `encryptRSA(message, n, e)` which encrypts a string `message` using RSA key `(n = p * q, e)`.  You may NOT use any built-in functions as part of your implementation, but you may use any functions you implemented for previous coding assignments.  Please make sure to copy and paste them into this file, so that they are uploaded to CodePost when you submit your `pa3.py` file.

def encryptRSA(message, n, e):
    """encrypts the plaintext message, using RSA and the key (n = p * q, e)
    INPUT:  message - plaintext as a string of letters
            n - a positive integer
            e - integer satisfying gcd((p-1)*(q-1), e) = 1
            
    OUTPUT: The encrypted message as a string of digits
    """
    #initial values that will be used in various place of the code
    l = blocksize(n) #length of n which will serve as the blocksize
    slice = [] #the slice of each message in number form with lengths of n
    ls = [] #all the slices stored in a list
    encrypt = '' #the final encrypted string
    number = '' #holds the string form of the slice
    
    message_numbers = letters2digits(message)
    
    while True: #cushions if all block sizes don't equal the length of n (l)
        if (len(message_numbers) % l != 0):
            message_numbers += '23' #adds X (23) to cushion string
        else:
            break
    
    for i in message_numbers: #divides the translated message into l blocks
        slice.append(i)
        if (len(slice) % l == 0):
            ls.append(slice)
            slice = []
            
    for block in ls: #encodes each block and appends it to string
        if (len(number) == l):
            x = int(number)
            number = ''
            t = str(mod_exp(x, e, n))
            while (len(t) % l != 0): #if the length of the block is not equal to l add a 0 to the front until it is
                t = f'0{t}'
            encrypt += t
            encrypt += ' '
        for item in block:
            number += item
            
    x = int(number) #translates final block that isn't captured in loop
    t = str(mod_exp(x, e, n))
    while (len(t) % l != 0):
        t = f'0{t}'
    encrypt += t
           
    return encrypt

'''
"""--------------------- ENCRYPTION TESTER CELL ---------------------------"""
encrypted1 = encryptRSA("STOP", 2537, 13)
encrypted2 = encryptRSA("HELP", 2537, 13)
encrypted3 = encryptRSA("STOPS", 2537, 13)
print("Encrypted Message:", encrypted1)
print("Expected: 2081 2182")
print("Encrypted Message:", encrypted2)
print("Expected: 0981 0461")
print("Encrypted Message:", encrypted3)
print("Expected: 2081 2182 1346")


"""--------------------- TEST 2 ---------------------------"""
encrypted = encryptRSA("UPLOAD", 3233, 17)
print("Encrypted Message:", encrypted)
print("Expected: 2545 2757 1211")
'''

# -------------------------------------------------------
# 
# #### Problem 5:
# 
# Complete the implementation of the function `decryptRSA(c, p, q, m)` which depends on `modinv(a,m)` and the given functions `digits2letters(digits)` and `blockSize(n)`.  When you are done, you can test your function against the given examples.

def decryptRSA(cipher, p, q, e):
    """decrypts cipher, which was encrypted using the key (p * q, e)
    INPUT:  cipher - ciphertext as a string of digits
            p, q - prime numbers used as part of the key n = p * q to encrypt the ciphertext
            e - integer satisfying gcd((p-1)*(q-1), e) = 1
            
    OUTPUT: The decrypted message as a string of letters
    """
    n = p * q
    e_bar = modinv(e, (p - 1) * (q - 1))
    l = blocksize(n)
    ls = []
    slice = ''
    decrypt = ''
    
    for number in cipher:
        if (number == ' '):
            continue
            
        if (len(slice) == l):
            ls.append(slice)
            slice = ''
            slice += number
        else:
            slice += number
    ls.append(slice)
    
    for number in ls:
        x = int(number)
        p = str(mod_exp(x, e_bar, n))
        while (len(p) % l != 0):
            p = f'0{p}'
        decrypt += p
        
    return digits2letters(decrypt)

'''
"""--------------------- TESTER CELL ---------------------------"""
decrypted1 = decryptRSA("2081 2182", 43, 59, 13)
decrypted2 = decryptRSA("0981 0461", 43, 59, 13)
decrypted3 = decryptRSA("2081 2182 1346", 43, 59, 13)
print("Decrypted Message:", decrypted1)
print("Expected: STOP")
print("Decrypted Message:", decrypted2)
print("Expected: HELP")
print("Decrypted Message:", decrypted3)
print("Expected: STOPSX")

"""--------------------- TEST 2---------------------------"""
decrypted = decryptRSA("0667 1947 0671", 43, 59, 13)
print("Decrypted Message:", decrypted)
print("Expected: SILVER")
'''