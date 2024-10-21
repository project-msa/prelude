from Crypto.Util.number import *

class ECC:
    ## y^2 = x^3 + ax + b (mod p)
    def __init__(self, p, coeffs):
        ## ensure that coeffs is a list
        if not isinstance(coeffs, list):
            raise TypeError("(second argument) coeffs should be a list")

        ## check if p is prime
        if not isPrime(p):
            raise ValueError("(first argument) p should be a prime")
        
        self.p = p
        self.a = self.b = 0 

        if len(coeffs) == 2:
            self.a, self.b = map(lambda x: x % self.p, coeffs)
        else:
            raise ValueError("coeffs must have either 2 elements")

    def __str__(self):
        left = []
        right = []

        # Left-hand side (y^2)
        left.append("y^2")

        # Right-hand side (x^3 + a * x + b)
        right.append("x^3")
        if self.a != 0:
            right.append(f"{self.a} * x")
        if self.b != 0:
            right.append(f"{self.b}")

        left_side = " + ".join(left)
        right_side = " + ".join(right)

        return f"{left_side} = {right_side} (mod {self.p})"

class Point:
    def __init__(self, x, y, E, inf=0):
        ## sanity checks
        if not isinstance(E, ECC):
            raise TypeError("E passed must be an object of the class ECC")
 
        self.x = x % E.p
        self.y = y % E.p
        self.inf = inf
        self.ecc = E
        self.a = E.a 
        self.b = E.b
        self.p = E.p

        ## lies on curve check 
        if inf == 0 and pow(self.y, 2, self.p) != (pow(self.x, 3, self.p) + self.a * self.x + self.b) % self.p:
            raise AssertionError(f"Point does not lie on the curve {str(E)}")

    def __str__(self):
        return f"Point({self.x}, {self.y}) on the curve: {str(self.ecc)}"

    def __add__(self, other):
        ## sanity checks
        if self.p != other.p or \
            self.a != other.a or \
            self.b != other.b:
            raise Exception("incompatible points cannot be added")
        
        ## identity checks
        if self.inf == 1 and other.inf == 1:
            return self
        if self.inf == 1:
            return other 
        if other.inf == 1:
            return self

        ## point doubling
        if self.x != other.x:
            lamb = ((other.y - self.y) * pow((other.x - self.x), -1, self.p)) % self.p
        else:
            if self.y == (other.p - other.y) % other.p:
                return Point(0, 0, self.ecc, inf=1)
            if self.y == 0:
                return Point(0, 0, self.ecc, inf=1)

            lamb = ((3 * self.x ** 2 + self.a) * (pow(2 * self.y, -1, self.p))) % self.p
        
        x1 = (lamb ** 2 - self.x - other.x) % self.p 
        y1 = ((self.x - x1) * lamb - self.y) % self.p

        return Point(x1, y1, self.ecc)
    
    def __neg__(self):
        return Point(self.x, self.p - self.y, self.ecc)
    
    def __sub__(self, other):
        return self + (-other)

    def __mul__(self, k):
        result = Point(0, 0, self.ecc, 1)
        temp = self 

        while k > 0:
            if k & 1:
                result = result + temp 
            temp = temp + temp 
            k >>= 1 
        
        return result 
    
    def __rmul__(self, k):
        return self * k
    
    