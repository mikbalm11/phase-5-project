import React, { useContext } from 'react'
import { UserContext } from './App'

function UserProducers() {
  const { userProducers } = useContext(UserContext);

  return (
    <div>
      <h1>My Producers</h1>
      <ul>
        {userProducers.map((producer) => (
          <li key={producer.id}>
            <strong>{producer.name}</strong> — Address: {producer.address}, Capacity: {producer.capacity}
          </li>
        ))}
      </ul>
    </div>
  )
}

export default UserProducers
