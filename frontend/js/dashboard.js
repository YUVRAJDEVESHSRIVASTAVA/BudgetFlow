import { apiRequest, clearSession, getSession, formatCurrency } from "./api.js?v=20260510-2";
import {
  fillCategorySelect,
  renderCategoryItem,
  renderEmptyState,
  renderExpenseItem,
  renderSummaryCard,
} from "./expense.js?v=20260510-2";

const state = {
  categories: [],
  expenses: [],
  summary: null,
};

function requireSession() {
  if (!getSession()?.tokens?.access) {
    window.location.replace("/login/");
    return false;
  }
  return true;
}

function setMessage(element, message, kind = "success") {
  if (!element) {
    return;
  }
  element.textContent = message;
  element.classList.remove("is-error", "is-success");
  element.classList.add(kind === "error" ? "is-error" : "is-success");
}

function renderSummary(summary) {
  const container = document.getElementById("summary-cards");
  if (!container) {
    return;
  }

  const hasSpendingData = Number(summary.expense_count ?? 0) > 0;
  const hasMonthlyData = Number(summary.monthly_expense_count ?? 0) > 0;
  const hasBudgetData = summary.need_to_pay_amount !== null && summary.need_to_pay_amount !== undefined;
  const totalSpent = hasSpendingData ? formatCurrency(summary.total_spent) : "N/A";
  const monthlyTotal = hasSpendingData ? formatCurrency(summary.monthly_total) : "N/A";
  const monthlyAverage = hasMonthlyData ? formatCurrency(summary.monthly_average) : "N/A";
  const needToPayValue = hasBudgetData ? formatCurrency(summary.need_to_pay_amount) : "N/A";
  const needToPaySubtitle = summary.need_to_pay_label || "";

  const cards = [
    renderSummaryCard("Total spent", totalSpent),
    renderSummaryCard("This month", monthlyTotal),
    renderSummaryCard("Monthly average", monthlyAverage),
    renderSummaryCard("Need to pay", needToPayValue, needToPaySubtitle),
    renderSummaryCard("Expenses", String(summary.expense_count ?? 0)),
    renderSummaryCard("Categories", String(state.categories.length)),
  ];

  container.innerHTML = cards.join("");
}

function renderCategories() {
  const container = document.getElementById("category-list");
  const select = document.querySelector('#create-expense-form select[name="category"]');
  if (!container || !select) {
    return;
  }

  fillCategorySelect(select, state.categories);
  container.innerHTML = state.categories.length
    ? state.categories.map((category) => renderCategoryItem(category)).join("")
    : renderEmptyState("No categories yet", "Create your first category to organize expenses.");
}

function renderExpenses() {
  const container = document.getElementById("expense-list");
  if (!container) {
    return;
  }

  container.innerHTML = state.expenses.length
    ? state.expenses.map((expense) => renderExpenseItem(expense)).join("")
    : renderEmptyState("No expenses yet", "Add your first expense to start tracking.");
}

async function loadCurrentUser() {
  const user = await apiRequest("/auth/me/");
  const nameTarget = document.getElementById("user-name");
  if (nameTarget) {
    nameTarget.textContent = user.first_name ? `Hi, ${user.first_name}` : `Hi, ${user.username}`;
  }
}

async function loadCategories() {
  state.categories = await apiRequest("/categories/");
  renderCategories();
}

async function loadExpenses() {
  const search = document.getElementById("expense-search")?.value.trim() || "";
  const query = new URLSearchParams();
  if (search) {
    query.set("search", search);
  }
  const suffix = query.toString() ? `?${query.toString()}` : "";
  state.expenses = await apiRequest(`/expenses/${suffix}`);
  renderExpenses();
}

async function loadSummary() {
  state.summary = await apiRequest("/summary/");
  return state.summary;
}

async function refreshDashboard() {
  try {
    await Promise.all([loadCurrentUser(), loadCategories(), loadSummary(), loadExpenses()]);
    renderSummary(state.summary);
  } catch (error) {
    if (error.status === 401) {
      clearSession();
      window.location.replace("/login/");
      return;
    }
    const rootMessage = document.getElementById("dashboard-message");
    setMessage(rootMessage, error.message, "error");
  }
}

async function handleCategorySubmit(event) {
  event.preventDefault();
  const form = event.currentTarget;
  const message = document.getElementById("dashboard-message");
  const formData = Object.fromEntries(new FormData(form).entries());

  try {
    await apiRequest("/categories/", {
      method: "POST",
      body: {
        name: formData.name,
        color: formData.color || "#2563EB",
        budget_limit: formData.budget_limit ? Number(formData.budget_limit) : null,
      },
    });
    form.reset();
    setMessage(message, "Category added.");
    await loadCategories();
    await loadSummary();
    renderSummary(state.summary);
  } catch (error) {
    setMessage(message, error.message, "error");
  }
}

async function handleExpenseSubmit(event) {
  event.preventDefault();
  const form = event.currentTarget;
  const message = document.getElementById("dashboard-message");
  const formData = Object.fromEntries(new FormData(form).entries());

  try {
    await apiRequest("/expenses/", {
      method: "POST",
      body: {
        title: formData.title,
        amount: Number(formData.amount),
        spent_on: formData.spent_on,
        category: formData.category || null,
        description: formData.description || "",
      },
    });
    form.reset();
    setMessage(message, "Expense added.");
    await Promise.all([loadCategories(), loadSummary(), loadExpenses()]);
    renderSummary(state.summary);
  } catch (error) {
    setMessage(message, error.message, "error");
  }
}

function wireEvents() {
  const logoutButton = document.getElementById("logout-button");
  const categoryForm = document.getElementById("create-category-form");
  const expenseForm = document.getElementById("create-expense-form");
  const refreshButton = document.getElementById("refresh-expenses");
  const searchInput = document.getElementById("expense-search");

  if (logoutButton) {
    logoutButton.addEventListener("click", async () => {
      try {
        await apiRequest("/auth/logout/", { method: "POST" });
      } catch (error) {
        console.warn("Logout audit could not be saved:", error);
      } finally {
        clearSession();
        window.location.replace("/");
      }
    });
  }

  if (categoryForm) {
    categoryForm.addEventListener("submit", handleCategorySubmit);
  }

  if (expenseForm) {
    expenseForm.addEventListener("submit", handleExpenseSubmit);
  }

  if (refreshButton) {
    refreshButton.addEventListener("click", () => loadExpenses());
  }

  if (searchInput) {
    let timer = null;
    searchInput.addEventListener("input", () => {
      window.clearTimeout(timer);
      timer = window.setTimeout(() => loadExpenses(), 220);
    });
  }
}

if (requireSession()) {
  wireEvents();
  refreshDashboard();
}
