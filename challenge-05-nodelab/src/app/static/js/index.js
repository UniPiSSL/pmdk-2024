window.onload = function() {
    var loginBtn = document.getElementById("loginBtn");
    var registerBtn = document.getElementById("registerBtn");
  
    loginBtn.onclick = function() {
        switchForm("login");
    };
  
    registerBtn.onclick = function() {
        switchForm("register");
    };
};
  
function switchForm(formType) {
    var loginForm = document.getElementById("loginForm");
    var registerForm = document.getElementById("registerForm");
  
    if (formType === "login") {
        loginForm.style.display = "block";
        registerForm.style.display = "none";
    } else {
        registerForm.style.display = "block";
        loginForm.style.display = "none";
    }
    event.preventDefault();
}

function submitRegisterForm(event) {
    event.preventDefault();     
  
    var registerData = {
        username: document.getElementById("newUsername").value,
        school: document.getElementById("newSchool").value,
        password: document.getElementById("newPassword").value
    };
    console.log(registerData);
    fetch("/api/auth/register", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(registerData),
    })
    .then(response => response.json())
    .then(data => {
        displayResponseBox(data);
        if (data.message) {        
            switchForm("login");
        }
    })
}

function submitLoginForm(event) {
    event.preventDefault();

    var loginData = {
        username: document.getElementById("username").value,
        password: document.getElementById("password").value
    };

    fetch("/api/auth/login", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        credentials: "include",
        body: JSON.stringify(loginData),
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            displayResponseBox(data);
        } else {
            window.location.href = "/dashboard";
        }
    })
}
  
