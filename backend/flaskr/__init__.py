import os
from flask import Flask, json, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
from sqlalchemy.orm import query

from sqlalchemy.orm.query import Query

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
      response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
      response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,PUT,OPTIONS')
      return response
  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  def parse_categories(category_objects):
    categories = {c.id: c.type for c in category_objects}
    return categories

  @app.route('/categories', methods=['GET'])
  def get_categories():
    category_objects = Category.query.all()
    if len(category_objects) == 0:
      abort(404)

    categories = parse_categories(category_objects)
    # print(categories)
    return jsonify({
      'success': True,
      'categories': categories
    })
  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''

  def paginate(page, questions):
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = page * QUESTIONS_PER_PAGE

    return [ q.format() for q in questions[start:end]]

  @app.route('/questions')
  def get_questions():
    page = request.args.get('page', 1, int)
    print("page: ", page)
    question_objects = Question.query.all()
    questions = paginate(page, question_objects)
    
    category_objects = Category.query.all()
    if len(category_objects) == 0:
      abort(404)

    return jsonify({
      'success': True,
      'questions': questions,
      'total_questions': len(questions),
      'categories': parse_categories(category_objects),
      'currentCategory': None
    })
  
  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
    try:
      question = Question.query.get(question_id)
      if question is None:
        abort(404)
      else:
        question.delete()
        return jsonify({
          'success': True,
          'deleted': question_id
        })
    except Exception as e:
      print(e)
      abort(422)

  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  @app.route('/questions', methods=['POST'])
  def add_or_search_question():
    data = request.get_json()
    print(data)
    page = request.args.get('page', 1, int)
    # add_question
    if not data.get('searchTerm'):
      try:
        new_question = Question(question=data['question'],
                                answer=data['answer'],
                                difficulty=data['difficulty'],
                                category=data['category'])
        new_question.insert()
        return jsonify({
          'success': True
        })
      except Exception as e:
        print(e)
        abort(422)
    # search
    else:
      term = data.get('searchTerm')
      questions = Question.query.filter(Question.question.ilike(f'%{term}%')).all()
      if len(questions)  == 0:
        abort(404)
      return jsonify({
        'success': True,
        'questions': paginate(page, questions),
        'total_questions': len(questions)
      })
  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''

  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/categories/<int:category_id>/questions', methods=['GET'])
  def get_questions_by_category_id(category_id):
    questions = Question.query.filter_by(category=category_id).all()
    if len(questions) == 0:
      abort(404)
    page = request.args.get('page', 1, int)
    return jsonify({
      'success': True,
      'questions': paginate(page, questions),
      'total_questions': len(questions),
      'current_category': category_id
    })
  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
  @app.route('/quizzes', methods=['POST'])
  def get_question_for_play():
    data = request.get_json()
    previous_questions = data.get('previous_questions')
    quiz_category = data.get('quiz_category')
    print(previous_questions, quiz_category)

    if quiz_category['id'] == 0: # ALL categories
      questions = Question.query.filter(Question.id.notin_(previous_questions)).all()
    else:    
      questions = Question.query.filter(Question.id.notin_(previous_questions)) \
                                  .filter_by(category=quiz_category['id']) \
                                  .all()

    return jsonify({
      'success': True,
      'question': questions[random.randint(0, len(questions) - 1)].format() \
                  if len(questions) != 0 else None
    })
  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  
  return app

    