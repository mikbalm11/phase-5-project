import React, { useState } from 'react';

function OliveOilItem({ oil, onEdit, onDelete }) {
  const [editing, setEditing] = useState(false);
  const [editFields, setEditFields] = useState({
    name: oil.name,
    year: oil.year,
    price: oil.price,
  });

  function startEditing() {
    setEditing(true);
  }

  function cancelEditing() {
    setEditing(false);
    setEditFields({ name: oil.name, year: oil.year, price: oil.price });
  }

  async function handleEdit() {
    const payload = {
      name: editFields.name,
      year: parseInt(editFields.year),
      price: parseFloat(editFields.price),
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
    <div>
      <input
        type="text"
        value={editFields.name}
        onChange={(e) => setEditFields({ ...editFields, name: e.target.value })}
      />
      <input
        type="number"
        value={editFields.year}
        min="1900"
        max="2025"
        onChange={(e) => setEditFields({ ...editFields, year: e.target.value })}
        style={{ width: '50px' }}
      />
      <input
        type="number"
        value={editFields.price}
        step="10.0"
        min="0"
        onChange={(e) => setEditFields({ ...editFields, price: e.target.value })}
      />
      <button onClick={handleEdit}>Save</button>
      <button onClick={cancelEditing}>Cancel</button>
    </div>
  ) : (
    <div>
      <strong>{oil.name}</strong> — Year: {oil.year}, Price: ${oil.price}
      <button onClick={startEditing}>✏️</button>
      <button onClick={handleDelete}>🗑️</button>
    </div>
  );
}

export default OliveOilItem;
