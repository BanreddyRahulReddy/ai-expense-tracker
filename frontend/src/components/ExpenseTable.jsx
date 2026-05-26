export default function ExpenseTable({ expenses, onDelete }) {
  if (!expenses || expenses.length === 0)
    return <p className="no-data">No expenses yet. Click "Add Expense" to get started!</p>;

  const colors = {
    food:"#f59e0b", transport:"#3b82f6", entertainment:"#8b5cf6",
    shopping:"#ec4899", technology:"#6366f1", health:"#10b981",
    education:"#14b8a6", utilities:"#f97316", travel:"#0ea5e9", other:"#94a3b8"
  };

  return (
    <div className="table-wrapper">
      <table className="expense-table">
        <thead>
          <tr>
            <th>Date</th><th>Description</th><th>Category</th><th>Amount</th><th>Action</th>
          </tr>
        </thead>
        <tbody>
          {expenses.map(exp => (
            <tr key={exp.id}>
              <td>{exp.date.split(" ")[0]}</td>
              <td>{exp.description}</td>
              <td>
                <span className="category-badge"
                  style={{ backgroundColor: colors[exp.category] || "#94a3b8" }}>
                  {exp.category}
                </span>
              </td>
              <td className="amount">${exp.amount.toFixed(2)}</td>
              <td>
                <button className="btn-delete"
                  onClick={() => window.confirm("Delete?") && onDelete(exp.id)}>🗑️</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}