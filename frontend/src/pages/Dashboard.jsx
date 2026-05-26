import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import api from "../api/axios";
import SpendChart from "../components/SpendChart";
import CategoryPie from "../components/CategoryPie";
import TipsCard from "../components/TipsCard";
import ExpenseTable from "../components/ExpenseTable";

export default function Dashboard() {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [summary, setSummary] = useState({ by_category: [], by_month: [] });
  const [expenses, setExpenses] = useState([]);
  const [forecast, setForecast] = useState(null);
  const [tips, setTips] = useState([]);
  const [totalSpend, setTotalSpend] = useState(0);
  const [loading, setLoading] = useState(true);

  useEffect(() => { fetchAll(); }, []);

  async function fetchAll() {
    setLoading(true);
    try {
      const [summaryRes, expensesRes, forecastRes, tipsRes] = await Promise.all([
        api.get("/expenses/summary"),
        api.get("/expenses/list"),
        api.get("/predict/forecast"),
        api.get("/insights/tips"),
      ]);
      setSummary(summaryRes.data);
      setExpenses(expensesRes.data.expenses);
      setTotalSpend(expensesRes.data.total);
      setForecast(forecastRes.data);
      setTips(tipsRes.data.tips || []);
    } catch (err) {
      console.error("Dashboard error:", err);
    } finally {
      setLoading(false);
    }
  }

  const handleDelete = async (id) => {
    try {
      await api.delete(`/expenses/${id}`);
      fetchAll();
    } catch {
      alert("Could not delete.");
    }
  };

  if (loading) return <div className="loading">Loading your dashboard... ⏳</div>;

  return (
    <div className="dashboard">
      <div className="dash-header">
        <div>
          <h1>Hi, {user?.name} 👋</h1>
          <p className="dash-subtitle">Here's your spending overview</p>
        </div>
        <button className="btn-primary" onClick={() => navigate("/add")}>+ Add Expense</button>
      </div>

      <div className="cards-row">
        <div className="stat-card">
          <p className="stat-label">Total Spent</p>
          <h2 className="stat-value">${totalSpend.toFixed(2)}</h2>
        </div>
        <div className="stat-card">
          <p className="stat-label">Transactions</p>
          <h2 className="stat-value">{expenses.length}</h2>
        </div>
        {forecast && (
          <div className={`stat-card ${forecast.trend === "increasing" ? "card-warning" : "card-good"}`}>
            <p className="stat-label">Next Month Forecast</p>
            <h2 className="stat-value">${forecast.predicted.toFixed(2)}</h2>
            <p className="stat-trend">
              {forecast.trend === "increasing" ? "📈" : forecast.trend === "decreasing" ? "📉" : "➡️"}
              {" "}{Math.abs(forecast.change_pct)}% {forecast.trend}
            </p>
          </div>
        )}
        <div className="stat-card">
          <p className="stat-label">Top Category</p>
          <h2 className="stat-value">
            {summary.by_category.length > 0
              ? summary.by_category.sort((a, b) => b.total - a.total)[0].category
              : "—"}
          </h2>
        </div>
      </div>

      <div className="charts-row">
        <div className="chart-box">
          <h3>Monthly Spending</h3>
          <SpendChart data={summary.by_month} />
        </div>
        <div className="chart-box">
          <h3>By Category</h3>
          <CategoryPie data={summary.by_category} />
        </div>
      </div>

      <TipsCard tips={tips} />

      <div className="section">
        <h3>Recent Expenses</h3>
        <ExpenseTable expenses={expenses} onDelete={handleDelete} />
      </div>
    </div>
  );
}