import unittest

from app import app



class TestEcommerceApp(unittest.TestCase):

    def setUp(self):

        app.testing = True

        self.app = app.test_client()



    def tearDown(self):

        pass



    def test_home_route(self):

        response = self.app.get('/')

        self.assertEqual(response.status_code, 200)



    def test_login_route(self):

        response = self.app.get('/login')

        self.assertEqual(response.status_code, 200)





if __name__ == '__main__':

    unittest.main()
