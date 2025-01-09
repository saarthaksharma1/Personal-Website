// Login JavaScript
let incorrectAttempts = 0; // Variable to track incorrect login attempts

function checkCredentials() {
    // Retrieves the email and password values when the user inputs them in the form fields
    const email = document.getElementById('login-email').value;
    const password = document.getElementById('password').value;

    // JSON object that holds the email and password data
    const data_d = { email: email, password: password };

    // Gets the authentication message element and hides it initially
    const authMessage = document.getElementById('auth-message');
    authMessage.style.display = "none";

    // Makes an AJAX request to the server to process the login
    jQuery.ajax({
        // Specifies the endpoint where the login request will be sent with processlogin from routes.py
        url: "/processlogin",
        // Passes the email and password data as a JSON string
        data: JSON.stringify(data_d),
        // Uses POST method to send the request
        type: "POST",
        // Specifies the content type as JSON
        contentType: "application/json",
        // Handles the success response from the server
        success: function (returned_data) {
            // Parses the JSON response from the server
            const response = typeof returned_data === "string" ? JSON.parse(returned_data) : returned_data;

            // Checks if the response is successful
            if (response.success === 1) {
                window.location.href = "/home"; // Redirects to the home page on successful login
            } 
            // If the response is not successful, display the message and increment the counter
            else {
                incorrectAttempts++; // Increments the incorrect login attempts counter
                authMessage.style.display = "block";
                authMessage.innerText = `Incorrect login attempt. You have made ${incorrectAttempts} failed login attempt(s). Please try again.`;
            }
        },
        // Handles the error response from the server
        error: function () {
            authMessage.style.display = "block";
            authMessage.innerText = "An internal server error occurred. Please try again.";
        }
    });
}
