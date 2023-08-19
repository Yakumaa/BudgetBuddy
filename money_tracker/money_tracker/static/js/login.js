const showPasswordToggle = document.querySelector(".showPasswordToggle");
const passwordField = document.querySelector("#passwordField");

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