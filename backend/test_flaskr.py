import os
from re import I
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy
from sqlalchemy.orm.query import Query
from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://ewan@{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)
        self.engine = sqlalchemy.create_engine(self.database_path)
        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
            self.drop_data()
            self.populate_data()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    # ------------------------------------------------------------------
    # get categories
    # ------------------------------------------------------------------
    def test_get_all_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)
        expected = Category.query.all()
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(data['categories']), len(expected))
        self.assertTrue(data['success'])
    
    def test_get_empty_categories(self):
        res = self.client().get('/categories/6/questions')
        self.assertEqual(res.status_code, 404)

    def test_get_category_does_not_exist(self):
        res = self.client().get('/categories/100/questions')
        self.assertEqual(res.status_code, 404)
    # ------------------------------------------------------------------
    # get all questions for '/questions' 'GET'
    # ------------------------------------------------------------------
    def test_get_all_questions_and_paginate(self):
        expected = Question.query.all()
        epected_length = 10 if len(expected) >= 10 else len(expected)
        res = self.client().get('/questions')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['total_questions'], epected_length)
        self.assertTrue(data['success'])

    def test_get_all_questions_wit_empty_database(self):
        self.drop_data()
        res = self.client().get('/questions')
        self.assertEqual(res.status_code, 404)

    # ------------------------------------------------------------------
    # search
    # ------------------------------------------------------------------
    def test_search_case_insensitive(self):
        res1 = self.client().post('questions', json={'searchTerm': 'q'})
        data1 = json.loads(res1.data)

        res2 = self.client().post('questions', json={'searchTerm': 'Q'})
        data2 = json.loads(res2.data)

        isSame = True
        for d1 in data1['questions']:
            self.assertTrue(d1 in data2['questions'])

    def test_data_not_found(self):
        res = self.client().post('questions', json={'searchTerm': 'k'})
        self.assertEqual(res.status_code, 404)

    # ------------------------------------------------------------------
    # post new question
    # ------------------------------------------------------------------
    def test_post_new_question_to_cat1(self):
        self.drop_data()
        res = self.client().post('/questions', json={'question': 'q1', 
                                                    'answer': 'a1',
                                                    'difficulty': 1,
                                                    'category': 1})
        cat1_query = Question.query.filter_by(category=1).all()
        self.assertEqual(len(cat1_query), 1)
        self.assertEqual(cat1_query[0].question, 'q1')
        self.assertEqual(cat1_query[0].answer, 'a1')
        self.assertEqual(cat1_query[0].difficulty, 1)
        self.assertEqual(res.status_code, 200)
    
    def test_422_post_new_question_with_non_existent_category(self):
        self.drop_data()
        res = self.client().post('/questions', json={'question': 'q1', 
                                                    'answer': 'a1',
                                                    'difficulty': 1,
                                                    'category': 100})
        self.assertEqual(res.status_code, 422)

    def test_422_post_new_question_with_invalid_difficulty(self):
        res = self.client().post('/questions', json={'question': 'q1', 
                                                    'answer': 'a1',
                                                    'difficulty': 100,
                                                    'category': 1})
        self.assertEqual(res.status_code, 422)
        data = json.loads(res.data)
        self.assertFalse(data['success'])

    # ------------------------------------------------------------------
    # delete functions
    # ------------------------------------------------------------------
    def test_200_delete_complete(self):
        questions_before = Question.query.all()
        res = self.client().delete('/questions/1')
        data = json.loads(res.data)
        questions_after = Question.query.all()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(questions_before) - len(questions_after), 1)
        self.assertEqual(data.get('deleted'), 1)
        self.assertTrue(data.get('success'))

    def test_422_deleting_question_not_found(self):
        res = self.client().delete('/questions/20000')
        self.assertEqual(res.status_code, 422)
        data = json.loads(res.data)
        self.assertFalse(data['success'])

    # ------------------------------------------------------------------
    # quizzes post functions
    # ------------------------------------------------------------------
    def test_200_post_category_1_quizzes(self):
        previous_questions = [1,2,3,4]
        # force it to return the #5 question
        res = self.client().post('/quizzes', json={'previous_questions': previous_questions,
                                                    'quiz_category': {'type': 'Science', 'id': 1}})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['question']['id'], 5)

    def test_post_all_category_quizzes(self):
        questions = Question.query.all()
        previous_questions = []
        for i in range(len(questions)):
            res = self.client().post('/quizzes', json={'previous_questions': previous_questions,
                                                        'quiz_category': {'type': '', 'id': 0}})
            data = json.loads(res.data)
            self.assertTrue(data['success'])
            self.assertEqual(res.status_code, 200)
            self.assertTrue(data['question']['id'] not in previous_questions)
            previous_questions.append(data['question']['id'])
        
        # when len(previos_questions) == len(all_questions), return None
        res = self.client().post('/quizzes', json={'previous_questions': previous_questions,
                                                        'quiz_category': {'type': '', 'id': 0}})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['question'] is None)

    def test_422_string_previous_questions(self):
        previous_questions = ['a' + str(i) for i in range(10)]
        res = self.client().post('/quizzes', json={'previous_questions': previous_questions,
                                                        'quiz_category': {'type': '', 'id': 0}})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])

    def test_422_input_insufficient_query(self):
        res = self.client().post('/quizzes', json={'previous_questions': []})
        self.assertEqual(res.status_code, 422)
    # ----------------------------------------------------  --------------
    # helper functions
    # ------------------------------------------------------------------
    def populate_data(self):
        questions = [
            Question(question="q0101", answer="a1", category=1, difficulty=1),
            Question(question="q0102", answer="a1", category=1, difficulty=2),
            Question(question="q0103", answer="a1", category=1, difficulty=3),
            Question(question="q0104", answer="a1", category=1, difficulty=4),
            Question(question="q0105", answer="a1", category=1, difficulty=5),
            Question(question="q0201", answer="a1", category=2, difficulty=1),
            Question(question="q0202", answer="a1", category=2, difficulty=2),
            Question(question="q0203", answer="a1", category=2, difficulty=3),
            Question(question="q0301", answer="a1", category=3, difficulty=3),
            Question(question="q0401", answer="a1", category=4, difficulty=1),
            Question(question="q0501", answer="a1", category=5, difficulty=1),
            Question(question="q0502", answer="a1", category=5, difficulty=1),
            Question(question="q0503", answer="a1", category=5, difficulty=1)
        ]
        for i, q in enumerate(questions):
            q.id = i + 1
            q.insert()
    
    def drop_data(self):
        Question.query.delete()
# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()