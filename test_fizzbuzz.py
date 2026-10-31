# test_fizzbuzz.py
# Apache CloudStack Marvin functional tests for the custom fizzBuzz API.

from marvin.cloudstackTestCase import cloudstackTestCase
from marvin.cloudstackException import InvalidParameterException


class TestFizzBuzz(cloudstackTestCase):
    """Functional tests for the custom fizzBuzz API."""

    def setUp(self):
        super(TestFizzBuzz, self).setUp()
        self.apiclient = self.testClient.getApiClient()

    def call_fizzbuzz(self, number):
        """
        Verify these generated-client assumptions before running:
        - API method: fizzBuzz
        - Request parameter: number
        - Response field: answer
        """
        response = self.apiclient.fizzBuzz(number=number)
        self.assertTrue(
            hasattr(response, "answer"),
            "fizzBuzz response does not contain an 'answer' field"
        )
        return response.answer

    # LEVEL 0: core specification checks

    def test_00_example(self):
        """3 must return fizz."""
        self.assertEqual(self.call_fizzbuzz(3), "fizz")

    def test_divisible_by_5_returns_buzz(self):
        self.assertEqual(self.call_fizzbuzz(5), "buzz")

    def test_divisible_by_both_returns_fizzbuzz(self):
        self.assertEqual(self.call_fizzbuzz(15), "fizzbuzz")

    def test_zero_returns_fizzbuzz(self):
        # Zero is mathematically divisible by both 3 and 5.
        self.assertEqual(self.call_fizzbuzz(0), "fizzbuzz")

    def test_missing_number_is_rejected(self):
        # Assumes None is rejected as a missing required parameter.
        with self.assertRaises(InvalidParameterException):
            self.call_fizzbuzz(None)

    # LEVEL 1: additional bug-hunting checks

    def test_other_multiples_of_3(self):
        for number in (6, 9, 12, 18, 21, 30):
            with self.subTest(number=number):
                expected = "fizzbuzz" if number % 5 == 0 else "fizz"
                self.assertEqual(self.call_fizzbuzz(number), expected)

    def test_other_multiples_of_5(self):
        for number in (10, 20, 25, 35, 40):
            with self.subTest(number=number):
                self.assertEqual(self.call_fizzbuzz(number), "buzz")

    def test_negative_integers(self):
        # The supplied specification says integer and does not exclude negatives.
        self.assertEqual(self.call_fizzbuzz(-3), "fizz")
        self.assertEqual(self.call_fizzbuzz(-5), "buzz")
        self.assertEqual(self.call_fizzbuzz(-15), "fizzbuzz")

    # LEVEL 3: optional repeatability check

    def test_same_input_returns_same_answer(self):
        expected = self.call_fizzbuzz(15)
        for attempt in range(3):
            with self.subTest(attempt=attempt + 1):
                self.assertEqual(self.call_fizzbuzz(15), expected)
        self.assertEqual(expected, "fizzbuzz")
