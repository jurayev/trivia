from flask import Flask, request, abort, jsonify
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10
BAD_REQUEST = "Bad Request"
NOT_FOUND = "Not Found"
UNPROCESSABLE_ENTITY = "Unprocessable Entity"
INTERNAL_SERVER_ERROR = "Internal Server Error"


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app, resources={r"/categories|questions|quizzes/*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,POST,DELETE,OPTIONS')
        return response

    def get_serialized_categories():
        try:
            categories = Category.query.order_by(Category.id).all()
            serialized_categories = {c.id: c.type for c in categories}
            return serialized_categories
        except:
            abort(500)

    def get_questions_per_page(page):
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE
        questions = Question.query.order_by(Question.difficulty).all()
        serialized_questions = [q.format() for q in questions]
        return serialized_questions[start:end]

    @app.route("/categories", methods=["GET"])
    def get_categories():
        return jsonify({
            "success": True,
            "categories": get_serialized_categories()
        })

    @app.route("/questions", methods=["GET"])
    def get_questions():
        try:
            page = request.args.get('page', 1, type=int)
        except:
            abort(400)

        if page < 1:
            abort(422)

        questions = get_questions_per_page(page)
        if not questions:
            abort(404)

        try:
            return jsonify({
                "success": True,
                "questions": questions,
                "total_questions": Question.query.count(),
                "categories": get_serialized_categories(),
                "current_category": None
            })
        except:
            abort(500)

    @app.route("/questions/<int:id>", methods=["DELETE"])
    def delete_question(id):
        question = Question.query.filter(Question.id == id).first_or_404()
        try:
            question.delete()
        except:
            abort(500)

        return jsonify({
            "success": True,
            "id": id
        })

    @app.route("/questions", methods=["POST"])
    def post_question():
        try:
            data = request.get_json()
        except:
            abort(400)

        try:
            new_question = Question(question=data["question"],
                                    answer=data["answer"],
                                    category=data["category"],
                                    difficulty=data["difficulty"])
            new_question.insert()
        except:
            abort(500)

        return jsonify({
            "success": True,
            "id": new_question.id
        })

    @app.route("/questions/search", methods=["POST"])
    def search_question():
        try:
            data = request.get_json()
        except:
            abort(400)

        try:
            search_term = data['searchTerm'].strip()
            questions = Question.query.filter(Question.question.ilike(f"%{search_term}%")).all()
            serialized_questions = [q.format() for q in questions]
            total_questions = Question.query.count()
        except:
            abort(500)

        return jsonify({
            "success": True,
            "questions": serialized_questions,
            "total_questions": total_questions,
            "current_category": None
        })

    @app.route("/categories/<int:id>/questions", methods=["GET"])
    def get_questions_by_category(id):
        if id < 1:
            abort(422)
        try:
            questions = Question.query.filter(Question.category == id).order_by(Question.difficulty.asc()).all()
            serialized_questions = [q.format() for q in questions]
            total_questions = Question.query.count()
        except:
            abort(500)

        if not serialized_questions:
            abort(404)

        return jsonify({
            "success": True,
            "questions": serialized_questions,
            "total_questions": total_questions,
            "current_category": None
        })

    @app.route("/quizzes", methods=["POST"])
    def get_questions_for_quiz():
        try:
            data = request.get_json()
            category_id = data["quiz_category"]["id"]
            prev_questions = data["previous_questions"]
        except:
            abort(400)

        if int(category_id) < 0:
            abort(422)

        try:
            if int(category_id) == 0:
                questions_by_category = Question.query.all()
            else:
                questions_by_category = Question.query.filter(Question.category == category_id).all()
        except:
            abort(500)

        if not questions_by_category:
            abort(404)

        unique_questions = [q.format() for q in questions_by_category if q.id not in prev_questions]

        return jsonify({
            "success": True,
            "question": random.choice(unique_questions) if unique_questions else None
        })

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": BAD_REQUEST
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": NOT_FOUND
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": UNPROCESSABLE_ENTITY
        }), 422

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": INTERNAL_SERVER_ERROR
        }), 500

    return app
