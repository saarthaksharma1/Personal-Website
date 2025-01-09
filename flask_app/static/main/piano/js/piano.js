//Piano JS Handling
const mobileMenu = document.getElementById('mobile-menu');
const navMenu = document.querySelector('.navbar__menu');

// Mobile View 
mobileMenu.addEventListener('click', () => {
    navMenu.classList.toggle('active');
});

// Sound mapping for piano keys
const sound = {
    65: "http://carolinegabriel.com/demo/js-keyboard/sounds/040.wav",
    87: "http://carolinegabriel.com/demo/js-keyboard/sounds/041.wav",
    83: "http://carolinegabriel.com/demo/js-keyboard/sounds/042.wav",
    69: "http://carolinegabriel.com/demo/js-keyboard/sounds/043.wav",
    68: "http://carolinegabriel.com/demo/js-keyboard/sounds/044.wav",
    70: "http://carolinegabriel.com/demo/js-keyboard/sounds/045.wav",
    84: "http://carolinegabriel.com/demo/js-keyboard/sounds/046.wav",
    71: "http://carolinegabriel.com/demo/js-keyboard/sounds/047.wav",
    89: "http://carolinegabriel.com/demo/js-keyboard/sounds/048.wav",
    72: "http://carolinegabriel.com/demo/js-keyboard/sounds/049.wav",
    85: "http://carolinegabriel.com/demo/js-keyboard/sounds/050.wav",
    74: "http://carolinegabriel.com/demo/js-keyboard/sounds/051.wav",
    75: "http://carolinegabriel.com/demo/js-keyboard/sounds/052.wav",
    79: "http://carolinegabriel.com/demo/js-keyboard/sounds/053.wav",
    76: "http://carolinegabriel.com/demo/js-keyboard/sounds/054.wav",
    80: "http://carolinegabriel.com/demo/js-keyboard/sounds/055.wav",
    186: "http://carolinegabriel.com/demo/js-keyboard/sounds/056.wav"
};

// Keeps track of pressed keys
const pressedKeys = {};

// Plays sound based on key
function playSound(key) {
    const audio = new Audio(sound[key]);
    audio.play();
}

// Handles key press visually
function keyPressed(key) {
    const element = document.querySelector(`[data-key="${key}"]`);
    if (element) {
        element.classList.add("pressed");
        setTimeout(() => element.classList.remove("pressed"), 100);
    }
}

// Keyboard press event listener
document.addEventListener("keydown", (event) => {
    const key = event.keyCode;

    // Check if the key is associated with a sound and not currently pressed
    if (sound[key] && !pressedKeys[key]) {
        pressedKeys[key] = true; // Mark the key as pressed
        playSound(key);
        keyPressed(key);
    }
});

// Key release event listener
document.addEventListener("keyup", (event) => {
    const key = event.keyCode;

    // Mark the key as not pressed when released
    if (pressedKeys[key]) {
        delete pressedKeys[key];
    }
});

// Mouse click event listener
document.querySelectorAll(".white-key, .black-key").forEach(key => {
    key.addEventListener("click", function () {
        const keyCode = parseInt(this.getAttribute("data-key"));
        playSound(keyCode);
        keyPressed(keyCode);
    });
});

// "weseeyou" sequence to awaken The Great Old One
let typedSequence = "";
document.addEventListener("keydown", function (event) {
    const key = event.key.toLowerCase();
    typedSequence += key;

    // Keep only the last 8 characters for matching "weseeyou"
    typedSequence = typedSequence.slice(-8);

    if (typedSequence === "weseeyou") {
        awakenGreatOldOne();
    }
});

// Awaken "The Great Old One" function
function awakenGreatOldOne() {
    // Gradually fade out the entire piano container
    const pianoContainer = document.querySelector(".piano-container");
    pianoContainer.style.transition = "opacity 2s ease";  
    pianoContainer.style.opacity = "0";

    // Removes Piano Container after wesee you typed
    setTimeout(() => {
        pianoContainer.style.display = "none";  //Gets rid of piano

        // Creates and shows the awakened message with texture image
        const awakenedMessage = document.createElement("div");
        awakenedMessage.classList.add("awakened");
        awakenedMessage.innerHTML = `
            <h2>I have awoken.</h2>
            <img src="/static/piano/images/texture.jpeg" alt="The Great Old One" style="width: 100%; max-width: 600px; border: none;" />`;

    
        document.body.appendChild(awakenedMessage);

        // Plays the creepy sound
        const creepySound = new Audio('https://orangefreesounds.com/wp-content/uploads/2020/09/Creepy-piano-sound-effect.mp3');
        creepySound.play();

        // Cancels Further pushes after weseeyou is typed
        document.removeEventListener("keydown", handleKeyPress);
        document.removeEventListener("keyup", handleKeyRelease);

        // Disables mouse click event listeners for Piano Keys
        document.querySelectorAll(".white-key, .black-key").forEach(key => {
            key.replaceWith(key.cloneNode(true)); // This effectively removes all event listeners
        });

    }, 2000);  
}
