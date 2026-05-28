import { useState } from "react";

export default function Chat() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");

  async function sendMessage(e) {
    e.preventDefault();
    if (!input.trim()) return;

    const userMsg = { role: "user", text: input };
    setMessages((prev) => [...prev, userMsg]);
    setInput("");

    const res = await fetch("/api/chat/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question: input, context: "" }),
    });
    const data = await res.json();
    setMessages((prev) => [...prev, { role: "assistant", text: data.answer }]);
  }

  return (
    <div className="chat">
      <h1>Ask BalanceBoss</h1>
      <div className="messages">
        {messages.map((m, i) => (
          <div key={i} className={`message ${m.role}`}>
            <strong>{m.role === "user" ? "You" : "BalanceBoss"}:</strong> {m.text}
          </div>
        ))}
      </div>
      <form onSubmit={sendMessage} className="input-row">
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask about your finances…"
        />
        <button type="submit">Send</button>
      </form>
    </div>
  );
}
