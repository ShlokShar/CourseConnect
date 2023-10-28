
var method;

function createPracticeProblem() {
    // get selected subject for practice problem
    let selectObject = document.getElementById("subject");
    let chatroomId = selectObject.options[selectObject.selectedIndex].getAttribute("chatroomId");

    // tell the user the problem is being created
    document.getElementById("main").innerHTML = `
            <h1>...</h1>
            <h1>Your practice problem is being created...</h1>
            <h2>You can exit this page or wait for the problem to fully load</h2>
    `

    // tell the python file to create a practice problem
    fetch(`/create-practice-problem/${chatroomId}`)
        .then(response => {
            return response.json();
        }).then(data => {
            // tell the user the practice problem has been created
            document.getElementById("main") = `
            <h1>Your practice problem has been created</h1>
            <h2>View it <a href="/practice-problems">here</a></h2>
            `
        })
}

function switchMethod(newMethod) {
    method = newMethod;

}

function submitAnswer(practiceProblemId) {
    let practiceProblemObject = document.getElementById(practiceProblemId);
    let chatroomId = practiceProblemObject.getAttribute("chatroomId")
    let userAnswer = document.getElementById(practiceProblemId + "Answer").value;
    let question = document.getElementById(practiceProblemId + "Question").innerHTML;

    practiceProblemObject.innerHTML = `
    <div class="bg-yellow-500 w-full p-3 rounded-t-3xl">
        <p class="text-yellow-800 font-bold text-lg">GRADING</p>
    </div>
    <div class="flex flex-col space-y-1 px-2 pt-1 pb-3 text-sm h-full justify-between">
        <p>${question}</p>
        <br>
        <div class="flex flex-row space-x-1">
            <input id="{{ practice_problem.id }}Answer" placeholder="${userAnswer}" disabled="disabled" class=" w-full outline outline-yellow-500 rounded-3xl px-2">
        </div>
    </div>
    `

    fetch(`/submit-practice-problem/${practiceProblemId}/${chatroomId}/${userAnswer}`)
        .then(response=> {
            return response.json()
        })
        .then(data => {
        })
}
