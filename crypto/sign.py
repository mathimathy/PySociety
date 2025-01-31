from crypto import rsa, hash
class Sign:
    def __init__(self, createKey=True, public=None,private=None):
        self.rsa = rsa.RSA()
        if createKey:
            self.rsa.createKey()
        else:
            self.rsa.public = public
            self.rsa.private = private        

    def sign(self, msg):
        hashedMsg = hash.sha256(msg)
        signed = self.rsa.cipher(hashedMsg, self.rsa.private)
        return signed
    
    def checkSign(self, msg, signed):
        hashedMsg = hash.sha256(msg)
        unsigned = self.rsa.decipher(signed, self.rsa.public)
        return hashedMsg==unsigned