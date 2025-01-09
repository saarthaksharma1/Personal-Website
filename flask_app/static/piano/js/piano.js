const mobileMenu = document.getElementById('mobile-menu');
const navMenu = document.querySelector('.navbar__menu');

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

// Handle key press event
function playSound(key) {
    const audio = new Audio(sound[key]);
    if (audio) {
        audio.play();
    }
}

// Handle key press visual effect
function keyPressed(key) {
    const element = document.querySelector(`[data-key="${key}"]`);
    if (element) {
        element.classList.add("pressed");
        setTimeout(() => element.classList.remove("pressed"), 100);
    }
}

// Keyboard press event listener
document.addEventListener("keydown", function (event) {
    const key = event.keyCode;
    if (sound[key]) {
        playSound(key);
        keyPressed(key);
    }
});

// Mouse click event listener
document.querySelectorAll(".white-key, .black-key").forEach(key => {
    key.addEventListener("click", function () {
        const keyCode = this.getAttribute("data-key");
        if (sound[keyCode]) {
            playSound(keyCode);
            keyPressed(keyCode);
        }
    });
});

// "weseeyou" sequence to awaken The Great Old One
let typedSequence = "";
document.addEventListener("keydown", function (event) {
    const key = event.key.toLowerCase();
    typedSequence += key;
    if (typedSequence.includes("weseeyou")) {
        awakenGreatOldOne();
    }
});

// Awaken "The Great Old One" function
function awakenGreatOldOne() {
    // Gradually fade out the entire piano container
    const pianoContainer = document.querySelector(".piano-container");
    pianoContainer.style.transition = "opacity 2s ease";  // Gradual fade out over 2 seconds
    pianoContainer.style.opacity = "0";

    // After fade-out, completely remove the piano container
    setTimeout(() => {
        pianoContainer.style.display = "none";  // Hide the entire piano container after fade-out

        // Create and show the awakened message with an image
        const awakenedMessage = document.createElement("div");
        awakenedMessage.classList.add("awakened");
        awakenedMessage.innerHTML = `
            <h2>I have awoken.</h2>
            <img src="/static/piano/images/texture.jpeg" alt="The Great Old One" style="width: 100%; max-width: 600px; border: none;" />`;  // Removed border and increased width

        // Append the message to the body
        document.body.appendChild(awakenedMessage);

        // Play creepy sound
        const creepySound = new Audio('https://orangefreesounds.com/wp-content/uploads/2020/09/Creepy-piano-sound-effect.mp3');
        creepySound.play();
    }, 2000);  // Wait for the fade-out to complete (2 seconds)

    // Disable keypresses
    document.removeEventListener("keydown", keydownHandler);
}
// Keydown handler function
function keydownHandler(event) {
    const key = event.keyCode;
    if (sound[key]) {
        playSound(key);
        keyPressed(key);
    }
}

// Add the event listener for keydown initially
document.addEventListener("keydown", keydownHandler);
