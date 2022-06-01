import requests
from faker import Faker
from clients.matchbook_client import MatchBookClient
from assertpy import assert_that
import unittest
import string
import random
import jsonpath


class LoginTest(unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.client = MatchBookClient()
        self.fake = Faker()  # this is a library used to generate

    def test_valid_login(self):
        payload = {
            'username': 'QA_ITW6',
            'password': 'PCBvJvY5FZ'
        }

        response = self.client.login(payload)

        # verify the status code of the response
        assert_that(response.status_code).is_equal_to(requests.codes.ok)

        # parse the response to json format
        json_response = response.json()

        # note that the response body is stored as a list

        # get the user_Id and the email of the user
        user_id = jsonpath.jsonpath(json_response, "user-id")
        email = jsonpath.jsonpath(json_response, "account.email")

        # verify the values of the user Id and the email
        assert_that(user_id).is_equal_to([426924])
        assert_that(email).is_equal_to(['cmadotto9@xanadu.ie'])

    def test_invalid_password_login(self):
        invalid_password = self.fake.password()
        payload = {
            'username': 'QA_ITW6',
            'password': invalid_password
        }
        response = self.client.login(payload)
        assert_that(response.status_code).is_equal_to(requests.codes.bad_request)

        # parse the response to json format
        json_response = response.json()

        # note that the response body is stored as a list
        # To get the error message in the response body, the index 0 is used to get that
        messages = jsonpath.jsonpath(json_response, "errors[0].messages")

        # verify that the response body contains the right error message
        assert_that(messages).is_equal_to([['Incorrect credentials. Please try again or reset your password.']])

    def test_login_with_empty_fields(self):
        payload = {
            'username': '',
            'password': ''
        }
        response = self.client.login(payload)
        assert_that(response.status_code).is_equal_to(requests.codes.bad_request)

        # parse the response to json format
        json_response = response.json()

        # note that the response body is stored as a list
        # To get the error message in the response body, the index 0 is used to get that
        messages = jsonpath.jsonpath(json_response, "errors[0].messages")

        # verify that the response body contains the right error message
        assert_that(messages).is_equal_to([['Incorrect credentials. Please try again or reset your password.']])

    def test_login_with_invalid_username(self):
        # this generates a string which contains both lower and upper case characters
        # and then store it in "invalid _username" variable
        invalid_username = string.ascii_letters

        # this randomly generates a string of 10 characters from the initial value of "invalid_username"
        invalid_username = (''.join(random.choice(invalid_username) for i in range(10)))

        payload = {
            'username': invalid_username,
            'password': 'PCBvJvY5FZ'
        }
        response = self.client.login(payload)
        assert_that(response.status_code).is_equal_to(requests.codes.bad_request)

        # parse the response to json format
        json_response = response.json()

        # note that the response body is stored as a list
        # To get the error message in the response body, the index 0 is used to get that
        messages = jsonpath.jsonpath(json_response, "errors[0].messages")

        # verify that the response body contains the right error message
        assert_that(messages).is_equal_to([['Incorrect credentials. Please try again or reset your password.']])
