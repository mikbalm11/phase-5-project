import React, { useState } from "react";

function AddProducerForm({ onAddProducer }) {
  const [name, setName] = useState("");
  const [address, setAddress] = useState("");
  const [capacity, setCapacity] = useState("");

  async function handleSubmit(e) {
    e.preventDefault();

    try {
      const res = await fetch("/producers", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "include",
        body: JSON.stringify({ name, address, capacity: parseInt(capacity) }),
      });

      if (!res.ok) {
        const err = await res.json();
        throw new Error(err.error || "Failed to add producer");
      }

      const newProducer = await res.json();
      onAddProducer(newProducer);

      setName("");
      setAddress("");
      setCapacity("");
    } catch (error) {
      alert(error.message);
    }
  }

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="text"
        placeholder="Producer name"
        value={name}
        onChange={(e) => setName(e.target.value)}
        required
      />
      <input
        type="text"
        placeholder="Producer address"
        value={address}
        onChange={(e) => setAddress(e.target.value)}
        required
      />
      <input
        type="number"
        placeholder="Capacity (min: 0)"
        min="0"
        value={capacity}
        onChange={(e) => setCapacity(e.target.value)}
        required
      />
      <button type="submit">Add Producer</button>
    </form>
  );
}

export default AddProducerForm;
