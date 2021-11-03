import os
from flask import Flask, json, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
from sqlalchemy.orm import query

from sqlalchemy.orm.query import Query
from sqlalchemy.sql.expression import false

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add(
            'Access-Control-Allow-Headers',
            'Content-Type,Authorization,true')
        response.headers.add(
            'Access-Control-Allow-Methods',
            'GET,PATCH,POST,DELETE,PUT,OPTIONS')
        return response

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


    def paginate(page, questions):
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = page * QUESTIONS_PER_PAGE

        return [q.format() for q in questions[start:end]]

    @app.route('/questions')
    def get_questions():
        page = request.args.get('page', 1, int)
        print("page: ", page)
        question_objects = Question.query.all()
        if len(question_objects) == 0:
            abort(404)

        questions = paginate(page, question_objects)
        category_objects = Category.query.all()

        return jsonify({
            'success': True,
            'questions': questions,
            'total_questions': len(question_objects),
            'categories': parse_categories(category_objects),
        })

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.get(question_id)
            question.delete()
            return jsonify({
                'success': True,
                'deleted': question_id
            })
        except Exception as e:
            print(e)
            abort(422)

    @app.route('/questions', methods=['POST'])
    def add_or_search_question():
        data = request.get_json()
        print(data)
        page = request.args.get('page', 1, int)
        # add_question
        if not data.get('searchTerm'):

            try:
                if data['difficulty'] > 5 or data['difficulty'] < 1:
                    abort(422)
                new_question = Question(question=data['question'],
                                        answer=data['answer'],
                                        difficulty=data['difficulty'],
                                        category=data['category'])
                new_question.insert()
                return jsonify({
                    'success': True,
                    'question': new_question.format()
                })
            except Exception as e:
                print(e)
                abort(422)
        # search
        else:
            term = data.get('searchTerm')
            questions = Question.query.filter(
                Question.question.ilike(f'%{term}%')).all()
            if len(questions) == 0:
                abort(404)
            return jsonify({
                'success': True,
                'questions': paginate(page, questions),
                'total_questions': len(questions)
            })

    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def get_questions_by_category_id(category_id):
        questions = Question.query.filter_by(category=category_id).all()
        print(len(questions))
        if len(questions) == 0:
            abort(404)
        page = request.args.get('page', 1, int)
        return jsonify({
            'success': True,
            'questions': paginate(page, questions),
            'total_questions': len(questions),
            'current_category': category_id
        })

    @app.route('/quizzes', methods=['POST'])
    def get_question_for_play():
        data = request.get_json()
        try:
            previous_questions = data.get('previous_questions')
            quiz_category = data.get('quiz_category')
            print(previous_questions, quiz_category)

            if quiz_category['id'] == 0:  # ALL categories
                questions = Question.query.filter(
                    Question.id.notin_(previous_questions)).all()
            else:
                questions = Question.query.filter(
                    Question.id.notin_(previous_questions)) .filter_by(
                    category=quiz_category['id']) .all()

            return jsonify({'success': True, 'question': questions[random.randint(
                0, len(questions) - 1)].format() if len(questions) != 0 else None})
        except Exception as e:
            print(e)
            abort(422)


    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'Data not found'
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'unprocessable'
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'Bad request'
        }), 400

    return app

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({
            'success': False,
            'error': 500,
            'message': 'Internal error'
        }), 500
