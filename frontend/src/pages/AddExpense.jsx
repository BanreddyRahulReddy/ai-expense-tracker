import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api/axios";

const CATEGORIES = [
  "food", "shopping", "technology", "entertainment",
  "transport", "health", "education", "utilities", "travel", "other"
];

const CAT_EMOJI = {
  food:"🍔", shopping:"🛍️", technology:"💻", entertainment:"🎬",
  transport:"🚗", health:"💊", education:"📚", utilities:"💡",
  travel:"✈️", other:"📦"
};

export default function AddExpense() {
  const [form, setForm] = useState({ amount: "", description: "", category: "" });
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const navigate = useNavigate();

  useEffect(() => {
    if (form.description.length < 3) { setPrediction(null); return; }
    const timer = setTimeout(async () => {
      try {
        const res = await api.post("/predict/category", { description: form.description });
        setPrediction(res.data);
        if (!form.category) setForm(prev => ({ ...prev, category: res.data.category }));
      } catch {}
    }, 500);
    return () => clearTimeout(timer);
  }, [form.description]);

  const handleChange = (e) => setForm({ ...form, [e.target.name]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      await api.post("/expenses/add", {
        amount: parseFloat(form.amount),
        description: form.description,
        category: form.category
      });
      setSuccess("Expense added! ✅");
      setTimeout(() => navigate("/dashboard"), 1000);
    } catch (err) {
      setError(err.response?.data?.error || "Failed to add expense.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="page-container">
      <div className="form-card">
        <h2>Add Expense 💸</h2>
        {error   && <div className="error-msg">{error}</div>}
        {success && <div className="success-msg">{success}</div>}
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Amount ($)</label>
            <input type="number" name="amount" placeholder="e.g. 250"
              value={form.amount} onChange={handleChange} min="0" step="0.01" required />
          </div>
          <div className="form-group">
            <label>Description</label>
            <input type="text" name="description"
              placeholder='e.g. "uber ride" or "netflix subscription"'
              value={form.description} onChange={handleChange} required />
            {prediction && (
              <div className="ml-badge">
                🤖 AI suggests: <strong>{CAT_EMOJI[prediction.category]} {prediction.category}</strong>
                <span className="confidence">({prediction.confidence}% confident)</span>
              </div>
            )}
          </div>
          <div className="form-group">
            <label>Category</label>
            <select name="category" value={form.category} onChange={handleChange} required>
              <option value="">Select category</option>
              {CATEGORIES.map(cat => (
                <option key={cat} value={cat}>{CAT_EMOJI[cat]} {cat}</option>
              ))}
            </select>
          </div>
          <button type="submit" className="btn-primary" disabled={loading}>
            {loading ? "Adding..." : "Add Expense"}
          </button>
        </form>
      </div>
    </div>
  );
}