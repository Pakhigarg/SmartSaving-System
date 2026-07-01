from fastapi import APIRouter, HTTPException

from src.database.mongodb import users_collection

from src.schemas.user_schema import (
    UserRegister,
    UserLogin
)

from src.utils.security import (
    hash_password,
    verify_password,
    create_token
)



router = APIRouter()



@router.post("/register")
def register(user:UserRegister):


    existing_user = users_collection.find_one(
        {
            "email":user.email
        }
    )


    if existing_user:

        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )


    new_user={

        "name":user.name,

        "email":user.email,

        "password":
        hash_password(user.password)

    }


    users_collection.insert_one(
        new_user
    )


    return {

        "message":
        "User Registered Successfully"

    }





@router.post("/login")
def login(user:UserLogin):


    db_user = users_collection.find_one(
        {
            "email":user.email
        }
    )


    if not db_user:

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )



    if not verify_password(
        user.password,
        db_user["password"]
    ):

        raise HTTPException(
            status_code=401,
            detail="Wrong Password"
        )



    token=create_token({

        "email":user.email

    })


    return {

        "access_token":token,

        "token_type":"bearer"

    }