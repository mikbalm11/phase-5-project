import React, { useState, useContext } from "react";
import { UserContext } from "./App";
import OliveOilItem from "./OliveOilItem";

function UserProducers() {
  const { userProducers, handleEditOil, handleDeleteOil } = useContext(UserContext);
  const [expandedProducerId, setExpandedProducerId] = useState(null);

  return (
    <section className="user-producers">
      <h1>My Producers</h1>
      <ul className="producer-list">
        {userProducers.map((producer) => (
          <li key={producer.id} className="producer-list-item">
            <strong
              className="producer-name"
              onClick={() =>
                setExpandedProducerId(expandedProducerId === producer.id ? null : producer.id)
              }
              role="button"
              aria-expanded={expandedProducerId === producer.id}
            >
              {producer.name}
            </strong>{" "}
            — <span className="producer-address">Address: {producer.address}</span>,{" "}
            <span className="producer-capacity">Capacity: {producer.capacity}</span>
            {expandedProducerId === producer.id && (
              <ul className="producer-oil-list">
                {producer.oils.map((oil) => (
                  <li key={oil.id} className="producer-oil-list-item">
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

export default UserProducers;
