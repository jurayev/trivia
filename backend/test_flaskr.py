import unittest
from parameterized import parameterized
import json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import database_exists, create_database

from flaskr import create_app, QUESTIONS_PER_PAGE, BAD_REQUEST, NOT_FOUND, INTERNAL_SERVER_ERROR, UNPROCESSABLE_ENTITY
from models import setup_db, Question, Category
import functools


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.user = "postgres"
        self.passwd = "postgres"
        self.host = "localhost:5432"
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}:{}@{}/{}".format(self.user, self.passwd, self.host, self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)

            # create all tables
            if not database_exists(self.database_path):
                create_database(self.database_path)

    def tearDown(self):
        """Executed after reach test"""
        pass

    def log(func):
        @functools.wraps(func)
        def wrapper(*args):
            splitted_test_name = func.__name__.split("_")
            test_name = " ".join(splitted_test_name)

            if len(args) > 1:
                case_name = args[1]
                print("-"*10, f"{test_name} {case_name}", "-"*10)
            else:
                print("-"*10, test_name, "-"*10)
            func(*args)
            print("-"*10, "PASSED", "-"*10, "\n")

        return wrapper

    # TESTS

    @log
    def test_get_categories(self):
        response = self.client().get("/categories")
        data = json.loads(response.data)
        categories_count = Category.query.count()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data["categories"]), categories_count)
        self.assertTrue(data["success"])

    @parameterized.expand([
        ("first page", ""),
        ("second page", "?page=2")
    ])
    @log
    def test_get_questions(self, name, query_parameter):
        response = self.client().get(f"/questions{query_parameter}")
        data = json.loads(response.data)

        questions_count = Question.query.count()
        categories_count = Category.query.count()

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data["success"])
        self.assertEqual(len(data["questions"]), QUESTIONS_PER_PAGE)
        self.assertEqual(data["total_questions"], questions_count)
        self.assertEqual(len(data["categories"]), categories_count)
        self.assertFalse(data["current_category"])

    @parameterized.expand([
        ("404 if invalid page == -1", "-1", 422, UNPROCESSABLE_ENTITY),
        ("404 if invalid page == 0", "0", 422, UNPROCESSABLE_ENTITY),
        ("404 if beyond valid page", "10000", 404, NOT_FOUND)
    ])
    @log
    def test_get_questions_returns_error(self, name, query_parameter, error_code, error_message):
        response = self.client().get(f"/questions?page={query_parameter}")
        data = json.loads(response.data)

        self.assertEqual(response.status_code, error_code)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], error_message)

    @log
    def test_delete_question(self):
        question_id = 12
        response = self.client().delete(f"/questions/{question_id}")
        data = json.loads(response.data)
        question_in_db = Question.query.filter(Question.id == question_id).one_or_none()

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data["success"])
        self.assertEqual(data["id"], question_id)
        self.assertFalse(question_in_db)

        # Rollback deleted question
        question = Question(id=question_id, question="Who invented Peanut Butter?",
                            answer="George Washington Carver", difficulty=2, category=4)
        question.insert()

    @log
    def test_delete_question_returns_404(self):
        question_id = 0
        response = self.client().delete(f"/questions/{question_id}")
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], NOT_FOUND)

    @log
    def test_post_question(self):
        payload = {"question": "test my difficult question",
                   "answer": "test",
                   "category": "2",
                   "difficulty": "4"
                   }
        response = self.client().post("/questions", json=payload)
        data = json.loads(response.data)
        question_in_db = Question.query.order_by(Question.id.desc()).first()

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data["success"])
        self.assertEqual(data["id"], question_in_db.id)

    @log
    def test_post_question_returns_400(self):
        payload = {"question": "test my difficult question",
                   "answer": "test",
                   "category": "2",
                   "difficulty": "4"
                   }
        response = self.client().post("/questions", content_type="application/json", data=payload)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], BAD_REQUEST)

    @log
    def test_post_question_returns_500(self):
        response = self.client().post("/questions", json={})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 500)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], INTERNAL_SERVER_ERROR)

    @parameterized.expand([
        ("normal_search", "title"),
        ("search with trailing spaces", "   Which   "),
        ("blank search term", " "),
        ("non existing search term", "abcdef 1234")
    ])
    @log
    def test_search_question(self, name, search_term):
        payload = {"searchTerm": search_term}
        response = self.client().post("/questions/search", json=payload)
        data = json.loads(response.data)

        filtered_questions_count = Question.query.filter(Question.question.ilike(f'%{search_term.strip()}%')).count()
        questions_count = Question.query.count()

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data["success"])
        self.assertEqual(len(data["questions"]), filtered_questions_count)
        self.assertEqual(data["total_questions"], questions_count)
        self.assertFalse(data["current_category"])

    @log
    def test_search_question_returns_400(self):
        payload = {"searchTerm": "title"}
        response = self.client().post("/questions/search", content_type="application/json", data=payload)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], BAD_REQUEST)

    @log
    def test_search_question_returns_500(self):
        response = self.client().post("/questions/search", json={})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 500)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], INTERNAL_SERVER_ERROR)

    @parameterized.expand([
        ("with id == 1", 1),
        ("with id == 6", 6)
    ])
    @log
    def test_get_questions_by_category(self, name, category_id):
        response = self.client().get(f"/categories/{category_id}/questions")
        data = json.loads(response.data)

        filtered_questions_count = Question.query.filter(Question.category == category_id).count()
        questions_count = Question.query.count()

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data["success"])
        self.assertEqual(len(data["questions"]), filtered_questions_count)
        self.assertEqual(data["total_questions"], questions_count)
        self.assertFalse(data["current_category"])

    @parameterized.expand([
        ("404 if category id == -1", -1, 404, NOT_FOUND),
        ("422 if category id == 0", 0, 422, UNPROCESSABLE_ENTITY),
        ("404 if category id == 10000", 1000, 404, NOT_FOUND)
    ])
    @log
    def test_get_questions_by_category_returns_error(self, name, category_id, error_code, error_message):
        response = self.client().get(f"/categories/{category_id}/questions")
        data = json.loads(response.data)

        self.assertEqual(response.status_code, error_code)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], error_message)

    @parameterized.expand([
        ("case 1", [2, 4, 7], 5),
        ("case 2", [12, 21, 19], 4)
    ])
    @log
    def test_get_questions_for_quiz(self, name, prev_questions, category_id):
        payload = {
            "previous_questions": prev_questions,
            "quiz_category": {"id": category_id}
        }
        response = self.client().post("/quizzes", json=payload)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data["success"])
        self.assertTrue(data["question"]["id"] not in prev_questions)
        self.assertEqual(data["question"]["category"], category_id)

    @log
    def test_get_questions_for_quiz_when_ALL_category(self):
        category_id = 0
        payload = {
            "previous_questions": [],
            "quiz_category": {"id": category_id}
        }
        response = self.client().post("/quizzes", json=payload)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data["success"])
        self.assertTrue(data["question"])
        self.assertNotEqual(data["question"]["category"], category_id)

    @log
    def test_get_questions_for_quiz_when_no_new_ones_left(self):
        payload = {
            "previous_questions": [2, 4, 6],
            "quiz_category": {"id": 5}
        }
        response = self.client().post("/quizzes", json=payload)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data["success"])
        self.assertFalse(data["question"])

    @parameterized.expand([
        ("422 if category id == -1", -1, 422, UNPROCESSABLE_ENTITY),
        ("404 if category id == 10000", 1000, 404, NOT_FOUND)
    ])
    @log
    def test_get_questions_for_quiz_returns_error(self, name, category_id, error_code, error_message):
        payload = {
            "previous_questions": [2, 4, 7],
            "quiz_category": {"id": category_id}
        }
        response = self.client().post("/quizzes", json=payload)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, error_code)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], error_message)

    @log
    def test_get_questions_for_quiz_returns_error_400_if_invalid_payload(self):
        payload = {
            "previous_questions": [2, 4, 7],
            "quiz_category": {"id": "1"}
        }
        response = self.client().post("/quizzes", content_type="application/json", data=payload)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], BAD_REQUEST)

    @log
    def test_get_questions_for_quiz_returns_error_400_if_empty_payload(self):
        response = self.client().post("/quizzes", json={})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], BAD_REQUEST)


if __name__ == "__main__":
    unittest.main()
