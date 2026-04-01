from src.services.auth_service import AuthService


class TestAuthService:
    def test_hash_and_verify_password(self):
        password = "TestP@ss123"
        hashed = AuthService.hash_password(password)
        assert hashed != password
        assert AuthService.verify_password(password, hashed) is True

    def test_verify_wrong_password(self):
        hashed = AuthService.hash_password("CorrectP@ss1")
        assert AuthService.verify_password("WrongP@ss1", hashed) is False

    def test_create_and_decode_token(self):
        token = AuthService.create_access_token(user_id=1, email="test@example.com")
        payload = AuthService.decode_token(token)
        assert payload is not None
        assert payload["sub"] == "1"
        assert payload["email"] == "test@example.com"

    def test_decode_invalid_token(self):
        result = AuthService.decode_token("invalid.token.here")
        assert result is None
