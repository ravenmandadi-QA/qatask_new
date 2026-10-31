# test_fizzbuzz_latest_new.py
# Apache CloudStack Marvin functional tests for the custom fizzBuzz API.

from marvin.cloudstackTestCase import cloudstackTestCase
from marvin.cloudstackException import InvalidParameterException


class TestFizzBuzz(cloudstackTestCase):
    """Functional tests for the custom fizzBuzz API."""

    def setUp(self):
        # Marvin provides the configured API client for this test.
        self.apiclient = self.testClient.getApiClient()

    def call_fizzbuzz(self, number):
        """
        Send one API request and return its answer.

        Assumptions:
        1. Marvin generated a method named fizzBuzz.
        2. The response object has a field named answer.
        """
        response = self.apiclient.fizzBuzz(number=number)

        self.assertTrue(
            hasattr(response, "answer"),
            "fizzBuzz response has no 'answer' field"
        )
        return response.answer

    # LEVEL 0: core tests

    def test_00_divisible_by_3_returns_fizz(self):
        self.assertEqual(self.call_fizzbuzz(3), "fizz")

    def test_01_divisible_by_5_returns_buzz(self):
        self.assertEqual(self.call_fizzbuzz(5), "buzz")

    def test_02_divisible_by_both_returns_fizzbuzz(self):
        self.assertEqual(self.call_fizzbuzz(15), "fizzbuzz")

    def test_03_zero_returns_fizzbuzz(self):
        # Zero is divisible by both 3 and 5.
        self.assertEqual(self.call_fizzbuzz(0), "fizzbuzz")

    def test_04_missing_number_is_rejected(self):
        # Assumes the API declares number as a required parameter.
        with self.assertRaises(InvalidParameterException):
            self.call_fizzbuzz(None)

    # LEVEL 1: wider bug-hunting scope

    def test_05_other_multiples_of_3(self):
        for number in (6, 9, 12, 18, 21, 30):
            with self.subTest(number=number):
                expected = "fizzbuzz" if number % 5 == 0 else "fizz"
                self.assertEqual(self.call_fizzbuzz(number), expected)

    def test_06_other_multiples_of_5(self):
        for number in (10, 20, 25, 35, 40):
            with self.subTest(number=number):
                self.assertEqual(self.call_fizzbuzz(number), "buzz")

    def test_07_negative_integers(self):
        # The task says integer and does not exclude negative values.
        self.assertEqual(self.call_fizzbuzz(-3), "fizz")
        self.assertEqual(self.call_fizzbuzz(-5), "buzz")
        self.assertEqual(self.call_fizzbuzz(-15), "fizzbuzz")

    # LEVEL 3 (OPTIONAL): repeatability check

    def test_08_same_input_returns_same_answer(self):
        first_answer = self.call_fizzbuzz(15)
        for attempt in range(3):
            with self.subTest(attempt=attempt + 1):
                self.assertEqual(self.call_fizzbuzz(15), first_answer)
        self.assertEqual(first_answer, "fizzbuzz")
