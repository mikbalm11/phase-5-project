import React, { useState, useContext } from 'react'
import { UserContext } from './App'
import AddOilForm from './AddOilForm'



function UserOliveOils() {
  const { user, setUser } = useContext(UserContext);
  const [editingId, setEditingId] = useState(null);
  const [editFields, setEditFields] = useState({});

  function startEditing(oil) {
    setEditingId(oil.id);
    setEditFields({
      name: oil.name,
      year: oil.year,
      price: oil.price,
    });
  }

  function cancelEditing() {
    setEditingId(null);
    setEditFields({});
  }

  async function handleEdit(oilId) {
    const res = await fetch(`/oils/${oilId}`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      credentials: "include",
      body: JSON.stringify(editFields),
    });

    if (res.ok) {
      const updatedOil = await res.json();
      setUser((prev) => ({
        ...prev,
        oils: prev.oils.map((oil) =>
          oil.id === updatedOil.id ? updatedOil : oil
        ),
      }));
      cancelEditing();
    } else {
      alert("Failed to edit olive oil");
    }
  }


  function handleDelete(id) {
    fetch(`/oils/${id}`, {
      method: "DELETE",
      credentials: "include",
    }).then((res) => {
      if (res.ok) {
        setUser((prev) => ({
          ...prev,
          oils: prev.oils.filter((oil) => oil.id !== id),
        }));
      } else {
        alert("Failed to delete olive oil");
      }
    });
  }

  return (
    <div>
      <h1>My Olive Oils</h1>
      <ul>
        {user.oils.map((oil) => (
          <li key={oil.id}>
            {editingId === oil.id ? (
              <div>
                <input
                  type="text"
                  value={editFields.name}
                  onChange={(e) =>
                    setEditFields({ ...editFields, name: e.target.value })
                  }
                />
                <input
                  type="text"
                  value={editFields.year}
                  onChange={(e) =>
                    setEditFields({ ...editFields, year: e.target.value })
                  }
                />
                <input
                  type="text"
                  value={editFields.price}
                  onChange={(e) =>
                    setEditFields({ ...editFields, price: e.target.value })
                  }
                />
                <button onClick={() => handleEdit(oil.id)}>Save</button>
                <button onClick={cancelEditing}>Cancel</button>
              </div>
            ) : (
              <div>
                <strong>{oil.name}</strong> — Year: {oil.year}, Price: ${oil.price}
                <button onClick={() => startEditing(oil)}>Edit</button>
                <button onClick={() => handleDelete(oil.id)}>Delete</button>
              </div>
            )}
          </li>
        ))}
      </ul>
      <AddOilForm />
    </div>
  );
}


export default UserOliveOils
