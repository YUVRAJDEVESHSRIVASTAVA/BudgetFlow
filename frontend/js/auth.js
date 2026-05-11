import { apiRequest, getSession, setSession } from "./api.js?v=20260510-2";

function showMessage(element, message, kind = "success") {
  if (!element) {
    return;
  }
  element.textContent = message;
  element.classList.remove("is-error", "is-success");
  element.classList.add(kind === "error" ? "is-error" : "is-success");
}

function redirectIfAuthenticated() {
  if (getSession()?.tokens?.access) {
    window.location.replace("/dashboard/");
  }
}

async function handleRegisterSubmit(event) {
  event.preventDefault();
  const form = event.currentTarget;
  const message = document.getElementById("register-message");
  const formData = Object.fromEntries(new FormData(form).entries());

  try {
    const payload = {
      username: formData.username,
      email: formData.email,
      first_name: formData.first_name || "",
      last_name: formData.last_name || "",
      password: formData.password,
      confirm_password: formData.confirm_password,
    };
    const response = await apiRequest("/auth/register/", { method: "POST", body: payload, auth: false });
    setSession(response);
    showMessage(message, response.message || "Account created successfully.");
    window.setTimeout(() => window.location.replace("/dashboard/"), 350);
  } catch (error) {
    showMessage(message, error.message, "error");
  }
}

async function handleLoginSubmit(event) {
  event.preventDefault();
  const form = event.currentTarget;
  const message = document.getElementById("login-message");
  const formData = Object.fromEntries(new FormData(form).entries());

  try {
    const response = await apiRequest("/auth/login/", {
      method: "POST",
      body: {
        identifier: formData.identifier,
        password: formData.password,
      },
      auth: false,
    });
    setSession(response);
    showMessage(message, response.message || "Login successful.");
    window.setTimeout(() => window.location.replace("/dashboard/"), 250);
  } catch (error) {
    showMessage(message, error.message, "error");
  }
}

const registerForm = document.getElementById("register-form");
const loginForm = document.getElementById("login-form");

redirectIfAuthenticated();

if (registerForm) {
  registerForm.addEventListener("submit", handleRegisterSubmit);
}

if (loginForm) {
  loginForm.addEventListener("submit", handleLoginSubmit);
}
