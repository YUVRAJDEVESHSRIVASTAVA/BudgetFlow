const STORAGE_KEY = "expenseflow.theme";

function getSystemTheme() {
  return window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
}

function getSavedTheme() {
  try {
    const savedTheme = window.localStorage.getItem(STORAGE_KEY);
    if (savedTheme === "dark" || savedTheme === "light") {
      return savedTheme;
    }
  } catch (error) {
    return null;
  }
  return null;
}

function applyTheme(theme) {
  document.documentElement.dataset.theme = theme;
  document.documentElement.style.colorScheme = theme;
}

function updateButton(button, theme) {
  button.textContent = theme === "dark" ? "Light mode" : "Dark mode";
  button.setAttribute("aria-pressed", theme === "dark" ? "true" : "false");
}

function initializeThemeToggle() {
  const button = document.getElementById("theme-toggle");
  const currentTheme = getSavedTheme() || getSystemTheme();

  applyTheme(currentTheme);

  if (!button) {
    return;
  }

  updateButton(button, currentTheme);

  button.addEventListener("click", () => {
    const nextTheme = document.documentElement.dataset.theme === "dark" ? "light" : "dark";
    try {
      window.localStorage.setItem(STORAGE_KEY, nextTheme);
    } catch (error) {
      // Ignore storage failures and still switch the active theme.
    }
    applyTheme(nextTheme);
    updateButton(button, nextTheme);
  });
}

initializeThemeToggle();