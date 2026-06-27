const API_URL = "http://127.0.0.1:8000";


async function apiCall(endpoint, method = "GET", data = null) {


    let options = {

        method: method,

        headers: {

            "Content-Type": "application/json"

        }

    };


    let token = localStorage.getItem("token");


    if(token){

        options.headers["Authorization"] =
        "Bearer " + token;

    }



    if(data){

        options.body = JSON.stringify(data);

    }



    try {


        let response = await fetch(
            API_URL + endpoint,
            options
        );


        let result = await response.json();


        console.log(result);


        return result;


    }
    catch(error){


        console.log(error);

        throw error;

    }


}