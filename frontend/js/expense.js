let expenseChart;



async function addExpense(){


    let expense = {

        title: document.getElementById("title").value,

        amount:parseFloat(
            document.getElementById("amount").value
        ),

        category:
        document.getElementById("category").value,

        date:
        document.getElementById("date").value

    };



    if(!expense.title || !expense.amount){

        alert("Please fill all details");

        return;

    }



    try{


        await apiCall(

            "/expenses",

            "POST",

            expense

        );


        alert("Expense Added Successfully");


        loadExpenses();


    }
    catch(error){

        console.log(error);

        alert("Server Error");

    }

}







async function loadExpenses(){


    let expenses = await apiCall(

        "/expenses",

        "GET"

    );



    let table =
    document.getElementById("expenseList");



    table.innerHTML="";



    let food=0;
    let travel=0;
    let shopping=0;
    let bills=0;



    expenses.forEach((e)=>{


        table.innerHTML += `


        <tr class="expense-row">


        <td>
        ${e.title}
        </td>

        <td>
₹ ${Number(e.amount).toLocaleString("en-IN")}
</td>


        <td>
        ${e.category}
        </td>


        <td>

        <button 
        onclick="deleteExpense('${e._id}')">

        Delete

        </button>

        </td>


        </tr>


        `;



        if(e.category=="Food")
        food += e.amount;


        if(e.category=="Travel")
        travel += e.amount;


        if(e.category=="Shopping")
        shopping += e.amount;


        if(e.category=="Bills")
        bills += e.amount;



    });



    createChart(
        food,
        travel,
        shopping,
        bills
    );


}








async function deleteExpense(id){


    await apiCall(

        "/expenses/"+id,

        "DELETE"

    );


    loadExpenses();


}







function createChart(
food,
travel,
shopping,
bills
){


const ctx =
document.getElementById(
"expenseChart"
);



if(expenseChart)
expenseChart.destroy();



expenseChart = new Chart(ctx,{


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

food,
travel,
shopping,
bills

]

}]

}


});


}







window.onload =
loadExpenses;