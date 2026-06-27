async function getRecommendation(){


let data = await apiCall(

"/recommendation",

"GET"

);



document.getElementById(
"recommendationBox"
).innerHTML = `


<h3>
${data.title || "Smart Saving Tips"}
</h3>


<p>

${data.message || 
"Track your expenses daily and save at least 20% of your income."}

</p>



`;


}




window.onload =
getRecommendation;