import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    #@app for qu

    def test_get_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['questions']),10)
        self.assertTrue(data['total_questions'])
        self.assertEqual(len(data['categories']), 6)
    #categories 
    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])
        self.assertEqual(len(data['categories']), 6) 
    
    #delete 
    def test_delete_questions(self):
        res = self.client().delete('/questions/14')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_error_422_delete_questions(self):
        res = self.client().delete('/questions/10000')
        data = json.loads(res.data) 
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)

    def test_adding_question(self):
        res = self.client().post('/questions',json={'question': 'what is my age?', 'answer': '21', 'difficulty': 4, 'category' : 4})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 201)
        self.assertEqual(data['success'], True)

    def test_error_422_adding_question(self):
        res = self.client().post('/questions',json={'question': '', 'answer': '21', 'difficulty':4, 'category' : 4})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)

#search 
    def test_search_question(self):
        res = self.client().post('/questions/search',json={'searchTerm' : 's'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertEqual(len(data['questions']),10)
        self.assertEqual(len(data['categories']), 6)


    def test_error_404_search_question(self):
        res = self.client().post('/questions/search',json={'searchTerm' : 'abcdefghijklmn'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)



        
 #game quizz
    def test_game_the_quiz(self):
        res = self.client().post('/quizzes',json={'previous_questions' : [4,18], 'quiz_category': {'type': 'Science', 'id':'1'}})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])

    def test_error_400_game_the_quiz(self):
        res = self.client().post('/quizzes',json={})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)

    def test_questions_besed_category(self):
        res = self.client().get('/categories/7/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])
        self.assertEqual(data['current_category'],'Sports')
    def test_error_422_questions_besed_category(self):
        res = self.client().get('/categories/18749/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()