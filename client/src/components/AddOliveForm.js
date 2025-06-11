import React, { useState, useContext } from "react";
import { UserContext } from "./App";

function AddOliveForm({ onAddOlive }) {
  const { extraData } = useContext(UserContext);
  const [name, setName] = useState("");
  const [country, setCountry] = useState("");
  const [region, setRegion] = useState("");
  const [color, setColor] = useState("");
  const [rarity, setRarity] = useState("");

  const countries = extraData.oliveOilProducingCountries || [];
  const regionsByCountry = extraData.oliveOilProducingRegionsByCountry || {};
  const colors = extraData.oliveColors || [];
  const rarities = extraData.oliveRarities || [];

  const regions = country ? regionsByCountry[country] || [] : [];

  async function handleSubmit(e) {
    e.preventDefault();

    try {
      const res = await fetch("/olives", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "include",
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

      <select value={country} onChange={(e) => {
        setCountry(e.target.value);
        setRegion("");
      }} required>
        <option value="">Select Country</option>
        {countries.map((c) => (
          <option key={c} value={c}>{c}</option>
        ))}
      </select>

      <select value={region} onChange={(e) => setRegion(e.target.value)} required>
        <option value="">Select Region</option>
        {regions.map((r) => (
          <option key={r} value={r}>{r}</option>
        ))}
      </select>

      <select value={color} onChange={(e) => setColor(e.target.value)} required>
        <option value="">Select Color</option>
        {colors.map((c) => (
          <option key={c} value={c}>{c}</option>
        ))}
      </select>

      <select value={rarity} onChange={(e) => setRarity(e.target.value)} required>
        <option value="">Select Rarity</option>
        {rarities.map((r) => (
          <option key={r} value={r}>{r}</option>
        ))}
      </select>

      <button type="submit">Add Olive</button>
    </form>
  );
}

export default AddOliveForm;
