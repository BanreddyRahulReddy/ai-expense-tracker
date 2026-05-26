export default function TipsCard({ tips }) {
  if (!tips || tips.length === 0) return null;
  return (
    <div className="tips-card">
      <h3>💡 AI Saving Tips</h3>
      <p className="tips-subtitle">Personalized advice based on your spending</p>
      <div className="tips-list">
        {tips.map((tip, i) => (
          <div key={i} className="tip-item">
            <span className="tip-number">{i + 1}</span>
            <p>{tip}</p>
          </div>
        ))}
      </div>
    </div>
  );
}