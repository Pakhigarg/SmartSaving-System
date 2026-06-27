// Expense Pie Chart


const expense = document
.getElementById("expenseChart");


new Chart(expense, {


type:"doughnut",


data:{


labels:[

"Food",
"Travel",
"Shopping",
"Bills"

],


datasets:[{

data:[

30,
20,
25,
25

]


}]


},


options:{


responsive:true


}



});







// Saving Chart


const saving = document
.getElementById("savingChart");



new Chart(saving,{


type:"bar",


data:{


labels:[

"Jan",
"Feb",
"Mar",
"Apr",
"May"

],


datasets:[{

label:"Savings",

data:[

10000,
15000,
12000,
20000,
30000

]


}]


}



});









// AI Recommendation


let tips=[

"Your food expense is high. Try saving ₹2000 this month.",

"Great job! Your saving rate is improving 🚀",

"Reduce unnecessary shopping expenses.",

"Create a new goal to improve saving habits."

];



let randomTip =
tips[Math.floor(Math.random()*tips.length)];



document.getElementById(
"recommendation"
).innerHTML=randomTip;