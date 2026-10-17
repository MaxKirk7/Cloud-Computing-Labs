# COMP3207 - Python - Lab 2

We are assuming that you know how to code in Python already as you were taught it in Year 1.

This lab gives you an opportunity on brushing up your skills before the later labs. 

Completing this lab is  beneficial for the later labs as they will use the same TreeHugger set of requirements and codebase used in this lab. The difference is that this lab requires you to code it to run locally. Later labs will have you adapting this code to deploy to MS Azure: Azure Functions and Cosmos DB.


## Lab Goals

The goals of this lab are to:

1. Set up a virtual environment and install Python packages
2. Write Python classes and methods 
3. Write and run unit tests for Python classes
4. Persist Python classes in a local document database (TinyDB) 
5. Manipulate JSON objects with the json library
6. Use external WebServices through the request library

The steps to accomplish all of these goals are listed below.

## 1. Getting Started

* Put the TreeHuggers folder (contained in this zip file) into your work area.
* Note that if you use OneDrive to work, you may run into problems due to network/synchronisation hiccups. I suggest to work on local HardDrive, and once you are finished, copy to OneDrive for archival or store in source control such as GitLab.
* Open the folder in your preferred IDE 

## 2. Virtual Environment

A *Virtual Environment* is a folder where you have a link to a particular python version and hold python packages a project uses

* Very useful to be able to work on projects that use different Python versions, different packages and versions. Without this, you have to install everything globally and risk messing up
* If you are taking MLT, you will see these too
* Read the following:
  * [Python guidance on venv](https://docs.python.org/3.13/library/venv.html) up to section "How venv work"
  * [Guidance on setting up venv in terminal and vs code](https://www.dataquest.io/blog/a-complete-guide-to-python-virtual-environments/) 

## 3. Activity 0.1 - Virtual Environment

It's up to you whether you wish to use the command line or an IDE to setup your virtual environment.

You can use the terminal create a virtual environment with Python 3.13 in the `TreeHuggers` folder supplied with the lab materials. Activate it.

* You may use whatever name you like for the environment

If you use VS Code, open the `TreeHuggers` folder supplied with the lab materials and configure an environment with the appropriate Python version

* VS Code uses the folder name as name for the environment
* VS Code makes it difficult to know if the environment is active. You may need to create a new terminal so it is activated. You should see a message like the below 

Note, you can use other IDEs such as JetBrains PyCharm. We mention VS Code as this has excellent integration with Azure.

## 4. Activity 0.2 - Pip and package installs

Pip is a Python package manager, to install libraries. When you create a venv, pip is automatically installed

* Read this [this page](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/) from section "Prepare pip" until the end 

Install in your virtual environment the following packages

* `requests`
* `tinydb`

You can do the installs through `pip install request` and `pip install tinydb`

The command `pip list` shows packages installed in the active environment. You should see `requests` and `tinydb` in the list

The example has the environment in a *.venv folder*, you probably chose a different place in a previous step

If you don't see the packages, it might be

* Installation failed
* You have not activated the virtual environment, or are in another one (is easy to mixup in VSCode if you have several Python installations and several virtual environments)

## 5. Treehuggers

The example application used in this lab and later labs is Treehuggers. This is a social network where users:

* Add trees 
* Attach stories to their tree friends
* Find similar trees around the world

### Database Scheme

The database for Treehuggers consists of three main tables:

* **User**
  * Username
* **Tree**
  * ID-tree
  * Coordinates
  * Address
  * Species
* **Story**
  * ID-story
  * ID-user
  * Id-tree
  * Text

In our prototype explored in this lab, we will use TinyDB to implement this as sets of JSON documents

## 5.1 Activity 0.3

Open the files User.py, Tree.Py, Story.py and inspect them in order. No need to change anything yet, or read the external resources linked in them, we'll get to that.

Take note of:

* How Class methods and class variables are used
* The ProxyObjects that interface with a TinyDb database and how they are used

## 5.2 Activities 1 and 2

Complete the *is_valid* method in Class *Tree* to raise an appropriate *ValueError* exception when:

1. Attribute *species* is an empty string, or not a String
2.  *coordinates* is not a tuple of size 2, or if it is,  
    1. the first element is not in the valid ranges of latitude [-90,90] or 
    2. the second element is not in the valid ranges of longitude [-180,180]

## 5.3 Activity 3

In the *add_tree* method of *Tree* class, use a *try... except* block to catch the *ValueError* of an empty string *species* attribute of Activity 2, set the *species* attribute to "unknown" and insert the tree. 

* Link to Python documentation on [exception handling](https://docs.python.org/3.13/tutorial/errors.html)


## 5.4 Activity 4

Open the test files (begin with *test_py*)

Read the [python unittest documentation](https://docs.python.org/3.13/library/unittest.html) up to "Organizing test code", ensure you know how to run tests from the terminal

If you use VSCode, after you understand how the terminal works, you may investigate how to [configure VSCode to run them](https://code.visualstudio.com/docs/python/testing). We will be running on the terminal in the rst of the lab though. 

Inspect the tests in the files and take note of:

* How mock objects are created
* What assertions are tested for each method   
* Run tests with the python -m command
  * Ensure you run on the active virtual environment

Go to `test_tree.py` and write unit tests for validation of species and validation of coordinates of the *is_valid()* method you wrote in Activities 1 and 2.

## 5.5 Activity 5

Go back to *Tree* class and implement method *get_address*

* Read all the requests library [quickstart](https://requests.readthedocs.io/en/latest/user/quickstart/)
* Read [json decoder/encoder](https://docs.python.org/3.13/library/json.html) manual up to "basic usage"
* Read the API of [nominatim's reverse geocoder](https://nominatim.org/release-docs/develop/api/Reverse/)  service and use it to get the address of this tree from its coordinates.
  * You should use the requests library to construct the http request, the *address* attribute must be set to the *display_name* field of the JSON response
  * You may assume the tree is valid.

## 5.6 Activity 6

Read tinydb's documentation about [basic usage](https://tinydb.readthedocs.io/en/latest/getting-started.html) and [queries](https://tinydb.readthedocs.io/en/latest/usage.html)

Inspect the *huggerboard* method to understand how to use the ProxyObject to query the story_collection

Implement the *best_friend* method as described in the code comments

## 5.7 Additional Activities

If you want to try some additional coding activities:

1. Write a unit test for the *delete_tree* method case where the tree to delete exists (successful deletion)
2. Refactor the *best_friend* method to, in case of many users having the same number of stories attached to a tree, return a JSON list instead of any of them. 
   1. Write a unittest for that case.
3. Refactor *get_address* to raise an exception if no address is returned. You may try coordinates (0,0), in the middle of the ocean, to see what to expect as output in this case.
4. Create a method *get_coordinates* in Class Tree, that uses nominatim's [lookup method ](https://nominatim.org/release-docs/develop/api/Lookup/) to take a Tree's address and update the coordinates.
5. Complete the *is_valid* function in the Class User to check a username is valid before it is inserted.
    1. Write a unit test to check this is working
    2. Call the *is_valid* in the *add_user* function and handle any exception appropriately