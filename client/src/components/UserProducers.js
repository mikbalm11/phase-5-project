import React, { useState, useContext } from "react";
import { UserContext } from "./App";
import OliveOilItem from "./OliveOilItem";

function UserProducers() {
  const { userProducers, handleEditOil, handleDeleteOil } = useContext(UserContext);
  const [expandedProducerId, setExpandedProducerId] = useState(null);

  return (
    <div>
      <h1>My Producers</h1>
      <ul>
        {userProducers.map((producer) => (
          <li key={producer.id}>
            <strong
              onClick={() =>
                setExpandedProducerId(expandedProducerId === producer.id ? null : producer.id)
              }
            >
              {producer.name}
            </strong>{" "}
            — Address: {producer.address}, Capacity: {producer.capacity}
            {expandedProducerId === producer.id && (
              <ul>
                {producer.oils.map((oil) => (
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

export default UserProducers;
