VALID_USER = {
    "email": "kagameacu@gmail.com",
    "password": "1234"
}

INVALID_USERS = [
    {
        "case": "Invalid email format",
        "email": "not-an-email",  # Invalid format
        "password": "1234",
        "error": "Invalid email"  # Should show before OTP flow
    },
    {
        "case": "Wrong password",
        "email": "kagameacu@gmail.com",  # Valid existing email
        "password": "wrong123",
        "error": "Invalid email or password"  # The actual error message
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
    }
]