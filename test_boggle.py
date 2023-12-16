from unittest import TestCase
from app import app
from flask import session

class BoggleAppTests(TestCase):

    def setUp(self):

        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_home(self):

        with self.client:
            response = self.client.get('/')
            self.assertIn('board', session)
            self.assertEqual(session.get('high_score'), 0)
            self.assertEqual(session.get('num_try'), 1)
            self.assertIn(b'<title> Boggle </title>', response.data)
            self.assertIn(b'<input class="input_guess" type="text" placeholder="Your Guess" name="input_guess" autofocus>', response.data)

    def test_word_exit(self):

        with self.client as client:
            with client.session_transaction() as s:
                s['board'] = [["B", "O", "A", "R", "D"],
                              ["W", "O", "R", "D", "S"],
                              ["S", "E", "T", "U", "P"],
                              ["G", "U", "E", "S", "S"],
                              ["T", "E", "S", "T", "S"]]
        response = self.client.get('/guess?input_guess=guess')
        self.assertEqual(response.json['result'], 'ok')

    def test_word_not(self):

        self.client.get('/')
        response = self.client.get('/guess?input_guess=springboard')
        self.assertEqual(response.json['result'], 'not-on-board')

    def test_non_word(self):

        self.client.get('/')
        response = self.client.get('/guess?input_guess=abcdefghijklmnopqrstuvwxyz')
        self.assertEqual(response.json['result'], 'not-word')