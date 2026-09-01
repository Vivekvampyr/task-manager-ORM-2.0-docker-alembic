const registerForm = document.getElementById("register-form")
registerForm.addEventListener("submit", async function (event) {
    event.preventDefault();
    const firstName = document.getElementById("first_name").value;
    const lastName = document.getElementById("last_name").value;
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    const message = document.getElementById("message");
    message.innerText = "Creating account...";
    try {
        const response = await fetch(
            "/api/auth/register",
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    first_name: firstName,
                    last_name: lastName,
                    email: email,
                    password: password
                })
            }
        );
        const data = await response.json();
        if (!response.ok) {
            message.innerText = data.detail || "Registration failed";
            return;
        }
        message.innerText = "Registration successful!";
        setTimeout(() => {
            window.location.href = "/login";
        }, 1000);
    } catch (error) {
        console.error(error);
        message.innerText = "Unable to connect to server";        
    }
}) 