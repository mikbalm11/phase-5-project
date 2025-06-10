import React, { useContext } from 'react'
import { UserContext } from './App'
import AddOilForm from './AddOilForm'

function UserOliveOils({ producers, olives, setProducers, setOlives, userProducers, userOlives, setUserProducers , setUserOlives}) {
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
            <AddOilForm
                producers={producers}
                olives={olives}
                onAddProducer={() => {}}
                onAddOlive={() => {}}
            />
        </div>
    )
}

export default UserOliveOils
