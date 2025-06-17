from django.test import TestCase
from lms_core.utils import calculator, validate_password


class CalculatorFunctionTest(TestCase):
    def test_addition(self):
        self.assertEqual(calculator(1, 2, '+'), 3)
        self.assertEqual(calculator(-1, -1, '+'), -2)
        self.assertEqual(calculator(0, 5, '+'), 5)

    def test_subtraction(self):
        self.assertEqual(calculator(5, 3, '-'), 2)
        self.assertEqual(calculator(-1, -1, '-'), 0)
        self.assertEqual(calculator(0, 5, '-'), -5)

    def test_multiplication(self):
        self.assertEqual(calculator(3, 4, 'x'), 12)
        self.assertEqual(calculator(-1, 5, 'x'), -5)
        self.assertEqual(calculator(0, 5, 'x'), 0)

    def test_division(self):
        self.assertEqual(calculator(10, 2, '/'), 5)
        self.assertEqual(calculator(-10, 2, '/'), -5)
        self.assertEqual(calculator(0, 1, '/'), 0)

    def test_division_by_zero(self):
        with self.assertRaises(ValueError) as context:
            calculator(10, 0, '/')
        self.assertEqual(str(context.exception), "Cannot divide by zero")

    def test_invalid_operator(self):
        with self.assertRaises(ValueError) as context:
            calculator(10, 5, '%')
        self.assertEqual(str(context.exception), "Invalid operator")
    #validate password
class PasswordValidationTest(TestCase):
    def test_valid_password(self):
        self.assertTrue(validate_password("PassValid1!"))
        self.assertTrue(validate_password("StrongPassword1@"))
        self.assertTrue(validate_password("Another$Valid2"))

    def test_invalid_password_length(self):
        self.assertFalse(validate_password("Short1!")) # Terlalu pendek

    def test_invalid_password_no_uppercase(self):
        self.assertFalse(validate_password("invalidpassword1!")) # Tidak ada huruf besar

    def test_invalid_password_no_lowercase(self):
        self.assertFalse(validate_password("INVALIDPASSWORD1!")) # Tidak ada huruf kecil

    def test_invalid_password_no_digit(self):
        self.assertFalse(validate_password("NoDigit!")) # Tidak ada angka

    def test_invalid_password_no_special_char(self):
        self.assertFalse(validate_password("NoSpecialChar1")) # Tidak ada karakter khusus
