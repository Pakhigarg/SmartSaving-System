from src.database import users_collection



def create_user(user_data: dict):

    result = users_collection.insert_one(user_data)

    return {

        "message": "User created successfully",

        "user_id": str(result.inserted_id)

    }




def get_all_users():

    users = []


    for user in users_collection.find():

        user["_id"] = str(user["_id"])

        users.append(user)


    return users





def find_user(email, password):


    user = users_collection.find_one(

        {
            "email": email,
            "password": password
        }

    )


    if user:


        user["_id"] = str(user["_id"])


        return user



    return None