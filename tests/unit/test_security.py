from src.utils.security import sanitize_input, validate_email, validate_password_strength


class TestValidateEmail:
    def test_valid_email(self):
        assert validate_email("user@example.com") is True

    def test_invalid_email_no_at(self):
        assert validate_email("userexample.com") is False

    def test_invalid_email_no_domain(self):
        assert validate_email("user@") is False

    def test_empty_email(self):
        assert validate_email("") is False


class TestPasswordStrength:
    def test_strong_password(self):
        is_valid, _ = validate_password_strength("StrongP@ss1")
        assert is_valid is True

    def test_too_short(self):
        is_valid, msg = validate_password_strength("Ab1!")
        assert is_valid is False
        assert "8 characters" in msg

    def test_no_uppercase(self):
        is_valid, msg = validate_password_strength("lowercase1!")
        assert is_valid is False
        assert "uppercase" in msg

    def test_no_lowercase(self):
        is_valid, msg = validate_password_strength("UPPERCASE1!")
        assert is_valid is False
        assert "lowercase" in msg

    def test_no_digit(self):
        is_valid, msg = validate_password_strength("NoDigits!!")
        assert is_valid is False
        assert "digit" in msg

    def test_no_special(self):
        is_valid, msg = validate_password_strength("NoSpecial1")
        assert is_valid is False
        assert "special" in msg


class TestSanitizeInput:
    def test_xss_prevention(self):
        result = sanitize_input("<script>alert('xss')</script>")
        assert "<script>" not in result
        assert "&lt;script&gt;" in result

    def test_normal_text(self):
        result = sanitize_input("Hello World")
        assert result == "Hello World"
