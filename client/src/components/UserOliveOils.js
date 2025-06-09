import React, { useContext } from 'react'
import { UserContext } from './App'

function UserOliveOils() {
    const { user } = useContext(UserContext);

    return (
        <div>
            <h1>My Olive Oils</h1>
            <ul>
                {user.oils.map((oil) => (
                <li key={oil.id}>
                    <strong>{oil.name}</strong> — Year: {oil.year}, Price: ${oil.price}
                </li>
                ))}
            </ul>
        </div>
    )
}

export default UserOliveOils
