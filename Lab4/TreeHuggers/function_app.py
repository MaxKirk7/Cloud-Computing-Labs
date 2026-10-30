import azure.functions as func
import datetime
import json
import logging

from azure.functions import HttpRequest, HttpResponse
from shared_code.Tree import Tree, BadCoordinateError


# To access variables in local.settings.json
# each entry in the dictionary "Values" in local.settings.json is made available as an environment variable when you run func start
# This also works when
import os
# Library to interact with a CosmosDB library
# install it with python -m pip install azure-cosmos in your virtual environment
from azure.cosmos import CosmosClient 
# Exceptions returned by ProxyObjects
# Consult the reference here: https://learn.microsoft.com/en-us/python/api/azure-cosmos/azure.cosmos.exceptions?view=azure-python
from azure.cosmos.exceptions import CosmosHttpResponseError, CosmosResourceExistsError, CosmosResourceNotFoundError

# ProxyObjects to account, database and container respectively
# This is one approach that can be used. Another is to use the CosmosDB input and output bindings, as we will see in the next lab.
# Either approach can be used. Both are shown here so you get an idea of how to use them.
# Generally, better to use one or the other and not both in the same function app

MyCosmos = CosmosClient.from_connection_string(os.environ['AzureCosmosDBConnectionString'])
TreeHuggersDBProxy = MyCosmos.get_database_client(os.environ['DatabaseName'])
TreeContainerProxy = TreeHuggersDBProxy.get_container_client(os.environ['TreeContainerName'])



app = func.FunctionApp()



@app.route(route="tree/search", methods=[func.HttpMethod.GET], auth_level=func.AuthLevel.FUNCTION)
def tree_search(req: func.HttpRequest) -> func.HttpResponse:
    filter_param = req.params.get('filter')
    logging.info('Buckle up, we weere asked to filter trees by parameter {}'.format(filter))

    ### TODO: Activity 3
    # Create appropriate ProxyObjects to the Tree collection to implement tree_search function as follows
    # Input: request with query parameter 'filter=XX' with XX a   
    # Output: JSON array representing list of Trees where the Address field includes the string 'XX'
    # For example, if Tree1 has address = "1, Highfield Road, SO17 1BJ, Southampton", 
    # Tree2 has address = "1, Highfield Road, PO17 1BJ, Portsmouth"
    # and filter="Southampton"
    # the output must be a list containing the Tree1 JSON representation.
    # The same tree with filter="Highfield" returns a list with both Tree1 and Tree2
    # Consider the search case-insensitive      
    ###

@app.route(route="tree/add", methods=[func.HttpMethod.POST], auth_level=func.AuthLevel.FUNCTION)
def tree_add(req: func.HttpRequest) -> func.HttpResponse:
    # get_json() decodes the received JSON string into a dict  
    try:
        input_json = req.get_json()
        logging.info('Buckle up, we got a request to add a tree from this JSON: {}'.format(input))
        input_tree = Tree(ident=0)           
        input_tree.from_dict(input_json)
    except ValueError:
        # we got the exception we implemented in from_dict method
        # return appropriate HttpResponse
        logging.info("Value Error caught from input {}".format(input_json))
        response_body = json.dumps({"result": False, "msg": "Input JSON is not from a Tree"}, status_code=400)
        return HttpResponse(body=response_body,mimetype="application/json")

    try:
        if input_tree.is_valid():
            #Method to create item in a container
            #Read the reference here: https://learn.microsoft.com/en-us/python/api/azure-cosmos/azure.cosmos.containerproxy?view=azure-python#azure-cosmos-containerproxy-create-item 
            
            TreeContainerProxy.create_item(input_tree.to_dict(),enable_automatic_id_generation=True)
            return HttpResponse(body=json.dumps({"result": True , "msg" : "OK"}),mimetype="application/json", status_code=200)
    except BadCoordinateError:
        # We got BadCoordinate from is_valid method, return appropriate HttpResponse
        # The spec does not distinguish between the two types of BadCoordinate error, so we return the same message
        response_body = json.dumps({"result": False, "msg": "Bad Coordinates"})
        return HttpResponse(body=response_body,mimetype="application/json", status_code=400)
    except CosmosHttpResponseError as cosmoserr:
        #Note from the documentation of create_item that this exception is returned if an item with the same id already exists
        logging.info(cosmoserr)
        response_body = json.dumps(body={"result": False, "msg": "Tree with input id already exist"},mimetype="application/json", status_code=409)


@app.route(route="user/add", methods=[func.HttpMethod.POST], auth_level=func.AuthLevel.FUNCTION)
@app.cosmos_db_output(
    arg_name="usercontainerbinding",
    database_name=os.environ['DatabaseName'],
    container_name=os.environ['UserContainerName'],
    connection="AzureCosmosDBConnectionString",
)    
def user_add(req: func.HttpRequest, 
             usercontainerbinding: func.Out[func.Document]) -> func.HttpResponse:
    req_body = req.get_json()
    logging.info('Buckle up, we are requested to add an user from this {}'.format(req_body))

    #Note that as class User use "name", we need to convert that to "id" to match the schema in the container

    try:
        user_doc = {"id": req_body['name'], "city": req_body['city']}
    except Exception as err:
        return HttpResponse("Something unexpected and bad happened, probably wrong formatted input. Look at it: {}".format(req_body),status_code=400)    
    
    try:
        #Create object of type Azure Document from the request
        # https://learn.microsoft.com/en-us/python/api/azure-functions/azure.functions.document?view=azure-python#azure-functions-document-from-dict
        user_doc_for_cosmos = func.Document.from_dict(user_doc)
        # user_container_binding is a ProxyObject to the container in the DB
        # the set(method) inserts the document
        # Note this demonstrates usage. One downside of this is that if there is a conflict
        # i.e. the tree already exists then it will just overwrite it rather than raise an exception
        # If you look at the openapi spec, it says tehre should be an error code returned if the tree already exists. 
        # This is not implemented here, but you can do it if you want to.
        usercontainerbinding.set(user_doc_for_cosmos)
        logging.info("Out binding successfully set")
        return HttpResponse("User {} inserted".format(user_doc),status_code=200)
    except Exception as err:
        logging.exception(err)
        return HttpResponse("Something unexpected and bad happened during insertion, look at the server log",status_code=500)    

@app.route(route="user/delete/{name}", methods=[func.HttpMethod.DELETE], auth_level=func.AuthLevel.FUNCTION)
def user_delete(req: func.HttpRequest) -> func.HttpResponse:
    name = req.route_params.get('name')
    
    logging.info('Buckle up, we got a request to delete a user with this name : {}'.format(name))

    ### TODO: Activity 2
    # Create an appropriate ProxyObject to the User collection and use it to implement delete user as follows
    # Input: Request with query parameter "name=XX" with XX the username to delete (No JSON input this time!)
    # Output (Stil JSON this time!):
    # {'result': true , 'msg': "User deleted"} if user deleted succesfully
    # {'result': false, 'msg' : "User does not exist"} if user asked to delete does not exist in the DB  
    # Hint: You need to read and understand method delete_item https://learn.microsoft.com/en-us/python/api/azure-cosmos/azure.cosmos.containerproxy?view=azure-python#azure-cosmos-containerproxy-delete-item
    # Hint2: the pre_trigger_include and post_trigger_include parameters have default values = None that you can leave. This means you just need to understand how to use of the id and partition_key parameters  
    # 
    ### 