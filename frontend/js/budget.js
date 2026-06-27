let budget = 0;


let expense = 0;



function setBudget(){


budget =
Number(
document.getElementById("budgetAmount").value
);



updateBudget();


}




function updateBudget(){


let remaining =
budget-expense;



document.getElementById(
"totalBudget"
).innerHTML=budget;



document.getElementById(
"spent"
).innerHTML=expense;



document.getElementById(
"remaining"
).innerHTML=remaining;



let percentage =
(expense/budget)*100;



document.getElementById(
"progressBar"
).style.width =
percentage+"%";



if(percentage>80){


document.getElementById(
"message"
).innerHTML =
"⚠ You are close to your budget limit";


}

else{


document.getElementById(
"message"
).innerHTML =
"Great! You are managing your money well";


}


}