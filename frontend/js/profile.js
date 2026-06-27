async function loadProfile(){


let user = await apiCall(

"/user/profile",

"GET"

);



document.getElementById(
"userName"
).innerHTML =
user.name;



document.getElementById(
"userEmail"
).innerHTML =
user.email;



}




async function updateProfile(){


let name =
prompt(
"Enter New Name"
);



if(name){


await apiCall(

"/user/profile",

"PUT",

{
name:name
}

);



alert(
"Profile Updated"
);



loadProfile();


}


}




window.onload =
loadProfile;