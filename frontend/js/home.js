import { apiRequest, formatCurrency, getSession } from "./api.js?v=20260510-2";

function setPreviewValue(selector, value) {
  const element = document.querySelector(selector);
  if (element) {
    element.textContent = value;
  }
}

function renderLoggedOutPreview() {
  setPreviewValue("[data-preview-total-spent]", "N/A");
  setPreviewValue("[data-preview-monthly-budget]", "N/A");
  setPreviewValue("[data-preview-category-1]", "N/A");
  setPreviewValue("[data-preview-category-2]", "N/A");
  setPreviewValue("[data-preview-category-3]", "N/A");
}

async function hydratePreviewForSignedInUser() {
  const session = getSession();
  if (!session?.tokens?.access) {
    renderLoggedOutPreview();
    return;
  }

  try {
    const [summary, categories] = await Promise.all([apiRequest("/summary/"), apiRequest("/categories/")]);
    const hasSpendingData = Number(summary.expense_count ?? 0) > 0;
    const totalSpent = hasSpendingData ? formatCurrency(summary.total_spent) : "N/A";
    const monthlyBudgetTotal = categories.reduce((accumulator, category) => accumulator + Number(category.budget_limit || 0), 0);
    const monthlyBudget = monthlyBudgetTotal > 0 ? formatCurrency(monthlyBudgetTotal) : "N/A";
    const breakdown = Array.isArray(summary.category_breakdown) ? summary.category_breakdown : [];

    setPreviewValue("[data-preview-total-spent]", totalSpent);
    setPreviewValue("[data-preview-monthly-budget]", monthlyBudget);
    setPreviewValue("[data-preview-category-1]", breakdown[0] ? formatCurrency(breakdown[0].total) : "N/A");
    setPreviewValue("[data-preview-category-2]", breakdown[1] ? formatCurrency(breakdown[1].total) : "N/A");
    setPreviewValue("[data-preview-category-3]", breakdown[2] ? formatCurrency(breakdown[2].total) : "N/A");
  } catch (error) {
    renderLoggedOutPreview();
  }
}

hydratePreviewForSignedInUser();