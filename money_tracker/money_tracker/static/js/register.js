const usernameField= document.querySelector("#usernameField");
const emailField = document.querySelector("#emailField");
const showPasswordToggle = document.querySelector(".showPasswordToggle");
const showPasswordToggleRepeat = document.querySelector(".showPasswordToggleRepeat");
const feedBackArea= document.querySelector('.invalid_feedback');
const emailFeedBackArea = document.querySelector(".emailFeedBackArea");
const passwordField = document.querySelector("#passwordField");
const repeatPasswordField = document.querySelector("#repeatPasswordField");
const usernameSuccessOutput = document.querySelector('.usernameSuccessOutput');

usernameField.addEventListener("keyup", (e) => {
    const usernameVal = e.target.value;
    usernameSuccessOutput.textContent = `Checking ${usernameVal}`

    usernameField.classList.remove("is-invalid");
    feedBackArea.style.display="none";

    if(usernameVal.length > 0){
        fetch("/authentication/validate-username", {
            body: JSON.stringify({username: usernameVal}),
            method: "POST",
        })
        .then((res) => res.json())
        .then((data) => {
            console.log("data", data);
            usernameSuccessOutput.style.display = 'none';
            if(data.username_error){
                usernameField.classList.add("is-invalid");
                feedBackArea.style.display="block";
                feedBackArea.innerHTML= `<p>${data.username_error}</p>`
            }
        });
    }
})

emailField.addEventListener("keyup", (e) => {
    console.log("77777", 77777);
    const emailVal = e.target.value;
    
    emailField.classList.remove("is-invalid");
    emailFeedBackArea.style.display="none";

    if(emailVal.length > 0){
        fetch("/authentication/validate-email", {
            body: JSON.stringify({email: emailVal}),
            method: "POST",
        })
        .then((res) => res.json())
        .then((data) => {
            console.log("data", data);
            if(data.email_error){
                emailField.classList.add("is-invalid");
                emailFeedBackArea.style.display="block";
                emailFeedBackArea.innerHTML= `<p>${data.email_error}</p>`
            }
        });
    }
})


const handleToggleInput = (field, toggleElement) => {
    if (field.type === "password") {
      field.type = "text";
      toggleElement.innerHTML = '<i class="bi-eye"></i>';
      toggleElement.classList.add("active");
    } else {
      field.type = "password";
      toggleElement.innerHTML = '<i class="bi bi-eye-slash"></i>';
      toggleElement.classList.remove("active");
    }
  };
  
  showPasswordToggle.addEventListener("click", () => {
    handleToggleInput(passwordField, showPasswordToggle);
  });
  
  showPasswordToggleRepeat.addEventListener("click", () => {
    handleToggleInput(repeatPasswordField, showPasswordToggleRepeat);
  });