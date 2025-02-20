const questions = {
    "Easy": [
        { image: "images/chat.png", sound: "sounds/chat.wav", answer: "Chat", options: ["Chien", "Chat", "Lapin", "Souris"] },
        { image: "images/pomme.png", sound: null, answer: "Pomme", options: ["Pomme", "Poire", "Orange", "Raisin"] }
    ],
    "intermediate": [
        { image: "images/voiture.png", sound: "sounds/voiture.wav", answer: "Voiture", options: ["Moto", "Camion", "Avion", "Voiture"] },
        { image: "images/avion.png", sound: "sounds/avion.wav", answer: "Avion", options: ["Bateau", "Voiture", "Avion", "Train"] }
    ],
    "difficult": [
        { image: "images/panther.png", sound: "sounds/panther.wav", answer: "Panthère", options: ["Tigre", "Léopard", "Panthère", "Jaguar"] },
        { image: "images/satellite.png", sound: null, answer: "Satellite", options: ["Lune", "Satellite", "Astéroïde", "Comète"] }
    ]
};

let currentQuestions = [];
let currentQuestionIndex = 0;
let currentSound = null;
let soundTimeout = null;

function startGame(difficulty) {
    document.getElementById("menu").style.display = "none";
    document.getElementById("game").style.display = "block";

    currentQuestions = [...questions[difficulty]].sort(() => Math.random() - 0.5);
    currentQuestionIndex = 0;
    showQuestion();
}

function showQuestion() {
    if (currentQuestionIndex >= currentQuestions.length) {
        document.getElementById("message").textContent = "End of questions!";
        setTimeout(returnToMenu, 2000);
        return;
    }

    const question = currentQuestions[currentQuestionIndex];
    document.getElementById("question-image").src = question.image;
    document.getElementById("message").textContent = "Choose an answer !";

    if (question.sound) {
        currentSound = new Audio(question.sound);
    } else {
        currentSound = null;
    }

    const optionsDiv = document.getElementById("options");
    optionsDiv.innerHTML = "";
    question.options.sort(() => Math.random() - 0.5).forEach(option => {
        let btn = document.createElement("button");
        btn.className = "option-btn";
        btn.textContent = option;
        btn.onclick = () => checkAnswer(option, question.answer);
        optionsDiv.appendChild(btn);
    });
}

function playSound() {
    if (currentSound) {
        stopSound(); // Stop previous sound if playing
        currentSound.currentTime = 0;
        currentSound.play();
        soundTimeout = setTimeout(() => {
            currentSound.pause();
        }, 5000); // Stop the sound after 5 seconds
    }
}

function stopSound() {
    if (currentSound) {
        currentSound.pause();
        clearTimeout(soundTimeout);
    }
}

function checkAnswer(selected, correct) {
    stopSound(); // Stop sound immediately when answering

    if (selected === correct) {
        document.getElementById("message").textContent = "Good Answer !";
    } else {
        document.getElementById("message").textContent = `Wrong, the correct answer was "${correct}"`;
    }

    setTimeout(() => {
        currentQuestionIndex++;
        showQuestion();
    }, 1500);
}

function returnToMenu() {
    document.getElementById("menu").style.display = "block";
    document.getElementById("game").style.display = "none";
}
