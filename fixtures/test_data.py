import pytest

# # ============== LOGIN TEST DATA ==============

# @pytest.fixture
# def valid_login_credentials():
#     """Valid login credentials"""
#     return {
#         "email": "kagameacu@gmail.com",
#         "password": "1234",
#         "expected_result": "success",
#         "expected_url": r".*user/home.*"
#     }

# @pytest.fixture
# def invalid_login_data():
#     """Invalid login scenarios"""
#     return [
#         {
#             "email": "wrong@email.com",
#             "password": "1234",
#             "expected_result": "error",
#             "expected_message": "Invalid email or password"
#         },
#         {
#             "email": "kagameacu@gmail.com",
#             "password": "wrongpassword",
#             "expected_result": "error",
#             "expected_message": "Invalid email or password"
#         },
#         {
#             "email": "invalid-email",
#             "password": "1234",
#             "expected_result": "error",
#             "expected_message": "Please enter a valid email"
#         },
#         {
#             "email": "",
#             "password": "1234",
#             "expected_result": "error",
#             "expected_message": "Email is required"
#         },
#         {
#             "email": "kagameacu@gmail.com",
#             "password": "",
#             "expected_result": "error",
#             "expected_message": "Password is required"
#         },
#         {
#             "email": "test@test.com",
#             "password": "123",
#             "expected_result": "error",
#             "expected_message": "Password must be at least 4 characters"
#         }
#     ]

# @pytest.fixture
# def edge_case_login_data():
#     """Edge cases for login"""
#     return [
#         {
#             "email": "user+test@gmail.com",
#             "password": "Test@123",
#             "description": "Email with plus sign"
#         },
#         {
#             "email": "user.test@domain.co.uk",
#             "password": "Test@123",
#             "description": "Email with subdomain"
#         },
#         {
#             "email": "user@sub.domain.com",
#             "password": "Test@123",
#             "description": "Email with multiple dots"
#         }
#     ]

# # ============== REGISTRATION TEST DATA ==============

# @pytest.fixture
# def invalid_registration_data():
#     """Invalid registration scenarios"""
#     return [
#         {
#             "email": "invalid-email",
#             "password": "Test@123",
#             "confirm_password": "Test@123",
#             "expected_error": "Please enter a valid email"
#         },
#         {
#             "email": "test@example.com",
#             "password": "123",
#             "confirm_password": "123",
#             "expected_error": "Password must be at least 4 characters"
#         },
#         {
#             "email": "test@example.com",
#             "password": "Test@123",
#             "confirm_password": "Different123",
#             "expected_error": "Passwords do not match"
#         },
#         {
#             "email": "",
#             "password": "Test@123",
#             "confirm_password": "Test@123",
#             "expected_error": "Email is required"
#         }
#     ]

# # ============== REDEEM TEST DATA ==============

# @pytest.fixture
# def redeem_test_data():
#     """Redeem test scenarios"""
#     return [
#         {
#             "amount": 10,
#             "expected_result": "success",
#             "description": "Valid redemption - minimum amount"
#         },
#         {
#             "amount": 100,
#             "expected_result": "success",
#             "description": "Valid redemption - medium amount"
#         },
#         {
#             "amount": 0,
#             "expected_result": "error",
#             "expected_message": "Amount must be greater than 0",
#             "description": "Zero amount"
#         },
#         {
#             "amount": -10,
#             "expected_result": "error",
#             "expected_message": "Amount must be positive",
#             "description": "Negative amount"
#         },
#         {
#             "amount": 999999,
#             "expected_result": "error",
#             "expected_message": "Insufficient points",
#             "description": "Amount exceeds available points"
#         }
#     ]




@pytest.fixture
def existing_user():
    return {
        "email": "kagameacu@gmail.com",
        "password": "1234"
    }

@pytest.fixture
def new_user():
    return {
        "email": "hamid123a2008@gmail.com",
        "otp": "572004",
        "name": "Sara",
        "password": "1234",
        "gender": "B",
        "bio": "Hello this is Sara",
        "values": ["Optimism", "Compassion", "Authenticity"],
        "flaws": ["Cowardice", "Grouchiness", "Intolerance"],
        "primary_photo": "avatar-3.png",
        "secondary_photo": "avatar-2.png"
    }