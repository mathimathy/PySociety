import random
class RSA:
    def __init__(self):
        self.public=None
        self.private=None

    def cipher(self,data,key):
        try:
            return pow(data,key[1], key[0])
        except:
            data = int("0x"+"".join([hex(ord(char)) for char in data]).replace("0x", ""), 16)
            return pow(data, key[1],key[0])

    def decipher(self,data,key):
        try:
            return pow(data,key[1], key[0])
        except:
            data = int("0x"+"".join([hex(ord(char)) for char in data]).replace("0x", ""), 16)
            return pow(data, key[1],key[0])
    
    def createKey(self, size=256):
        p = self.generatePrime(size)
        q = self.generatePrime(size)
        n = p*q
        phi = (p-1)*(q-1)
        e = self.generatePrimeWith(phi)
        d=self.eucl(e,phi)[1]
        self.public = (n,e)
        self.private=(n,d)
    
    def eucl(self, a, b):
        r, u, v, rp, up, vp = a, 1, 0, b, 0, 1
        while rp!=0:
            q=r//rp
            r, u, v, rp, up, vp = rp, up, vp, r-q*rp, u-q*up, v-q*vp
        return (r,u,v)

    def generatePrimeWith(self, number):
        for prime in self.generateFirstPrimes(100):
            if number%prime!=0:
                return prime

    def generatePrime(self, bit):
        while True:
            n = self.getLowLevelPrime(bit)
            if self.getHighLevelPrime(n):
                return n
    
    def nBitNumber(self, bit):
        return random.randrange(2**(bit-1)+1, 2**bit-1,2)

    def getLowLevelPrime(self, bit):
        number = self.nBitNumber(bit)
        for prime in self.generateFirstPrimes(400):
            if number%prime==0 and prime*prime<=number:
                break
            else:
                return number
        
    def getHighLevelPrime(self, number):
        maxDivisionsByTwo = 0
        evenComponent = number-1
    
        while evenComponent % 2 == 0: 
            evenComponent >>= 1
            maxDivisionsByTwo += 1
        assert(2**maxDivisionsByTwo * evenComponent == number-1) 
    
        def trialComposite(round_tester): 
            if pow(round_tester, evenComponent,  
                number) == 1: 
                return False
            for i in range(maxDivisionsByTwo): 
                if pow(round_tester, 2**i * evenComponent, 
                    number) == number-1: 
                    return False
            return True
    
        numberOfRabinTrials = 20
        for _ in range(numberOfRabinTrials): 
            round_tester = random.randrange(2, 
                        number) 
            if trialComposite(round_tester): 
                return False
        return True


    def generateFirstPrimes(self, high):
        primes = [True for _ in range(high+1)]
        prime=2
        while prime*prime<=high:
            if primes[prime]:
                for i in range(prime*prime, high+1, prime):
                    primes[i]=False
            prime+=1
        return [primeNumber for primeNumber in range(high+1) if primes[primeNumber]][2:]