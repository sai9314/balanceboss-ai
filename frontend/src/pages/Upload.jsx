import { useState } from "react";

export default function Upload() {
  const [status, setStatus] = useState("");

  async function handleUpload(e, type) {
    e.preventDefault();
    const formData = new FormData(e.target);
    const res = await fetch(`/api/upload/${type}`, {
      method: "POST",
      body: formData,
    });
    const data = await res.json();
    setStatus(`Uploaded ${data.uploaded} ${data.type} records`);
  }

  return (
    <div className="upload">
      <h1>Upload Financial Data</h1>

      <section>
        <h2>Sales CSV</h2>
        <form onSubmit={(e) => handleUpload(e, "sales")}>
          <input type="file" name="file" accept=".csv" required />
          <button type="submit">Upload Sales</button>
        </form>
      </section>

      <section>
        <h2>Expenses CSV</h2>
        <form onSubmit={(e) => handleUpload(e, "expenses")}>
          <input type="file" name="file" accept=".csv" required />
          <button type="submit">Upload Expenses</button>
        </form>
      </section>

      {status && <p className="status">{status}</p>}
    </div>
  );
}
