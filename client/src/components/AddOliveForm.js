import React, { useState } from "react";

function AddOliveForm({ onAddOlive }) {
  const [name, setName] = useState("");
  const [country, setCountry] = useState("");
  const [region, setRegion] = useState("");
  const [color, setColor] = useState("");
  const [rarity, setRarity] = useState("");

  async function handleSubmit(e) {
    e.preventDefault();

    try {
      const res = await fetch("/olives", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, country, region, color, rarity }),
      });

      if (!res.ok) {
        const err = await res.json();
        throw new Error(err.error || "Failed to add olive");
      }

      const newOlive = await res.json();
      onAddOlive(newOlive);

      setName("");
      setCountry("");
      setRegion("");
      setColor("");
      setRarity("");
    } catch (error) {
      alert(error.message);
    }
  }

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="text"
        placeholder="Olive name"
        value={name}
        onChange={(e) => setName(e.target.value)}
        required
      />
      <input
        type="text"
        placeholder="Country"
        value={country}
        onChange={(e) => setCountry(e.target.value)}
        required
      />
      <input
        type="text"
        placeholder="Region"
        value={region}
        onChange={(e) => setRegion(e.target.value)}
        required
      />
      <input
        type="text"
        placeholder="Color"
        value={color}
        onChange={(e) => setColor(e.target.value)}
        required
      />
      <input
        type="text"
        placeholder="Rarity"
        value={rarity}
        onChange={(e) => setRarity(e.target.value)}
        required
      />
      <button type="submit">Add Olive</button>
    </form>
  );
}

export default AddOliveForm;
