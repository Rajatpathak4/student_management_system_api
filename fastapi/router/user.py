from datetime import datetime, timedelta
from fastapi import Depends, APIRouter, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import get_db
import models
import jwt


SECRET_KEY = "1a31abc74f07155a7248058ba471fcad59a06a0a76aadac7f740a40b395e5b21"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

router = APIRouter(tags=["JWT_authentication"])


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")



def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def get_hashed_password(password: str):
    return pwd_context.hash(password)


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")


def get_user_by_email(email: str, db: Session):
    return db.query(models.User).filter(models.User.email == email).first()


def authenticate_user(email: str, password: str, db: Session):
    user = get_user_by_email(email, db)
    if user and verify_password(password, user.password_hash):
        return user
    return None






class UserCreate(BaseModel):
    # username: str
    email: str
    password: str
    role: str


class UserResponse(BaseModel):
    username: str
    email: str
    role: str




@router.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}





@router.post("/create_user")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    if get_user_by_email(user.email, db):
        raise HTTPException(status_code=400, detail="Username already exists")
    if db.query(models.User).filter(models.User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email already exists")
    
    hashed_password = get_hashed_password(user.password)
    new_user = models.User(email=user.email, password_hash=hashed_password, role= user.role)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"msg": "User created successfully"}





@router.get("/users", response_model=UserResponse)
def read_users_me(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    email = decode_token(token)
    user = get_user_by_email(email, db)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid user")
    return UserResponse( email=user.email, role=user.role)
