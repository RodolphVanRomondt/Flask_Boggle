let total = 0;
let score = 0;;
let input_guess = "";

function wordLength(arg) {
    return arg.length
}

async function handleClick(e) {
    e.preventDefault()
    input_guess = e.target.previousSibling.previousSibling.value
    const response = await axios({
        url: "http://127.0.0.1:5000/guess",
        method: "GET",
        params: { input_guess }
    });

    e.target.previousSibling.previousSibling.value = "";

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
    }

    $(".message").text(text);
    $(".score").text(`You scored ${score} for ${input_guess.toLocaleUpperCase()}.`);
    $(".total").text(`Your total is: ${total}`);
}

$("button").on("click", handleClick)
