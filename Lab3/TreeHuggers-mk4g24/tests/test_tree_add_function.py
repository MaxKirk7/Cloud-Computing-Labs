import json
import os
import unittest

import requests
from dotenv import load_dotenv

# Take note of how we import modules from shared_code
from shared_code.Tree import Tree


class TestAddTreeFunction(unittest.TestCase):
    """
    This test set focuses on testing the responses from the server on the addTree function, separated from tests of the base classes
    """

    load_dotenv()
    print(os.getenv("KEY"))
    LOCAL_DEV_URL = "http://localhost:7071/api/tree_add"
    PUBLIC_URL = "https://treehuggers-mk4g24-func-gddmarb7g9gjfbh2.belgiumcentral-01.azurewebsites.net/api/tree_add"
    TEST_URL = PUBLIC_URL
    # Experienced programmers will note the above can be improved to use environment variables. True. Out of scope for this lab

    # A valid tree
    tree_1 = Tree(
        ident=100,
        coordinates=(50.93304715, -1.3900633),
        address="85, Upper Shaftesbury Avenue, Portswood, Southampton, England, SO17 3RU, United Kingdom",
        species="Bamboo Bamboozle",
    )
    json_tree_1 = tree_1.to_json()

    # invalid trees
    tree_2 = Tree(
        ident=150,
        coordinates=(513, 513),
        address="Somewhere in the Cloud...",
        species="Bamboo Bambara",
    )

    tree_3 = Tree(ident=180, coordinates=(14, 14), address="Highfield", species="")

    def test_is_valid_correct(self):
        # note we use data instead of params as we want to send json
        # https://requests.readthedocs.io/en/latest/user/quickstart/#more-complicated-post-requests
        # response = requests.get(self.TEST_URL, data=self.json_tree_1)

        # to add the API KEY (when deployed to Azure) use this type of code
        response = requests.get(
            self.TEST_URL, data=self.json_tree_1, params={"code": os.getenv("KEY")}
        )

        # the below decodes json that we expect as response
        # https://requests.readthedocs.io/en/latest/user/quickstart/#json-response-content
        dict_response = response.json()

        self.assertTrue(dict_response["result"])
        self.assertEqual(dict_response["msg"], "OK")
        # TODO: Actually test the DB was correctly updated (Week 4)

    def test_is_valid_input(self):
        """
        Activity 2.2:
        Write a case to test we get the answer {"result": false, "msg": "Input JSON is not from a Tree"}
        """
        response = requests.get(
            self.TEST_URL,
            data=json.dumps({"id": 100}),
            params={"code": os.getenv("KEY")},
        )
        dict_response = response.json()
        self.assertFalse(dict_response["result"])
        self.assertEqual(dict_response["msg"], "Input JSON is not from a Tree")

    def test_is_valid_coordinates(self):
        """
        Activity 2.2:
        Write a case to test we get the answer {"result": false, "msg": "Bad Coordinates"}
        -- Yes, 'msg' should be the message of the exception triggered by is_valid, but we'll let you off the hook as there are many things to do ;)
        """
        invalid_tree = {
            "id": 150,
            "coordinates": (513, 513),
            "address": "Somewhere in the Cloud...",
            "species": "Bamboo Bambara",
        }
        response = requests.get(
            self.TEST_URL,
            data=json.dumps(invalid_tree),
            params={"code": os.getenv("KEY")},
        )
        dict_response = response.json()
        self.assertFalse(dict_response["result"])
        self.assertEqual(dict_response["msg"], "Bad Coordinates")
