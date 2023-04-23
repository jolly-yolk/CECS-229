#!/usr/bin/env python
# coding: utf-8

# # CECS 229: Programming Assignment #1
# 
# #### Due Date: 
# 
# Sunday, 2/5 @ 11:59 PM
# 
# #### Submission Instructions:
# 
# To receive credit for this assignment, you must submit **to CodePost** this file converted to a Python script named `pa1.py`
# 
# #### Objectives:
# 
# 1. Compute the quotient and remainder of two numbers.
# 2. Apply numerical algorithms for computing the sum of two numbers in binary representation.
# 3. Apply numerical algorithms for computing the modular exponentiation of a positive integer.
# 
# 

# --------------------------------
# 
# #### Problem 1:
# 
# Program a function `div_alg(a, d)` that computes the quotient and remainder of $$a \div d$$ according to the Division Algorithm (THM 4.1.2).   
# 
# The function should satisfy the following:
# 
# 1. INPUT: 
#     * `a` - an integer representing the dividend
#     * `d` - positive integer representing the divisor
# 
#     
# 2. OUTPUT:
#     * a dictionary of the form `{'quotient' : q, 'remainder' : r}` where `q` and `r` are the quotient and remainder values, respectively.  The remainder should satisfy, $0 \leq r < d$.
# 
#  
# EXAMPLE: 
# 
# `>> div_alg( 101 , 11 )`
# 
# `{'quotient' : 9, 'remainder' : 2}`

def div_alg(a, d):
    # FIXME: Implement this function
    q = a // d
    r = a % d
    return {'quotient': q, 'remainder': r}

# --------------------------------
# 
# #### Problem 2:
# 
# Program a function `binary_add(a, b)` that computes the sum of the binary numbers  $$a = (a_{i-1}, a_{i-2}, \dots, a_0)_2$$ and $$b = (b_{j-1}, b_{j-2}, \dots, b_0)_2$$ using the algorithm discussed in lecture.  No credit will be given to functions that employ any other implementation.  The function can not use built-in functions that already perform some kind of binary representation or addition of binary numbers.  For example, the function implementation can **not** use the functions `bin()` or `int(a, base=2)`.
# 
# The function should satisfy the following:
# 
# 1. INPUT: 
#     * `a` - a string of the 0's and 1's that make up the first binary number.  The string *may* contain spaces.
#     * `b` - a string of the 0's and 1's that make up the first binary number.  The string *may* contain spaces.
# 
#     
# 2. OUTPUT:
#     * the string of 0's and 1's that is the result of computing $a + b$.  The string must be separated by spaces into blocks of 4 characters or less, beginning at the end of the string.
# 
#  
# EXAMPLE: 
# 
# `>> binary_add( '10 1011' , '11011')`
# 
# `'100 0110'`

def binary_add(a, b):
    #FIXME: Implement this method
    x = a.replace(' ', '') #gets rid of spaces
    y = b.replace(' ', '')
    temp = '' 
    result = ''
    carry = 0
    
    while (len(x) != len(y)): #adds a 0 to the beginning of the smallest string until both strings are equal
        if (len(x) < len(y)):
            w = x[::-1]
            w += '0'
            x = w[::-1]
        else:
            w = y[::-1]
            w += '0'
            y = w[::-1]

    for i in range(len(x) - 1, -1, -1): #adds the two binary numbers together
        if (carry == 0):
            r = int(x[i]) + int(y[i])
        else:
            r = int(x[i]) + int(y[i]) + carry
            carry -= 1
            
        if (r > 1):
            carry += 1
            if (r == 2):
                temp += '0'
                r = 0
                continue
            else:
                temp += '1'
                r = 0
                continue
                
        temp += str(r)
        
    if (carry == 1):
        temp += '1'
        
    temp = list(temp) #makes temporary string into list
    
    step = 4
    for i in range(0, len(temp), 4): #spaces the binary numbers into 4 characters each and adds them to string
        slice = temp[i:step]
        if (len(slice) == 4):
            for j in range(len(slice)):
                result += slice[j]
            result += ' '
        else:
            for j in range(len(slice)):
                result += slice[j]
        step += 4  
        
        
    return result[::-1] #returns reversed result string

# --------------------------------
# 
# #### Problem 3:
# 
# Program a function `mod_exp(b, n, m)` that computes $$b^n \mod m$$ using the algorithm discussed in lecture.  No credit will be given to functions that employ any other implementation.  For example, if the function implementation simply consists of `b ** n % m`, no credit will be given.  
# 
# The function should satisfy the following:
# 
# 1. INPUT: 
#     * `b` - positive integer representing the base
#     * `n` - positive integer representing the exponent
#     * `m` - positive integer representing the modulo
# 
#     
# 2. OUTPUT:
#     * the computation of $b^n \mod m$ if b, n, m are positive integers, 0 otherwise.
# 
#  
# EXAMPLE: 
# 
# `>> mod_exp( 3 , 644, 645 )`
# 
# `36`

def mod_exp(b, n, m):
    # FIXME: Implement this function
    if (n % 2 == 0):
        return ((b ** (n//2)) % m) * ((b ** (n//2)) % m) % m
    elif (n % 2 != 0):
        return((b ** (n - 1)) % m) * ((b ** (n - (n - 1)) % m)) % m