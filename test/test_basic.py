import unittest

from portfolio import app


class BasicTesting(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.app.config['SECRET_KEY'] = 'sekrit!'
        self.client = self.app.test_client()
        self._ctx = self.app.test_request_context()
        self.app.config['WTF_CSRF_ENABLED'] = False
        self._ctx.push()

    def tearDown(self):
        pass

    def test_homepage(self):
        resp = self.client.get('/')
        self.assertTrue(resp.status_code, 200)
        self.assertIn(b"PC Gamer", resp.data)

    def test_projects(self):
        resp = self.client.get('/projects')
        self.assertTrue(resp.status_code, 200)
        self.assertIn(b"Sites might have sensitive data", resp.data)

    def test_portfolio(self):
        resp = self.client.get('/portfolio')
        self.assertTrue(resp.status_code, 200)
        self.assertIn(b"Work History", resp.data)

    def test_login(self):
        resp = self.client.post('/admin/login', data=dict(
                username='username',
                password='password',
        ), follow_redirects=True, content_type='application/x-www-form-urlencoded')

        self.assertTrue(resp.status_code, 200)
        self.assertIn(b'Add Post', resp.data)

    def test_invalid_login(self):
        resp = self.client.post('/admin/login', data=dict(
                username='invalid',
                password='invalid',
        ), follow_redirects=True, content_type='application/x-www-form-urlencoded')

        self.assertTrue(resp.status_code, 200)
        self.assertIn(b'Wrong Username or Password', resp.data)

    def test_logout(self):
        resp = self.client.get('/logout', follow_redirects=True)

        self.assertTrue(resp.status_code, 200)
        self.assertIn(b"I play well with others", resp.data)

    def test_save_post(self):
        with self.client as c:
            with c.session_transaction() as sess:
                sess['logged_in'] = True
            resp = c.get('/admin/add_post')
            self.assertIn(b'Title', resp.data)
        # self.assertEqual('with session', resp.data)


if __name__ == '__main__':
    unittest.main()
