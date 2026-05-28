import { useEffect, useState } from "react";

export default function Dashboard() {
  const [summary, setSummary] = useState(null);

  useEffect(() => {
    fetch("/api/analytics/summary")
      .then((r) => r.json())
      .then(setSummary);
  }, []);

  if (!summary) return <p>Loading…</p>;

  return (
    <div className="dashboard">
      <h1>BalanceBoss Dashboard</h1>
      <div className="cards">
        <div className="card">
          <h2>Total Sales</h2>
          <p>${summary.total_sales.toFixed(2)}</p>
        </div>
        <div className="card">
          <h2>Total Expenses</h2>
          <p>${summary.total_expenses.toFixed(2)}</p>
        </div>
        <div className="card">
          <h2>Net</h2>
          <p>${summary.net.toFixed(2)}</p>
        </div>
      </div>
    </div>
  );
}
