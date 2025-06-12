import React, { useState, useContext } from "react";
import { UserContext } from "./App";
import OliveOilItem from "./OliveOilItem";

function UserOlives() {
  const { userOlives, handleEditOil, handleDeleteOil } = useContext(UserContext);
  const [expandedOliveId, setExpandedOliveId] = useState(null);

  return (
    <div>
      <h1>My Olives</h1>
      <ul>
        {userOlives.map((olive) => (
          <li key={olive.id}>
            <strong
              onClick={() =>
                setExpandedOliveId(expandedOliveId === olive.id ? null : olive.id)
              }
            >
              {olive.name}
            </strong>{" "}
            — {olive.region}, {olive.country}, Color: {olive.color}, Rarity:{" "}
            {olive.rarity}
            {expandedOliveId === olive.id && (
              <ul>
                {olive.oils.map((oil) => (
                  <li key={oil.id}>
                    <OliveOilItem
                      oil={oil}
                      onEdit={handleEditOil}
                      onDelete={handleDeleteOil}
                    />
                  </li>
                ))}
              </ul>
            )}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default UserOlives;
