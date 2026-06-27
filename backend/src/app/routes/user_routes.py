from fastapi import APIRouter, HTTPException

from src.app.schemas.user_schema import UserSchema

from src.app.models.user_model import (
    create_user,
    get_all_users,
    find_user
)


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)



# Register

@router.post("/register")
def register(user: UserSchema):

    return create_user(
        user.model_dump()
    )



# Login

@router.post("/login")
def login(data: dict):

    user = find_user(
        data["email"],
        data["password"]
    )


    if user:

        return {

            "message":"Login Successful",

            "user":user,

            "access_token":"smart-saving-token"

        }


    raise HTTPException(

        status_code=401,

        detail="Invalid email or password"

    )



# Get all users

@router.get("/")
def read_users():

    return get_all_users()