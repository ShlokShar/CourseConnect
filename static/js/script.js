
var method;

function createPracticeProblem() {
    // get selected subject for practice problem
    let selectObject = document.getElementById("subject");
    let friend = selectObject.value;
    let friend_id = selectObject.options[selectObject.selectedIndex].getAttribute("friend_id");
    let subject = selectObject.options[selectObject.selectedIndex].getAttribute("id");

    // tell the user the problem is being created
    document.body.innerHTML = `
            <h1>...</h1>
            <h1>Your practice problem is being created...</h1>
            <h2>You can exit this page or wait for the problem to fully load</h2>
    `

    // tell the python file to create a practice problem
    fetch(`/create-practice-problem/${subject}/${friend_id}`)
        .then(response => {
            return response.json();
        }).then(data => {
            // tell the user the practice problem has been created
            document.body.innerHTML = `
            <h1>Your practice problem has been created</h1>
            <h2>View it here: </h2>
            `
        })
        .catch(error => {
            // in case of error...
            alert("An error occurred.. please try again.");
            location.reload();
        })
}

function switchMethod(newMethod) {
    method = newMethod;

}

function submitAnswer(practiceProblemId) {
    let practiceProblemObject = document.getElementById(practiceProblemId);
    let chatroomId = practiceProblemObject.getAttribute("chatroomId")
    let userAnswer = document.getElementById(practiceProblemId + "Answer").value;


    fetch(`/submit-practice-problem/${practiceProblemId}/${chatroomId}/${userAnswer}`)
        .then(response=> {
            return response.json()
        })
        .then(data => {
            alert("yoo")
        })
}
