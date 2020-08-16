# Full Stack Trivia Game

### Introduction

Trivia is a game where the players are asked about different facts, events, names, geography, science subjects. The game is aimed for anyone who loves playing quizzes, compete with other players, educate himself/herself in many fields and just for fun. 

### Overview

Main functionality of trivia game:

1) Display questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer. 
2) Delete questions.
3) Add questions and require that they include question and answer text.
4) Search for questions based on a text query string.
5) Play the quiz game, randomizing either all questions or within a specific category. 

### Tech Stack

* **SQLAlchemy ORM** to be ORM library of choice
* **PostgreSQL** as database of choice
* **Python 3.7** and **Flask** as server language and server framework
* **Flask-CORS** is the extension used to handle cross origin requests from a frontend server.
* **React-create-app** for website's frontend
* **Node.js** to support frontend server

### Main Files: Project Structure

  ```sh
  ├── README.md
  ├── LICENSE.md
  ├── backend
  |    ├── flaskr
  |        ├── __init__.py   *** the main driver of the app. Includes Flask Controllers and Endpoints
  |    ├── models.py         *** SQLAlchemy models   
  |    ├── requirements.txt  *** The dependencies we need to install
  |    ├── test_flaskr       *** The test for application
  |    ├── trivia.psql       *** DB dump file
  ├── frontend
  |    ├── public            *** the resources used for better UI/UX
  |    ├── src  
  |        ├── components    *** React components
  |        ├── stylesheets   *** CSS files
  |    ├── package-lock.json *** Config file
  |    ├── package.json      *** Config file and dependencies
  |    ├── README.md
  ```
  
### Development Setup

[Backend Server Setup](https://github.com/jurayev/trivia/tree/master/backend#getting-started)

[Frontend Server Setup](https://github.com/jurayev/trivia/tree/master/frontend#getting-started)
  
## Roadmap

Future TODOs:
* Add a live demo.
* Deploy application on Heroku.
* Add an additional question field such as rating and make all corresponding updates (db, api endpoints, add question form, etc.).
* Add users to the DB and track their game scores.
* Add capability to create new categories.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests [here](https://github.com/jurayev/trivia/blob/master/backend/test_flaskr.py) as appropriate and follow the PEP8 style guide.

## License

The content of this repository is licensed under a [MIT License.](https://github.com/jurayev/trivia/blob/master/LICENSE.md)
