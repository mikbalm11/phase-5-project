import React, { useContext } from 'react'
import { UserContext } from './App'

function UserProducers() {
    const { user } = useContext(UserContext);

    return (
        <div>
            <h1>My Producers</h1>
            <ul>
                {user.oils.map((oil) => (
                <li key={oil.producer.id}>
                    <strong>{oil.producer.name}</strong> — Address: {oil.producer.address}, Capacity: {oil.producer.capacity}
                </li>
                ))}
            </ul>
        </div>
    )
}

export default UserProducers
