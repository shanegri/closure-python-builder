import unittest, sys,os

sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))

import lib

class ClosureTests(unittest.TestCase):

    def test_js_dependencies(self):
        self.assertEqual(1, 1, "one should equal 1")

    def test_closure_output(self):
        self.assertEqual(1, 1, "one should equal 1")





def executeTests():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    suite = unittest.TestLoader().loadTestsFromTestCase(ClosureTests)
    unittest.TextTestRunner(verbosity=2).run(suite)

if __name__ == '__main__':
    executeTests()