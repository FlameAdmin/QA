# fixtures/login_data.py

VALID_USER = {
    "email": "kagameacu@gmail.com",
    "password": "1234"
}

INVALID_USERS = [
    {
        "case": "Wrong email",
        "email": "wrong@gmail.com",
        "password": "1234",
        "error": "User not found"
    },
    {
        "case": "Wrong password",
        "email": "kagameacu@gmail.com",
        "password": "wrong123",
        "error": "Invalid password"
    },
    {
        "case": "Empty email",
        "email": "",
        "password": "1234",
        "error": "Email is required"
    },
    {
        "case": "Empty password",
        "email": "kagameacu@gmail.com",
        "password": "",
        "error": "Password is required"
    },
    {
        "case": "Invalid email format",
        "email": "abc",
        "password": "1234",
        "error": "Invalid email"
    }
]