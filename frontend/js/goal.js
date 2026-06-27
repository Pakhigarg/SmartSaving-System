let goals=[];



function addGoal(){


let goal={


name:
document.getElementById("goalName").value,


target:
Number(
document.getElementById("targetAmount").value
),


saved:
Number(
document.getElementById("savedAmount").value
)


};



goals.push(goal);


displayGoals();


}




function displayGoals(){


let box =
document.getElementById("goalList");



box.innerHTML="";



goals.forEach((g)=>{


let progress =
(g.saved/g.target)*100;



box.innerHTML += `


<div class="card">


<h3>
🎯 ${g.name}
</h3>


<p>
Target:
₹${g.target}
</p>


<p>
Saved:
₹${g.saved}
</p>



<div class="progress">

<div 
style="
width:${progress}%
"
id="progressBar">

</div>

</div>


<p>

${progress.toFixed(0)}% Completed

</p>


</div>


`;



});


}