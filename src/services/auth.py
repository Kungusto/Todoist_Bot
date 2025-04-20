import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent))

from passlib.context import CryptContext

ACCESS_TOKEN_EXPIRE_MINUTES = 30

class AuthService :
    pwd_context = CryptContext(schemes=['pbkdf2_sha256'], deprecated='auto')    
    
    def hash_password(self, password: str) -> str : 
        return self.pwd_context.hash(password)        

    def verify_password(self, plain_password, hashed_password) -> bool : 
        return self.pwd_context.verify(plain_password, hashed_password)      