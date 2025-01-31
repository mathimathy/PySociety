from pprint import pprint
def chainMod(msg, turn=20, mod=256, reverse=False):
        data = [ord(letter) for letter in msg]
        lastNumber = 1
        for _ in range(turn):
            newData=[]
            for el in data:
                newData.append((el*lastNumber)%mod)
                lastNumber=el
            if reverse: data=newData[::-1]
        return abs(sum(data)%mod)

def rotr(n, amount):
    return n[-amount:]+n[:-amount]
def shr(n, amount):
	return "".join(["0" for _ in n[-amount:]])+n[:-amount]
def xor(*args):
	result=0
	for n in args:
		result^=int("0b"+n,2)
	result=resize(bin(result%(2**32))[2:])
	return result

def add(*args):
	result=0
	for n in args:
		result+=int("0b"+n,2)
	result=resize(bin(result%(2**32))[2:])
	return result

def init(m):
	binary = "".join([resize(bin(ord(char))[2:],8) for char in m])
	i=512
	while i<len(resize(binary)):
		i+=512
		
	size = len(binary)
	sizeB = bin(size)[2:]
	binary+="1"+"".join(["0" for _ in range(i-(1+size+len(sizeB)))])+sizeB
	words=[[binary[i:i+512][j:j+32] for j in range(0, 512, 32)] for i in range(0, len(binary), 512)]
	return words
def sigma0(w):
	return xor(rotr(w,7),rotr(w,18), shr(w,3))
def sigma1(w):
	return xor(rotr(w,17), rotr(w,19), shr(w,10))
def Ch(a,b,c):
	return resize(bin(int(a,2)&int(b,2)^(~int(a,2))&int(c,2))[2:])
def Maj(a,b,c):
	return resize(bin((int(a,2)&int(b,2))^(int(a,2)&int(c,2))^(int(b,2)&int(c,2)))[2:])
def SIGMA0(w):
	return xor(rotr(w,2),rotr(w,13),rotr(w,22))
def SIGMA1(w):
	return xor(rotr(w,6),rotr(w,11),rotr(w,25))
def resize(w, l=32):
	return "".join(["0" for _ in range(l-len(w))])+w
def compute2(W,i):
	H=[[0x6a09e667,0xbb67ae85,0x3c6ef372,0xa54ff53a,0x510e527f,0x9b05688c,0x1f83d9ab,0x5be0cd19]]
	K=[0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2]
	a=resize(bin(H[i-1][0])[2:])
	b=resize(bin(H[i-1][1])[2:])
	c=resize(bin(H[i-1][2])[2:])
	d=resize(bin(H[i-1][3])[2:])
	e=resize(bin(H[i-1][4])[2:])
	f=resize(bin(H[i-1][5])[2:])
	g=resize(bin(H[i-1][6])[2:])
	h=resize(bin(H[i-1][7])[2:])
	for t in range(64):
		T1=add(h,SIGMA1(e),Ch(e,f,g),resize(bin(K[t])[2:]),W[t])
		T2=add(SIGMA0(a),Maj(a,b,c))
		h=g
		g=f
		f=e
		e=add(d,T1)
		d=c
		c=b
		b=a
		a=add(T1,T2)
	H.append([int(a,2)+H[-1][0],int(b,2)+H[-1][1],int(c,2)+H[-1][2],int(d,2)+H[-1][3],int(e,2)+H[-1][4],int(f,2)+H[-1][5],int(g,2)+H[-1][6],int(h,2)+H[-1][7]])
	return H

def compute(M):
	for i in range(1,len(M)+1):
		W=M[i-1]
		for t in range(16,64):
			W.append(add(sigma1(W[t-2]), W[t-7], sigma0(W[t-15]),W[t-16]))
		H=compute2(W,i)
	return int("0b"+(bin(H[-1][0])+bin(H[-1][1])+bin(H[-1][2])+bin(H[-1][3])+bin(H[-1][4])+bin(H[-1][5])+bin(H[-1][6])+bin(H[-1][7])).replace("0b", ""),2)

def sha256(msg):
	words=init(msg)
	return compute(words)