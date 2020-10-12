"""
Ethan Paek
TA: Rachael Brooks
COEN 150L - Tuesdays 2:15 PM - 5:00 PM
6 October 2020
Lab 2
"""

from math import floor

from pip._vendor.msgpack.fallback import xrange

n = 12499013
e = 757
ciphertext = [8551637, 11944571, 5524159, 7674054, 5512257, 4858965, 5636066, 7674054, 738529, 11822690, 6031508,
              1824153, 5610715, 1824153]

# Step 1: find the prime values (p and q) from n and the given text file

# get all the numbers into a local list
primes = []
f1 = open("RSALabPrimes.txt", "r")
for number in f1:
    primes.append(int(number.strip('\n')))
f1.close()

p = 0
q = 0
# figure out which numbers multiply to n
for i in range(len(primes) - 1):
    for j in range(i+1, len(primes)):
        if primes[i] * primes[j] == n:
            p = primes[i]
            q = primes[j]
            break

# quit if we can't find the primes
if p == 0 and q == 0:
    print("We couldn't find the primes dawg. Idk what happened!")
    exit(1)

print("Value of p:", p)
print("Value of q:", q)

# calculate the value of Phi(n)
phi_n = (p - 1) * (q - 1)
print("Value of Phi(n):", phi_n)


# Step 2: Use the Extended Euclidean Algorithm to find d
def find_d(pub_exp, modulus):
    """
    This function will execute the Extended Euclidean Algorithm and return the value of d
    :param pub_exp: e
    :param modulus: phi(n)
    :return: d, the private key; the modular multiplicative inverse of e
    """

    A = [1, 0, modulus]
    B = [0, 1, pub_exp]

    while True:
        # return GCD(phi_n, e) and there is no inverse
        if B[2] == 0:
            print("There is no inverse!")
            return A[2]

        # return GCD(phi_n, e) and B[1] which is the inverse of e
        if B[2] == 1:
            print("Found the inverse!")
            return B[1]

        Q = floor(A[2] / B[2])
        T = [A[0] - (Q * B[0]), A[1] - (Q * B[1]), A[2] - (Q * B[2])]
        A = B
        B = T


# d is the inverse of e so we just need to mod it to get its proper value
d = find_d(e, phi_n)
d = d % phi_n
print("Value of d:", d)

# Step 3: decrypt each of our ciphertexts
plaintext = []
for word in ciphertext:
    m = 1
    for i in xrange(d):
        m = (m * word) % n
    plaintext.append(m)

print("Deciphered ASCII values:", plaintext)

# translate ASCII values to corresponding characters
res = ""
for val in plaintext:
    res = res + chr(val)

print("Resultant string:", str(res))
