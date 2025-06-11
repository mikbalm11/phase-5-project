import React, { useContext } from 'react'
import { UserContext } from './App'

function UserOlives() {
  const { userOlives } = useContext(UserContext);

  return (
    <div>
      <h1>My Olives</h1>
      <ul>
        {userOlives.map((olive) => (
          <li key={olive.id}>
            <strong>{olive.name}</strong> — {olive.region}, {olive.country}, Color: {olive.color}, Rarity: {olive.rarity}
          </li>
        ))}
      </ul>
    </div>
  )
}

export default UserOlives
