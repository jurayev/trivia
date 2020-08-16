# Trivia API

Provides API [endpoints](https://github.com/jurayev/trivia##Endpoints) for Trivia application.

All backend code base follows [PEP8 style guidelines.](https://www.python.org/dev/peps/pep-0008) and modern Python 3.7.

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### PIP Dependencies

Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)
Once you have your virtual environment setup and running, install dependencies by navigating to the `/backend` directory and running:

```
pip3 install -r requirements.txt
```

This will install all of the required packages within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM used handle postgres database.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension used to handle cross origin requests from a frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Endpoints
* [GET "/categories"](https://github.com/jurayev/trivia####GET "/categories")
* [GET "/categories/int:id/questions"](https://github.com/jurayev/trivia####GET "/categories/int:id/questions")
* [GET "/questions"](https://github.com/jurayev/trivia####GET "/questions")
* [POST "/questions"](https://github.com/jurayev/trivia####POST "/questions")
* [POST "/questions/search"](https://github.com/jurayev/trivia####POST "/questions/search")
* [POST "/quizzes"](https://github.com/jurayev/trivia####POST "/quizzes")
* [DELETE "/questions/int:id"](https://github.com/jurayev/trivia####DELETE "/questions/int:id")


#### GET "/categories"
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding name of the category.
- Request Arguments: None.
- Returns: An object with categories, that contains the key=id, value=name pairs. 
```
REQUEST

curl -X GET http://<host>:<port>/categories
```
```
RESPONSE
{ 
  "success": True
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }
}
```

#### GET "/categories/int:id/questions"
- Fetches a list of questions for a given category id.
- Request Arguments: None.
- Returns: An object with the questions list, total questions number and current category. 
```
REQUEST

curl -X GET http://<host>:<port>/categories/<int:id>/questions
```
```
RESPONSE
{
  "current_category": null, 
  "questions": [
    {
      "answer": "Escher", 
      "category": 2, 
      "difficulty": 1, 
      "id": 16, 
      "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
    }, 
    {
      "answer": "test answer", 
      "category": 2, 
      "difficulty": 1, 
      "id": 25, 
      "question": "test question"
    },
    ...
  ], 
  "success": true, 
  "total_questions": 22
}
```

#### GET "/questions"
- Fetches a list of questions sorted by difficulty in ascending order and limits 10 questions per page.
- URL parameters: `page`. Example: `"/questions?page=1`, `"/questions?page=2` etc.
- Request Arguments: None.
- Returns: An object with the categories dictionary, questions list with 10 questions, total questions number and current category. 
```
REQUEST

curl -X GET http://<host>:<port>/questions?page=1
```
```
RESPONSE
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "current_category": null, 
  "questions": [
    {
      "answer": "Muhammad Ali", 
      "category": 4, 
      "difficulty": 1, 
      "id": 9, 
      "question": "What boxer's original name is Cassius Clay?"
    }, 
    {
      "answer": "Escher", 
      "category": 2, 
      "difficulty": 1, 
      "id": 16, 
      "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
    }, 
    {
      "answer": "", 
      "category": 1, 
      "difficulty": 1, 
      "id": 34, 
      "question": ""
    }, 
    ...
  ], 
  "success": true, 
  "total_questions": 22
}
```

#### POST "/questions"
- Adds a new question to the questions list. Question text, Answer text, Category id and Difficulty rate must be provided.
- Request Arguments: `question, answer, category, difficulty`.
- Returns: An object with a new question id. 
```
REQUEST

curl -X POST -H "Content-Type: application/json" -d '{"question":"What boxers original name is Cassius Clay?", "answer":"Muhammad Ali", "difficulty":1, "category":"4"}' http://<host>:<port>/questions
```
```
RESPONSE
{
  "id": 36, 
  "success": true
}
```

#### POST "/questions/search"
- Fetches all questions that match a given search term, case-insensitive.
- Request Arguments: `searchTerm`.
- Returns: An object with the questions list, total questions number and current category.  
```
REQUEST

curl -X POST -H "Content-Type: application/json" -d '{"searchTerm": "title"}' http://<host>:<port>/questions/search
```
```
RESPONSE
{
  "current_category": null, 
  "questions": [
    {
      "answer": "Maya Angelou", 
      "category": 4, 
      "difficulty": 2, 
      "id": 5, 
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    }, 
    {
      "answer": "Edward Scissorhands", 
      "category": 5, 
      "difficulty": 3, 
      "id": 6, 
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }
  ], 
  "success": true, 
  "total_questions": 24
}
```

#### POST "/quizzes"
- Fetches the next question for a quiz. The question is selected based on category id and must be not in the list of previous questions.
- Request Arguments: `prev_questions, quiz_category`.
- Returns: An object with the next question for the quiz. 
```
REQUEST
curl -X POST -H "Content-Type: application/json" -d '{"previous_questions": [30], "quiz_category": {"type": "Art", "id": "2"}' http://<host>:<port>/quizzes
```
```
RESPONSE
{
  "question": {
    "answer": "One", 
    "category": 2, 
    "difficulty": 4, 
    "id": 18, 
    "question": "How many paintings did Van Gogh sell in his lifetime?"
  }, 
  "success": true
}
```

#### DELETE "/questions/int:id"
- Deletes a question with a given id.
- Request Arguments: None.
- Returns: An object with the deleted question id. 
```
REQUEST
curl -X DELETE http://<host>:<port>/questions/25
```
```
RESPONSE
{
  "id": 25, 
  "success": true
}
```

## Status codes
```
200 - OK                    | Everything worked as expected.
400 - BAD REQUEST           | The request was unacceptable, often due to missing a required parameter.
404 - NOT FOUND             | The requested resource doesn't exist.
422 - UNPROCESSABLE ENTITY  | The server understands the content type of the request entity, and the syntax of the request entity is correct, but it was unable to process the contained instructions.
500 - INTERNAL SERVER ERROR | Something went wrong on api's/database's end
```

## Testing
To run the tests
```
dropdb trivia_test && createdb trivia_test
psql trivia_test < trivia.psql
python3 test_flaskr.py
```
