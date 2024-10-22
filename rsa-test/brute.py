## Computing the time taken for a brute force prime factorization attack on RSA encrytion for different prime sizes

import time
from sympy.ntheory import factorint
from Crypto.Util.number import getPrime
import matplotlib.pyplot as plt

def generate_n(prime_size):
    p = getPrime(prime_size)  
    q = getPrime(prime_size)  
    n = p * q  
    return n, p, q

def factorize_rsa_modulus(n):
    start_time = time.time()  
    factors = factor(n) #replace factor with factorint if not using sage
    end_time = time.time()  
    factorization_time = end_time - start_time  
    return factors, factorization_time

prime_sizes = []
factorization_times = []

for prime_size in range(10, 100, 10): 
    print(f"Testing prime size: {prime_size}-bit")
    
    n, p, q = generate_n(prime_size)
    print(f"Generated RSA modulus n = p * q (p={p}, q={q}, n={n})")
    
    factors, time_taken = factorize_rsa_modulus(n)
    
    prime_sizes.append(prime_size)
    factorization_times.append(time_taken)
    print(f"Factorized n: {factors}")
    print(f"Time taken to factorize: {time_taken:.6f} seconds\n")

plt.plot(prime_sizes, factorization_times, marker='o', linestyle='-', color='b', label='Factorization Time')
plt.xlabel('Prime Size (bits)')
plt.ylabel('Time Taken to Factorize (seconds)')
plt.title('RSA Factorization Attack: Time to Factorize vs Prime Size')
plt.grid(True)
plt.legend()
plt.show()
