import { PieChart, Pie, Cell, Tooltip, ResponsiveContainer } from "recharts";

const COLORS = ["#6366f1","#f59e0b","#10b981","#ef4444","#3b82f6","#8b5cf6","#ec4899","#14b8a6","#f97316","#84cc16"];

export default function CategoryPie({ data }) {
  if (!data || data.length === 0)
    return <p className="no-data">No category data yet.</p>;
  return (
    <ResponsiveContainer width="100%" height={250}>
      <PieChart>
        <Pie data={data} dataKey="total" nameKey="category"
          cx="50%" cy="50%" outerRadius={90}
          label={({ category, percent }) => `${category} ${(percent*100).toFixed(0)}%`}
          labelLine={false}>
          {data.map((_, i) => <Cell key={i} fill={COLORS[i % COLORS.length]} />)}
        </Pie>
        <Tooltip formatter={(v) => [`$${v}`, "Total"]} />
      </PieChart>
    </ResponsiveContainer>
  );
}