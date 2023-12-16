let total = 0;
let score = 0;;
let countdown = 5;

function hideForm() {

    let timer = setInterval(function () {
        countdown -= 1;

        if (countdown <= 0) {
            sendScore(total)
            clearInterval(timer);
            finalScore(total);
        }
    }, 1000);
}

function wordLength(arg) {
    return arg.length
}

function finalScore(total) {
    $(".form-container").hide();
    $(".message").hide();
    $(".score").hide();
    $(".total").addClass("heading").text(`Your final score is ${total}.`);
}

async function sendScore(total) {
    
    const response = await axios({
        url: "http://127.0.0.1:5000/score",
        method: "POST",
        data: { total }
    });

    high_score = response.data["high_score"]
    numOfTries = response.data["num_try"]

    $(".high_score").addClass("heading").text(`Your highest score is ${high_score}.`);
    $(".tries").addClass("heading").text(`You played the game ${numOfTries} number of time.`);
}

async function handleClick(e) {
    e.preventDefault()

    let input_guess = $(".input_guess").val();

    const response = await axios({
        url: "http://127.0.0.1:5000/guess",
        method: "GET",
        params: { input_guess }
    });

    console.log(response);

    $(".input_guess").val("");

    text = response.data["result"]

    if (text === "ok") {
        text = `Great ${input_guess.toUpperCase()} is a valid word and its on the board`;
        score = wordLength(input_guess)
        total += score
    } else if (text === "not-on-board") {
        text = `${input_guess.toUpperCase()} is not on the board`;
        score = 0;
    } else if (text == "not-word") {
        text = `${input_guess.toUpperCase()} does not exit`;
        score = 0;
    } else if (text === "already guessed") {
        text = `${input_guess.toUpperCase()} has already been guess`;
        score = 0;
    }

    $(".message").text(text);
    $(".score").text(`You scored ${score} for ${input_guess.toLocaleUpperCase()}.`);
    $(".total").text(`Your total is: ${total}`);
}

$("button").on("click", handleClick)

hideForm();