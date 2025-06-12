import React, { useState } from 'react';

function OliveOilItem({ oil, onEdit, onDelete }) {
  const [editing, setEditing] = useState(false);
  const [editFields, setEditFields] = useState({
    name: oil.name,
    year: oil.year,
    price: oil.price,
    isActive: oil.isActive,
    acidity: oil.acidity,
  });

  function startEditing() {
    setEditing(true);
  }

  function cancelEditing() {
    setEditing(false);
    setEditFields({ name: oil.name, year: oil.year, price: oil.price, isActive: oil.isActive, acidity: oil.acidity });
  }

  async function handleEdit() {
    const payload = {
      name: editFields.name,
      year: parseInt(editFields.year),
      price: parseFloat(editFields.price),
      isActive: editFields.isActive,
      acidity: parseFloat(editFields.acidity),
    };

    const res = await fetch(`/oils/${oil.id}`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
      body: JSON.stringify(payload),
    });

    if (res.ok) {
      const updated = await res.json();
      if (onEdit) onEdit(updated);
      setEditing(false);
    } else {
      alert('Failed to update olive oil');
    }
  }

  function handleDelete() {
    fetch(`/oils/${oil.id}`, {
      method: 'DELETE',
      credentials: 'include',
    }).then((res) => {
      if (res.ok) {
        if (onDelete) onDelete(oil.id);
      } else {
        alert('Failed to delete olive oil');
      }
    });
  }

  return editing ? (
    <div className="oil-edit-container">
      <input
        type="text"
        value={editFields.name}
        onChange={(e) => setEditFields({ ...editFields, name: e.target.value })}
        className="oil-edit-input"
      />
      <input
        type="number"
        value={editFields.year}
        min="1900"
        max="2025"
        onChange={(e) => setEditFields({ ...editFields, year: e.target.value })}
        className="oil-edit-input"
      />
      <input
        type="number"
        value={editFields.price}
        step="10.0"
        min="0"
        onChange={(e) => setEditFields({ ...editFields, price: e.target.value })}
        className="oil-edit-input"
      />
      <input
        type="checkbox"
        checked={editFields.isActive}
        onChange={(e) => setEditFields({ ...editFields, isActive: e.target.checked })}
        className="oil-edit-input"
      />
      <input
        type="number"
        min="0.0"
        max="3.0"
        step="0.01"
        value={editFields.acidity}
        onChange={(e) => setEditFields({ ...editFields, acidity: e.target.value })}
        className="oil-edit-input"
      />
      <div className="oil-actions">
        <button onClick={handleEdit}>Save</button>
        <button onClick={cancelEditing}>Cancel</button>
      </div>
    </div>
  ) : (
    <div className="oil-list-item">
      <div className="oil-details">
        <strong>{oil.name}</strong> — Year: {oil.year}, Price: ${oil.price}, Actively Produced: {oil.isActive ? 'Yes' : 'No'}, Acidity: %{oil.acidity}
      </div>
      <div className="oil-actions">
        <button onClick={startEditing}>✏️</button>
        <button onClick={handleDelete}>🗑️</button>
      </div>
    </div>
  );
}

export default OliveOilItem;
