# COMP3207 - Azure Cosmos - Lab 4

Now you know how to create functions to run on Azure, let's look at how to connect these functions to a database so data can be persisted.

## Lab Goals

By the end of this lab you will have:

1. Created a ContentSafety resource
2. Created necessary CosmosDB resources for deployment
3. Create proxy objects for accounts, databases, and containers
4. Create/delete documents in containers
5. Query containers with SQL
6. Configure application settings in a FunctionApp

You will then be in a position to complete the first assignment.

## 0. Pre-requisites

* Lab 1 completed. i.e. you have an Azure account and setup your machine
* Lab 2 completed i.e., you have reacquainted yourself with coding in Python and have gained familiarity with the TreeHuggers application
* Lab 3 completed. You have Azure functions set up already and know how to deploy them to Azure.
* Lectures on Cosmos. You know what Cosmos DB is

## 1. Activity 1 - Configure Content Safety

As a reminder, Content Safety is needed for the first assignment. This activity sets it up and enables you to try it out. You can read more about [Content Safety](https://learn.microsoft.com/en-us/azure/ai-services/content-safety/overview). The link contains resources to learn how to use it programatically via an API.

On your Azure portal, click on "Create Resource" and search for "content safety". Locate Azure AI Content Safety and click on "Create"

![azure_content_safety](img/azure_content_safety.png)

![azure_content_safety](img/azure_content_safety2.png)

Ensure is Azure for Students, and Azure AI Content Safety. Create a new resource group for it (we will use it for CW too), set the region to one of your assigned regions (refer to Lab 3 to find them), set name to unique name, e.g. content-safety-vj3g25 (use your student name), Pricing Tier should be Free F0

![azure_content_safety](img/azure_content_safety3.png)

Hit Review + Create, now you see the review screen. Hit Create

![azure_content_safety](img/azure_content_safety4.png)

Now you see the success screen. Click on Go to Resource

![azure_content_safety](img/azure_content_safety5.png)

Configure the access control by selecting Access Control on the left-side

![azure_content_safety](img/azure_content_safety7.png)

Select Add role assignment within Grant access to this resource



Search for Cognitive Services user

Click on it to select it (note the grey highlight), then click Next

![azure_content_safety](img/azure_content_safety8.png)

Within members, hit Select members, search for your student id and click it, then click select

![azure_content_safety](img/azure_content_safety9.png)

You should now be listed as member, click Review + Assign

![azure_content_safety](img/azure_content_safety10.png)

Success

<img src="img/azure_content_safety12.png" alt="azure_content_safety" style="zoom:67%;" />

Back to the overview page, click the content resource you just created.

<img src="img/azure_content_safety13.png" alt="azure_content_safety" style="zoom:67%;" />



Click Content Safety Studio link at the bottom of 2 Make an API call

![azure_content_safety](img/azure_content_safety14.png)

Hit Try It Out under the Moderate Text Content box

You may need to login again using your Azure account (look at top right)

Once logged in, you will need to click the link within the sentence "I acknowledge this demo....." and choose your newly created content safety resource.

Note: You may need to wait a few minutes before the Try It Out works properly. It seems it takes a few minutes for the role to be fully assigned and you may get an error message about not having access. This error went away after a few minutes.

Play with it and inspect the code samples to understand how to call the service from a request

Under keys, you can get the access keys and the endpoint URL to call the API.

![azure_content_safety](img/azure_content_safety15.png)

## 2. Activity 2 - Create CosmosDB resources

On your Azure portal, click on "Create Resource" and search for "Azure Cosmos DB". Locate it and click on "Create"

![Cosmos](img/cosmos.png)

Select Create under Azure Cosmos DB for NoSQL

![Cosmos](img/cosmos2.png)



Set WorkloadType to Learning, select Azure for Students, create a new resource group, input a unique name for the account name, select one of your assigned regions, leave defaults under Capacity Mode, Apply Free Tier Discount, and Limit your account throughput. Then choose Review + create

Set to periodic, leave the defaults and ensure redundancy is set to Locally-redundant backup storage

Then go to Review+Create

Hit Create

Success, hit Go to resource

Read [this](https://learn.microsoft.com/en-us/azure/cost-management-billing/manage/check-free-service-usage?source=recommendations) before continuing about how to monitor your Azure free usage

Key points:

* Use this account to hold all your DBs and containers for lab and CW1
* The combined provisioned throughput of all DBs must be less than 1000 R/Us
* Any other account you create will not be covered by the free tier. A serverless account would consume little money, but still consume (For CW2, you can use this mode as for that we expect you to spend some credits to do nice things, or you can delete the treehuggers DB)
* A provisioned throughput account without the free tier consumes credits quite fast, even if idle

### Access Keys for requests

Look at the Keys on the left side. You may have to search for them. Make a note of the URI and the Primary Connection String as you will need these to connect your functions to the database

### Activity 2 - Create the database

Before creating the containers, a database needs to be created.

Now select Data Explorer on the left side.

Select Create a database under + New

![Cosmos](img/cosmos3a.png)

Enter a database id such as treehuggers-USERID. Hit OK

Note that for the coursework, you create another database with 400 RU/s. If you need one for CW2 then delete the treehuggers one to make room

### Document Schema for Tree Huggers

This is the document schema for our database, let's create it. Each document type needs its own container. For the purposes of this lab, we will just create the Users and Trees containers.

```json
Users
{
  "id": "Bob",
  "city": "Southampton",
}
```

```json
Trees
{
  "id":"100",
	"coordinates":{"lat":20, "lng":40}, 
	"species":"oak",
	"address":"highfield"
}
```

```json
Stories
{
  "story_id": "333",
  "username": "Bob",
  "tree_id": 100,
  "story_text": "Howdy!",
  "date":"20-10-2026"
}
```

To create it:

Choose New Container, use the existing database just created, enter Users as the Container id, and enter /id as Partition key, Tick manual container throughput, leave 400 as the default Database Required RU/s. Then hit OK

![Cosmos](img/cosmos3b.png)

Then hit OK to create the container

Repeat these steps to create a Trees container also with /id as Partition Key

Load the users.json file included with the lab code into the users collection. To do this, select the Upload Item.

![Cosmos](img/cosmos4.png)

CosmosDB adds metadata to your items

#### Importance of the "id" field

All items in a container must have an "id" string field:

* Either you let CosmosDB autogenerate a UUID for it
* Or you set it yourself as the unique id of your items

## 3. Activity 3 - Inserting in Container

Go to your work area and activate your virtual environment

* You should have already installed `requests` and `azure-functions` in Lab 3
* Now install `azure-cosmos` remember, `pip install azure-cosmos`
* Unzip the lab's code into your work area or VS Code project, it contains a FunctionApp. Be mindful of getting the right folder structure
  * Alternatively, create a fresh VS Code project and copy files there
  * Before coding, we will first inspect the new material

### openapi.json
This file is the OpenAPI file that specifies the API endpoints that are available. If you open it up, you will see it is a JSON file. A nicer presentation is if you view the *swagger.html* file as this presents the JSON is a more readable and user friendly manner. The accompanying README.md file tells you how to configure VS Code to view the html or use a basic python webserver. 

You can see the OpenAPI file defines 5 endpoints. Different HTTP methods are used (POST, GET, DELETE) and different responses are returned. 

These endpoints are defined in the *function_app.py* file

### Local.settings.json

Open *local.settings.json*, this is where local configuration is set

Fill the values:

* *AzureCosmosDBConnectionString* with the primary connection string to your account noted earlier
* *DatabaseName*, *TreeContainerName*, *UserContainerName* with the appropriate names as created earlier in this guide

These values will be available to your FunctionApp through environment variables. Short examples from Azure docs [here](https://learn.microsoft.com/en-us/azure/azure-functions/functions-reference-python?pivots=python-mode-decorators#environment-variables)



### function_app.py

This contains the defined API routes and accompanying functions. This approach of defining them in a single file is recommended when using v2 Azure Python functions. Indeed, Microsoft have recently deprecated the v1 approach of having a separate folder and __init__.py file for each function. If you look in this file, you will see four functions defined each with its own route. You should follow this approach for the coursework.

### Adding an user with an out binding

Inspect the *user_add* function and take note of how:

* The use of the *cosmos_db_output* decorator and how the *os.environ* function is used to access the values defined in *local.setttings.json*
* The *Out* and *Document* classes are used to insert a user in the user collection

### Adding a Tree using Proxy Objects

Inspect the *tree_add* function and take note of how:

* Proxy objects to the treehuggers database and the Tree container are instantiated
  * The Proxy to the container is the most important. Read its reference, focusing on methods about items (methods about conflicts are out of scope)
* The *TreeContainerProxy* object is used to add a tree
* The *CosmosHttpResponseError* exception is handled to return an appropriate response

### Cosmos Proxy vs. out binding

Binding is faster and less code, but you can only insert or replace ("overwrite"), not delete

CosmosProxy is slightly slower and requires more code, but allows deletion and querying

You can choose either for CW1 Part 1

### Testing a DB insert

* Inspect *tests/test_add_user_function.py* and note how:

  * Configuration variables are accessed. Tests don't have access to them as environment variables, so we need to load them from *local.settings.json*

  * How containerProxy objects are used to read from the DB and check the DB was updated as expected

* Start your development server (remember how to from Lab 3)

* Run the test from the project folder
  * Remember to activate your Python environment within your terminal first
  * `python -m unittest tests/test_user_add_function.py`
  * it should pass
* In the Azure portal, go to the Data Explorer, and confirm the test user was added to the users container. Use the Azure UI to delete this user.
* Note the tearDown function is commented out for now so that you can manually check the test user was added to the database. Now you can see it is, you may want to let the tear down delete users otherwise tests may fail due to duplicate usernames.
* Note also you can run simple tests via the swagger.html file. If you have the swagger.html file open in a browser (say via the VS Code integrated browser), go to the declaration of /user/add and hit Try it out. Then hit execute. You should see a successful response. You can check it was inserted correctly via the Azure portal.

## 4. Activity 4 - Delete User

Implement the *user_delete* function

## 5. Activity 5 - Queries

Implement the *tree_search* function

You must read the reference of the query_items method [here](https://learn.microsoft.com/en-us/python/api/azure-cosmos/azure.cosmos.containerproxy?view=azure-python#azure-cosmos-containerproxy-query-items)

And the available subset of SQL [here](https://learn.microsoft.com/en-us/azure/cosmos-db/nosql/query/)

## 6. Activity 6 - Configuring deployment settings

For security, Azure does not deploy *local.settings.json* to the cloud

* Meaning that if you deploy treehuggers now it won't work

We need to set the "Application Settings" in the Azure Portal

Everything you access from *local.settings.json* using *os.environ* must be replicated in the "Application Settings"

Go to the overview of your Treehuggers FunctionApp and look for Environment Variables

![FunctionApp](img/function_app.png)

Add as "app settings", the connection strings, names of DB and containers. Be careful to use the same names from *local.settings.json*

Note the connection strings tab on this screen is for a different type of connection strings that are out of scope. The CosmosDB connection strings must be added as App settings

Redeploy your app - remember how to from prior Lab. Remember also to regenerate the requirements.txt so the list of Python packages is updated.

Test the deployment works as expected

* Be careful! It is easy to forget to switch the URLs in the unit tests from local to deployment

## 7. Activity 7 (Optional) - Delete Tree

As a bonus, add and complete the function to delete a tree as per the specification in the *openapi.json* file. This will require you to add a new route and code to the *function_app.py* file. 

## In real life...

You would:

* Have separate collections for test data, likely in different CosmosDB accounts
* Have separate configuration files for test and production FunctionApps
* Not know the production access details. Highly locked down!
* Microsoft also sells the Key Vault for extra safe storage of keys (out of scope for this module). Other vendors have similar tools.
* Not use the Azure GUI to configure Azure. You would either use the CLI, a platform your company provides, tooling to automate the setup such as Terraform, or some combination of all of these.

## Next Steps

Use the knowledge gained in this lab to complete the first assignment.



