# Computes the Greatest Common Divisor (GCD) of two integers using the Euclidean algorithm.
# Parameters: a (int), b (int)
# Returns: int - the GCD of a and b
def gcd(a,b):
    if(b == 0): return a
    return gcd(b,a%b)

# A higher-order function that composes two single-input functions f and g, such that (port(g)(f))(x) = f(g(x)).
# Parameters: g (function) - a single-input function
# Returns: function - a function that takes another function f and returns a lambda that applies f to g(num)
def port(g): # f,g must be a single input function
    def output(f):
        return lambda num: f(g(num))
    return output

# Checks if a number or a pair of numbers (in a nested structure) equals 1.
# Parameters: num (int or object with attributes a and b)
# Returns: bool - True if num is 1 or both num.a and num.b are 1, False otherwise
def isone(num):
    if isinstance(num,int): return num == 1
    return isone(num.a) and isone(num.b)

# Converts various input types (bool, int, float, Frac) to a Frac object.
# Parameters: num (bool, int, float, or Frac)
# Returns: Frac - a simplified fraction representing the input
def tofrac(num):
    if isinstance(num,bool):
        # num is a type of integer
        return Frac(1,1) if num else Frac(0,1)
    elif isinstance(num,int): 
        return Frac(num,1)

    elif isinstance(num,float):
        sign = num/abs(num)
        d = str(abs(num)).split('.')
        denom = (10**len(d[1]))
        d = list(map(int,d))
        return Frac(d[0]*denom+d[1],sign*denom)
    
    elif isinstance(num,Frac): return num.sim()
    
    else: return Frac(1,1)

# A class representing a fraction with optional root (exponent) support.
class Frac:
    # Initializes a fraction with numerator a, denominator b, and optional exponent r.
    # Parameters: a (int) - numerator, b (int) - denominator, r (int, Frac, or None) - exponent
    # Simplifies the fraction and handles the exponent r.
    def __init__(self, a, b, r = None):
        self.a = a
        self.b = b
        self.sim()
        if r == None: 
            self.r = 1

        elif r == 0:
            self.a = 1
            self.b = 1
            self.r = 0

        elif isinstance(r,int):
            self.a, self.b = self.a**r, self.b**r
            self.r = 1
        
        else: 
            self.r = tofrac(r)
            #self.a, self.b = self.a**self.r.a,self.b**self.r.a
            #self.r = Frac(1,self.r.b)

    # Converts the exponent r to a Frac object.
    # Returns: Frac - the exponent as a fraction
    def rr(self): return tofrac(self.r)
    def isroot(self): return self.b != 1
    def sim(self):
        factor = gcd(self.a,self.b)
        self.a = int(self.a/factor)
        self.b = int(self.b/factor)
        return self

    # Prints the fraction in a readable format, including the exponent if not 1.
    # Returns: Frac - self, for method chaining
    def log(self):
        tosfrac = lambda a,b : f"({a}"+f"/{b}"*(b != 1)+")"
        info = f"{tosfrac(self.a,self.b)}"
        info += (not isone(self.rr()))*f"^{tosfrac(self.rr().a,self.rr().b)}"
        print(info)
        return self
    
    # Defines arithmetic operations (+, -, *, /, ^) between this fraction and another.
    # Parameters: opr (str) - the operation to perform ('+', '-', '*', '/', '^')
    # Returns: function - a function that takes another Frac and performs the operation
    def op(self,opr):
        frac1 = self
        f2frac = port(lambda x: tofrac(x))
        opr2frac = {
            '+': f2frac(lambda frac2: Frac(frac1.a*frac2.b + frac1.b*frac2.a,frac1.b*frac2.b,frac1.r)),
            '-': f2frac(lambda frac2: Frac(frac1.a*frac2.b - frac1.b*frac2.a,frac1.b*frac2.b,frac1.r)),
            '*': f2frac(lambda frac2: Frac(frac1.a*frac2.a,frac1.b*frac2.b,frac1.r)),
            '/': f2frac(lambda frac2: Frac(frac1.a*frac2.b,frac1.b*frac2.a,frac1.r)),
            '^': f2frac(lambda frac2: Frac(frac1.a,frac1.b,frac1.rr().op('*')(frac2)))
        }
        # ^ only allows whole integer so far
        
        return opr2frac[opr]

# Test cases demonstrating the functionality of the Frac class and related functions
print(isone(Frac(4,2)), isone(1))           # Checks if Frac(4,2) (simplifies to 2) and 1 are equal to 1
Frac(True,False).op('+')(Frac(5,2)).log()   # Adds Frac(1,1) (True) and Frac(5,2), prints result
Frac(5,5).log()                             # Prints simplified Frac(5,5) (i.e., 1)
f1 = Frac(-1,2,Frac(4,5)).op('^')(5).log()  # Creates Frac(-2,10) with exponent Frac(4,5), prints it
print('-')
f1 = f1.op('+')(Frac(-3,13)).log()          # Adds Frac(-3,13) to f1, prints result
Frac(-28,65).op('+')(Frac(+3,13)).log()     # Adds Frac(-28,65) and Frac(3,13), prints result
print(f1.a,f1.b)                            # Prints numerator and denominator of f1
f1 = f1.op('+')(Frac(+3,13)).log()          # Adds Frac(3,13) to f1, prints result
Frac(1,2).op('+')(Frac(1,5)).op('+')(Frac(-1,5)).log()  
Frac(1,2).op('+')(True).op('+')(False).log()
Frac(1,2).op('*')(Frac(1,2)).op('/')(Frac(1,2)).log()  