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
        self.DB_HOST = os.getenv('DB_HOST', '127.0.0.1:5432')  
        self.DB_USER = os.getenv('DB_USER', 'postgres')  
        self.DB_PASSWORD = os.getenv('DB_PASSWORD', '1234')  
        self.DB_NAME = os.getenv('DB_NAME', 'trivia')  
        self.DB_PATH = 'postgresql+psycopg2://{}:{}@{}/{}'.format(self.DB_USER, self.DB_PASSWORD, self.DB_HOST, self.DB_NAME)
        #name of database 
        #self.database_name = "trivia"
        #you should change passowed if have  databasse password
        #self.database_path = "postgresql://postgres:1234@{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.DB_PATH)
        self.new_q = {
            'question': 'what is my favorite day ?',
             'answer': 'Mother day',
              'difficulty': 1, 
              'category' : 5
        }
        self.data_quiz={
            'previous_questions' : [4,10], 'quiz_category': {'type': 'Art', 'id':'2'}
        }
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

    def test_get_paginated_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        
        
    '''def test_404_sent_req_beyond_invalid_page(self):
        res =self.client().get('/questions?page=100')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'],'Resource Not Found')
    '''    
    #categories 
    def test_get_paginated_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        
    


    #--------------------------
    #delete 
    

    def test_error_404_if_questions_not_found(self):
        res = self.client().delete('/questions/1000')
        data = json.loads(res.data) 
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'],'Resource Not Found')
        
    #---------------
    
    def test_create_new_question(self):
        res = self.client().post('/questions',json=self.new_q)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        

    def test_error_422_in_create_new_question_request_falid(self):
        res = self.client().post('/questions',json={})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        

#search 
#-------------------------------
    def test_search_question(self):
        res = self.client().post('/questions',json={'searchTerm' : 'what'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        
        


    def test_error_404_search_question_not_found(self):
        res = self.client().post('/questions',json={'searchTerm' : 'salamabcdifc'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        

#----------------------------------------
        
 #game quizz
    def test_game_the_quiz(self):
        res = self.client().post('/quizzes',json= self.data_quiz)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        
       

    def test_error_400_game_the_quiz(self):
        res = self.client().post('/quizzes')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        
        self.assertEqual(data['message'],'Bad request')
#---------------------------------------------


    

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()