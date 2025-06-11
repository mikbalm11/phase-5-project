import React, { useState, useContext } from "react";
import { UserContext } from "./App";
import AddProducerForm from "./AddProducerForm";
import AddOliveForm from "./AddOliveForm";

function AddOilForm() {
  const {
    producers, setProducers,
    olives, setOlives,
    user, setUser,
    userProducers, setUserProducers,
    userOlives, setUserOlives
  } = useContext(UserContext);  

  const [name, setName] = useState("");
  const [year, setYear] = useState("");
  const [price, setPrice] = useState("");
  const [acidity, setAcidity] = useState("");
  const [isActive, setIsActive] = useState(true);

  const [producerId, setProducerId] = useState("");
  const [oliveId, setOliveId] = useState("");
  const [showProducerForm, setShowProducerForm] = useState(false);
  const [showOliveForm, setShowOliveForm] = useState(false);

  async function handleSubmit(e) {
    e.preventDefault();
    if (!producerId) {
      alert("Please select a producer or add a new one");
      return;
    }
    if (!oliveId) {
      alert("Please select an olive or add a new one");
      return;
    }
    
    try {
      const res = await fetch("/oils", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          name, 
          year, 
          price, 
          acidity, 
          isActive, 
          producerId: producerId, 
          oliveId: oliveId 
        }),
      });

      if (!res.ok) {
        const err = await res.json();
        throw new Error(err.error || "Failed to add olive oil");
      }
    
      const newOil = await res.json();

      setUser({ ...user, oils: [...user.oils, newOil] });

      setName("");
      setYear("");
      setPrice("");
      setAcidity("");
      setIsActive(true);
      setProducerId("");
      setOliveId("");
      setShowProducerForm(false);
      setShowOliveForm(false);
    } catch (error) {
      alert(error.message);
    }
  }

  function handleNewProducer(newProducer) {
    setProducers([...producers, newProducer]);
    setUserProducers([...userProducers, newProducer]);
    setProducerId(newProducer.id);
    setShowProducerForm(false);
  }

  function handleNewOlive(newOlive) {
    setOlives([...olives, newOlive]);
    setUserOlives([...userOlives, newOlive]);
    setOliveId(newOlive.id);
    setShowOliveForm(false);
  }

  return (
    <div>
      <h2>Add a New Olive Oil</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Olive Oil Name"
          value={name}
          onChange={(e) => setName(e.target.value)}
          required
        />
        <input
          type="year"
          min="1990"
          max="2025"
          step="1"
          placeholder="Year (1990-2025)"
          value={year}
          onChange={(e) => setYear(e.target.value)}
          required
        />
        <input
          type="text"
          placeholder="Price"
          value={price}
          onChange={(e) => setPrice(e.target.value)}
          required
        />
        <input
          type="number"
          placeholder="Acidity"
          value={acidity}
          onChange={(e) => setAcidity(e.target.value)}
          required
        />
        Active
        <input
          type="checkbox"
          checked={isActive}
          onChange={(e) => setIsActive(e.target.checked)}
        />
        <select
          value={producerId}
          onChange={(e) => setProducerId(e.target.value)}
          required
        >
          <option value="">-- Select Producer --</option>
          {producers.map((producer) => (
            <option key={producer.id} value={producer.id}>
              {producer.name}
            </option>
          ))}
        </select>
        <select
          value={oliveId}
          onChange={(e) => setOliveId(e.target.value)}
          required
        >
          <option value="">-- Select Olive --</option>
          {olives.map((olive) => (
            <option key={olive.id} value={olive.id}>
              {olive.name}
            </option>
          ))}
        </select>
        <button>
          Add Olive Oil
        </button>
      </form>
    <div>Don't see your producer or olive?</div>
      <button onClick={() => setShowProducerForm((prev) => !prev)}>
        {showProducerForm ? "Cancel Adding Producer" : "Add New Producer"}
      </button>
      {showProducerForm && <AddProducerForm onAddProducer={handleNewProducer} />}

      <button onClick={() => setShowOliveForm((prev) => !prev)}>
        {showOliveForm ? "Cancel Adding Olive" : "Add New Olive"}
      </button>
      {showOliveForm && <AddOliveForm onAddOlive={handleNewOlive} />}

    </div>
  );
}

export default AddOilForm;
