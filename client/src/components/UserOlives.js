

function UserOlives({ user }) {
    return (
        <div>
            <h1>My Olives</h1>
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

export default UserOlives
