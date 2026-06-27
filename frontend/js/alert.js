async function loadAlerts(){


let alerts = await apiCall(

"/alerts",

"GET"

);



let box =
document.getElementById("alertBox");



box.innerHTML="";



alerts.forEach(alert=>{


box.innerHTML += `


<div class="alert-card">


<h3>

${alert.type}

</h3>


<p>

${alert.message}

</p>


</div>


`;


});


}




window.onload =
loadAlerts;