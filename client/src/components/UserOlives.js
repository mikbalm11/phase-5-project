import React, { useState, useContext } from "react";
import { UserContext } from "./App";
import OliveOilItem from "./OliveOilItem";

function UserOlives() {
  const { userOlives, handleEditOil, handleDeleteOil } = useContext(UserContext);
  const [expandedOliveId, setExpandedOliveId] = useState(null);

  return (
    <section className="user-olives">
      <h1>My Olives</h1>
      <ul className="olive-list">
        {userOlives.map((olive) => (
          <li key={olive.id} className="olive-list-item">
            <strong
              className="olive-name"
              onClick={() =>
                setExpandedOliveId(expandedOliveId === olive.id ? null : olive.id)
              }
              role="button"
              aria-expanded={expandedOliveId === olive.id}
            >
              {olive.name}
            </strong>{" "}
            — <span className="olive-region">{olive.region}</span>,{" "}
            <span className="olive-country">{olive.country}</span>, Color:{" "}
            <span className="olive-color">{olive.color}</span>, Rarity:{" "}
            <span className="olive-rarity">{olive.rarity}</span>
            {expandedOliveId === olive.id && (
              <ul className="olive-oil-list">
                {olive.oils.map((oil) => (
                  <li key={oil.id} className="olive-oil-list-item">
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
    </section>
  );
}

export default UserOlives;
