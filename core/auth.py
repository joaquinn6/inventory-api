from datetime import datetime, timedelta

from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from jose import JWTError, jwt
from passlib.context import CryptContext

from core.var_env import ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY
import core.var_mongo_provider as mongo_provider

ALGORITHM = "HS256"


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/")


def verify_password(plain_password, password):
  return pwd_context.verify(plain_password, password)


def get_password_hash(password):
  return pwd_context.hash(password)


def get_user(email: str):
  return mongo_provider.db.users.find_one({'email': email})


def authenticate_user(email: str, password: str):
  user = get_user(email)
  if not user:
    return False
  if not verify_password(password, user['password']):
    return False
  return user


def create_access_token(data: dict):
  to_encode = data.copy()
  expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
  to_encode['expire'] = expire.strftime("%Y-%m-%dT%H:%M:%S.%f")
  encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
  return encoded_jwt


def generate_token(email, password):
  user = authenticate_user(email, password)
  if not user:
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect email or password",
        headers={"WWW-Authenticate": "Bearer"},
    )
  return create_access_token(
      data={'extra_data': {
          'email': user['email'],
          'roles': user['roles']
      }
      }
  )


async def get_current_user(token: str):
  credentials_exception = HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Could not validate credentials",
      headers={"WWW-Authenticate": "Bearer"},
  )
  try:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    email: str = payload['extra_data']
    if email is None:
      raise credentials_exception
  except JWTError:
    raise credentials_exception

  user = get_user(email)
  if user is None:
    raise credentials_exception
  return user


def is_admin(token: str):
  payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
  roles: list = payload['str']
  return 'AMDIN' in roles


def is_sales(token: str):
  payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
  roles: list = payload['str']
  return 'SALES' in roles


def is_manager(token: str):
  payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
  roles: list = payload['str']
  return 'MANAGER' in roles
