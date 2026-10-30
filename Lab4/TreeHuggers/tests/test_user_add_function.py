import json
import unittest

import requests
from azure.cosmos import CosmosClient
from shared_code.User import User


class TestAddUserFunction(unittest.TestCase):
    LOCAL_DEV_URL = "http://localhost:7071/user/add"
    # you may need to change this if you have removed the api from URLs in your host.json file
    PUBLIC_URL = "https://your-deployment-url/api/user/add"
    TEST_URL = LOCAL_DEV_URL

    # Sadly, tests don't have local.settings.json available as environment variables
    # Hence, we have to parse it manually
    # Note you have to run tests from the project folder and not from the test fodler, otherwise the
    with open("local.settings.json") as settings_file:
        settings = json.load(settings_file)
    MyCosmos = CosmosClient.from_connection_string(
        settings["Values"]["AzureCosmosDBConnectionString"]
    )
    TreeHuggersDBProxy = MyCosmos.get_database_client(
        settings["Values"]["DatabaseName"]
    )
    UserContainerProxy = TreeHuggersDBProxy.get_container_client(
        settings["Values"]["UserContainerName"]
    )
    api_key = settings["Values"]["FunctionAppKey"]

    # remember to pass in the API key. This is not needed to run locally but adding here
    # for when you deploy to Azure. You can find the key in the local.settings.json file
    HEADERS = {"x-functions-key": api_key, "Content-Type": "application/json"}

    def test_user_add_valid(self):
        valid_user = User(name="Ilika", city="Cardiff")
        response = requests.post(
            self.TEST_URL, headers=self.HEADERS, data=valid_user.to_json()
        )
        # For brevity, just check the response code
        self.assertEqual(200, response.status_code)
        # Now we do the check directly in the DB (Similar how it will be done for marking ;)
        query_result = self.UserContainerProxy.read_item("Ilika", partition_key="Ilika")
        # Remember documents in DB include Cosmos metadata, we need to strip that for comparison
        # we also store the name as id
        query_result_stripped = {
            "name": query_result["id"],
            "city": query_result["city"],
        }
        self.assertEqual(query_result_stripped, valid_user.to_dict())

    def tearDown(self) -> None:
        # TODO: Uncomment the lines of code to clean up the User container after each test. This is important to ensure that tests are independent and do not interfere with each other.
        # Use the read_all_items() method of ContainerProxy to delete all items in the container
        for doc in self.UserContainerProxy.read_all_items():
            self.UserContainerProxy.delete_item(item=doc, partition_key=doc["id"])
