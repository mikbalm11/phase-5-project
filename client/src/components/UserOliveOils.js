import React, { useContext } from "react";
import { UserContext } from "./App";
import OliveOilItem from "./OliveOilItem";
import AddOilForm from "./AddOilForm";

function UserOliveOils() {
  const { user, handleEditOil, handleDeleteOil } = useContext(UserContext);

  return (
    <section className="user-olive-oils">
      <h1>My Olive Oils</h1>
      <ul className="oil-list">
        {user?.oils.map((oil) => (
          <li key={oil.id}>
            <OliveOilItem oil={oil} onEdit={handleEditOil} onDelete={handleDeleteOil} />
          </li>
        ))}
      </ul>
      <AddOilForm />
    </section>
  );
}

export default UserOliveOils;
