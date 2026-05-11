import { formatCurrency, formatDate } from "./api.js?v=20260510";

export function escapeHtml(value) {
  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#39;");
}

export function renderSummaryCard(label, value, subtitle = "", tone = "") {
  return `
    <article class="summary-card ${tone}">
      <span>${escapeHtml(label)}</span>
      <strong>${escapeHtml(value)}</strong>
      ${subtitle ? `<small class="summary-card-subtitle">${escapeHtml(subtitle)}</small>` : ""}
    </article>
  `;
}

export function renderCategoryItem(category) {
  const color = category.color || "#0f766e";
  const limit = category.budget_limit ? formatCurrency(category.budget_limit) : "No limit";
  const spent = formatCurrency(category.total_spent ?? 0);
  return `
    <article class="category-item">
      <div class="list-row-main">
        <span class="category-pill"><span class="category-dot" style="background:${escapeHtml(color)}"></span>${escapeHtml(category.name)}</span>
        <span class="category-meta">${escapeHtml(spent)} spent · ${escapeHtml(String(category.expense_count ?? 0))} expenses</span>
      </div>
      <strong>${escapeHtml(limit)}</strong>
    </article>
  `;
}

export function renderExpenseItem(expense) {
  const color = expense.category?.color || "#0f766e";
  const categoryName = expense.category_name || expense.category?.name || "Uncategorized";
  return `
    <article class="expense-item">
      <div class="list-row-main">
        <strong>${escapeHtml(expense.title)}</strong>
        <span class="expense-meta">${escapeHtml(formatDate(expense.spent_on))} · ${escapeHtml(categoryName)}</span>
        ${expense.description ? `<span class="expense-meta">${escapeHtml(expense.description)}</span>` : ""}
      </div>
      <div class="list-row-side">
        <span class="category-pill"><span class="category-dot" style="background:${escapeHtml(color)}"></span>${escapeHtml(categoryName)}</span>
        <strong class="expense-amount">${escapeHtml(formatCurrency(expense.amount))}</strong>
      </div>
    </article>
  `;
}

export function renderEmptyState(title, description) {
  return `
    <div class="empty-state">
      <strong>${escapeHtml(title)}</strong>
      <span>${escapeHtml(description)}</span>
    </div>
  `;
}

export function fillCategorySelect(selectElement, categories) {
  const options = ['<option value="">Select category</option>'];
  for (const category of categories) {
    options.push(`<option value="${escapeHtml(category.id)}">${escapeHtml(category.name)}</option>`);
  }
  selectElement.innerHTML = options.join("");
}
