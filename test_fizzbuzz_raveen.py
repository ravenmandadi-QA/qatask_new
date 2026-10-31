# test_fizzbuzz_raveen.py
# Apache CloudStack Marvin functional tests for the fizzBuzz API.

from marvin.cloudstackTestCase import cloudstackTestCase
from marvin.cloudstackException import InvalidParameterException
from marvin.cloudstackAPI import fizzBuzz


class TestFizzBuzz(cloudstackTestCase):
    """Functional tests for the fizzBuzz API."""

    def setUp(self):
        super(TestFizzBuzz, self).setUp()
        self.apiclient = self.testClient.getApiClient()

    def call_fizzbuzz(self, number):
        """Create and send a fizzBuzz API command."""

        command = fizzBuzz.fizzBuzzCmd()
        command.number = number

        response = self.apiclient.fizzBuzz(command)

        self.assertTrue(
            hasattr(response, "answer"),
            "fizzBuzz response has no 'answer' field"
        )

        return response.answer

    # LEVEL 0: Basic functional tests

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
        # The API declares number as a required parameter.
        with self.assertRaises(InvalidParameterException):
            self.call_fizzbuzz(None)

    # LEVEL 1: Additional functional tests

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
        # The specification says integer and does not exclude negatives.
        self.assertEqual(self.call_fizzbuzz(-3), "fizz")
        self.assertEqual(self.call_fizzbuzz(-5), "buzz")
        self.assertEqual(self.call_fizzbuzz(-15), "fizzbuzz")

    # LEVEL 3: Optional repeatability test

    def test_08_same_input_returns_same_answer(self):
        first_answer = self.call_fizzbuzz(15)

        for attempt in range(3):
            with self.subTest(attempt=attempt + 1):
                self.assertEqual(
                    self.call_fizzbuzz(15),
                    first_answer
                )

        self.assertEqual(first_answer, "fizzbuzz")
