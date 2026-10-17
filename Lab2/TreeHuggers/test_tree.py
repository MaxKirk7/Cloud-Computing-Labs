import unittest
from Tree import Tree

#Read this page on Python's unittest how https://docs.python.org/3.10/library/unittest.html up to section Class Methods
# In section ClassMethods, focus on the setUp() tearDown() and the assert* methods 
class TestTreeMethods(unittest.TestCase):   

    # A valid tree  
    tree_1 = Tree(ident=100,
        coordinates=(50.93304715,-1.3900633),address="85, Upper Shaftesbury Avenue, Portswood, Southampton, England, SO17 3RU, United Kingdom", species = "Bamboo Bamboozle")
    
    #invalid trees
    tree_2 = Tree(ident=150,
        coordinates=(513,513),
        address="Somewhere in the Cloud...", 
        species = "Bamboo Bambara")
    
    tree_3 = Tree(ident=180,
                  coordinates=(14,14),
                  address="Highfield",
                  species = "")


    # Empty the tree collection after each test
    def tearDown(self):
       Tree.tree_collection.truncate()

    #Activity 4: write unit tests for the correct, failed validation of species and failed validation of coordinates cases 
    # of the is_valid() method. For the failed validations, just check a ValueError exception is raised
    # Hint: https://www.pythonclear.com/unittest/python-unittest-assertraises/

    def test_is_valid_correct(self):
      #your code here
      pass
    
      
    def test_is_valid_species(self):
       #your code here
       pass
       
    def test_is_valid_coordinates(self):
       #your code here
       pass
     

    def test_add_tree_valid(self):
      Tree.add_tree(self.tree_1)
      # Assert result = expected
      self.assertEqual(len(Tree.tree_collection),1)

            
    def test_delete_tree_existent(self):
      # Additional activity 1: 
      # Write this unit test
      self.fail("TODO")

    def test_get_address(self):
      # May want to do this one to test your answer to Activity 5!
      self.fail("TODO")  
      
    

 
      

#Main to execute the tests
if __name__ == '__main__':
    unittest.main()

  
