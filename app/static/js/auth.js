const loginForm = document.getElementById("login-form");
if (loginForm) {
    loginForm.addEventListener("submit", async function (event) {
        event.preventDefault();
        const email = document.getElementById("email").value;
        const password = document.getElementById("password").value;
        const message = document.getElementById("message");
        message.innerText = "Logging in...";
        try {
            const formData = new URLSearchParams();
            formData.append("username", email);
            formData.append("password", password);
            const response = await fetch("/api/auth/login", {
                method: "POST",
                headers: {
                    "Content-Type":
                        "application/x-www-form-urlencoded"
                },
                body: formData
            });
            const data = await response.json();
            if (!response.ok) {
                message.innerText = data.detail || "login failed";
                return;
            }
            // Save JWT
            localStorage.setItem("access_token", data.access_token);
            // Go to Dashboard
            window.location.href = "/dashboard";
        } catch (error) {
            console.error(error);
            message.innerText = "Unable to connect to server";
        }
    });
}