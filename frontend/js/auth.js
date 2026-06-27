// REGISTER FUNCTION

async function register(){


    let name = document.getElementById("name").value;

    let email = document.getElementById("email").value;

    let password = document.getElementById("password").value;



    try{


        let result = await apiCall(

            "/users/register",

            "POST",

            {
                name:name,
                email:email,
                password:password
            }

        );



        console.log(result);



        if(result.message){


            alert("Account Created Successfully");


            window.location.href = "login.html";


        }
        else{


            alert("Registration Failed");


        }



    }
    catch(error){


        console.log(error);

        alert("Server Error");


    }


}







// LOGIN FUNCTION


async function login(){


    let email = document.getElementById("email").value;


    let password = document.getElementById("password").value;



    try{


        let result = await apiCall(

            "/users/login",

            "POST",

            {
                email:email,
                password:password
            }

        );



        console.log(result);



        if(result.access_token){


            localStorage.setItem(

                "token",

                result.access_token

            );



            localStorage.setItem(

                "user",

                JSON.stringify(result.user)

            );



            alert("Login Successful");


            window.location.href =
            "dashboard.html";


        }
        else{


            alert("Invalid Email or Password");


        }



    }
    catch(error){


        console.log(error);


        alert("Login Failed");


    }


}






// LOGOUT FUNCTION


function logout(){


    localStorage.removeItem("token");

    localStorage.removeItem("user");


    window.location.href="login.html";


}