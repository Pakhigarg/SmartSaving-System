from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta


pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


SECRET_KEY = "budgetbuddy_secret"
ALGORITHM = "HS256"



def hash_password(password):

    return pwd_context.hash(password)



def verify_password(password, hashed_password):

    return pwd_context.verify(
        password,
        hashed_password
    )



def create_token(data):

    expire = datetime.utcnow() + timedelta(days=1)

    data.update({
        "exp":expire
    })


    token = jwt.encode(
        data,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return token
def decode_token(token):
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        return payload

    except:
        return None