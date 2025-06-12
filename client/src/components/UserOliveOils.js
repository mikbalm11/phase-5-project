import React, { useContext } from "react";
import { UserContext } from "./App";
import OliveOilItem from "./OliveOilItem";
import AddOilForm from "./AddOilForm";

function UserOliveOils() {
  const { user, handleEditOil, handleDeleteOil } = useContext(UserContext);

  return (
    <div>
      <h1>My Olive Oils</h1>
      <ul>
        {user?.oils.map((oil) => (
          <li key={oil.id}>
            <OliveOilItem oil={oil} onEdit={handleEditOil} onDelete={handleDeleteOil} />
          </li>
        ))}
      </ul>
      <AddOilForm />
    </div>
  );
}

export default UserOliveOils;
