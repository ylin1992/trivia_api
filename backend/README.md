# Backend - Full Stack Trivia API 

### Installing Dependencies for the Backend

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)


2. **Virtual Enviornment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)


3. **PIP Dependencies** - Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:
```bash
pip install -r requirements.txt
```
This will install all of the required packages we selected within the `requirements.txt` file.


4. **Key Dependencies**
 - [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

 - [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

 - [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

### Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

### Running the server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.


# API References

## Getting Started
- Base URL: The api is not hosted as a base URL, instead, connect ```http://127.0.0.1:5000/``` or ```http://localhost:5000/``` to your frontend application

- Authentication: No authentication is required in this application 

## Error Handling
Errors are returned in JSON format:
```
{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
```
The API supports two types of status code
- 404: Data not found
- 422: Unproccessable
- 400: Bad request

## Endpoints

### GET/ categories
- General: Returns all categories, containing success flag and an array of categories, in which each category contains its type and id
- Example: ```curl http://localhost:5000/categories```
```
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "success": true
}
```

### GET /questions
- General: Returns all categories, questions, success flag and the number of questions in the database
- The returned question list is paginted in form of 10 questions per page 
- Example: ```curl http://localhost:5000/categories```
```
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "currentCategory": null, 
  "questions": [
    {
      "answer": "Tom Cruise", 
      "category": 5, 
      "difficulty": 4, 
      "id": 4, 
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    }, 
    {
      "answer": "Edward Scissorhands", 
      "category": 5, 
      "difficulty": 3, 
      "id": 6, 
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }, 
    {
      "answer": "George Washington Carver", 
      "category": 4, 
      "difficulty": 2, 
      "id": 12, 
      "question": "Who invented Peanut Butter?"
    }, 
    {
      "answer": "Lake Victoria", 
      "category": 3, 
      "difficulty": 2, 
      "id": 13, 
      "question": "What is the largest lake in Africa?"
    }, 
    {
      "answer": "The Palace of Versailles", 
      "category": 3, 
      "difficulty": 3, 
      "id": 14, 
      "question": "In which royal palace would you find the Hall of Mirrors?"
    }, 
    {
      "answer": "Agra", 
      "category": 3, 
      "difficulty": 2, 
      "id": 15, 
      "question": "The Taj Mahal is located in which Indian city?"
    }, 
    {
      "answer": "Escher", 
      "category": 2, 
      "difficulty": 1, 
      "id": 16, 
      "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
    }, 
    {
      "answer": "Mona Lisa", 
      "category": 2, 
      "difficulty": 3, 
      "id": 17, 
      "question": "La Giaconda is better known as what?"
    }, 
    {
      "answer": "One", 
      "category": 2, 
      "difficulty": 4, 
      "id": 18, 
      "question": "How many paintings did Van Gogh sell in his lifetime?"
    }, 
    {
      "answer": "Jackson Pollock", 
      "category": 2, 
      "difficulty": 2, 
      "id": 19, 
      "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
    }
  ], 
  "success": true, 
  "total_questions": 16
}
```

### DELETE /questions/<int:question_id>
- General: Input question's id as an integer and delete the the question corresponding to the id
- Returns a success flag and id of the deleted question
- Throws 422 error if no corresponding question is found
- Example: normal input: ```curl -X DELETE http://localhost:5000/questions/16```
```
{
  "error": 422, 
  "message": "unprocessable", 
  "success": false
}
```
- Example: deleted itidem doesn't exist: ```curl -X DELETE http://localhost:5000/questions/10000```
```
{
  "deleted": 16, 
  "success": true
}
```

### POST /questions
POST supports two functionalities, "search a question" and "create a new question"
The endpoints in general returns 422 error if it does not recieve JSON objects containing corresponding key (which will be explained below)
1. Search
- Search request can be made by sending JSON object that contains a "searchTerm" key, the server will search through the database to find questions that match the value of "searchTerm" in a case-insensitive manner.
- Returns a success flag, a paginted question list and the number of found questions
- Throws 404 error if no question is found
- Example of normal search: ```curl -X POST http://localhost:5000/questions -H 'Content-Type: application/json' -d '{"searchTerm": "1"}'```
```
{
  "questions": [
    {
      "answer": "Edward Scissorhands", 
      "category": 5, 
      "difficulty": 3, 
      "id": 6, 
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }, 
    {
      "answer": "3", 
      "category": 1, 
      "difficulty": 1, 
      "id": 24, 
      "question": "1+2"
    }
  ], 
  "success": true, 
  "total_questions": 2
}
```
- Example of not found error: ```curl -X POST http://localhost:5000/questions -H 'Content-Type: application/json' -d '{"searchTerm": "q"}'```
```
{
  "error": 404, 
  "message": "Data not found", 
  "success": false
}
```
2. Create a new question:
- Create request can be made by sending JSON object that does not contain "searchTerm" key, instead, keys listed below are strictly required.
    - ```question```: description of the new question
    - ```answer```: answer to the question
    - ```difficulty```: from 1~5, diffuclty out of the range will trigger 422 error
    - ```category```: from 0~6, category out of this range will trigger 422 error
- Returns a success flag and description of the newly created question
Example: ```curl -X POST http://localhost:5000/questions -H 'Content-Type: application/json' -d '{"question": "q1", "answer":"a1", "difficulty":1, "category":1}'```
```
{
  "question": {
    "answer": "a1", 
    "category": 1, 
    "difficulty": 1, 
    "id": 28, 
    "question": "q1"
  }, 
  "success": true
}
```
### GET /categories/<int:category_id>/questions
- Get all questions in the given category, paginated in 10 questions per page
- Returns a success flag, a paginated question list, number of total question in the category and current_category indicating the category_id in the query
- Throws 404 error if no question is found
- Example: ```curl http://localhost:5000/categories/1/questions```
```
{
  "current_category": 1, 
  "questions": [
    {
      "answer": "The Liver", 
      "category": 1, 
      "difficulty": 4, 
      "id": 20, 
      "question": "What is the heaviest organ in the human body?"
    }, 
    {
      "answer": "Alexander Fleming", 
      "category": 1, 
      "difficulty": 3, 
      "id": 21, 
      "question": "Who discovered penicillin?"
    }, 
    {
      "answer": "Blood", 
      "category": 1, 
      "difficulty": 4, 
      "id": 22, 
      "question": "Hematology is a branch of medicine involving the study of what?"
    }, 
    {
      "answer": "3", 
      "category": 1, 
      "difficulty": 1, 
      "id": 24, 
      "question": "1+2"
    }, 
    {
      "answer": "a1", 
      "category": 1, 
      "difficulty": 1, 
      "id": 26, 
      "question": "q1"
    }, 
    {
      "answer": "a1", 
      "category": 1, 
      "difficulty": 1, 
      "id": 28, 
      "question": "q1"
    }
  ], 
  "success": true, 
  "total_questions": 6
}
```

### POST /quizzes
- Input an array of past questions' id and a category object, return a randomly picked question which is not in the list of past question array
- Input:
    - ```previous_question```: an array of question id of which the question hasn't been used
    - ```quiz_category```: a JSON object containg the type and id of the selected category
    Note: send id = 0, category = "type: Click" for all categories (examplify as below)
    ```
    {
        previous_question: [],
        quiz_category: {
            type: 'Click',
            id: 0
        }
    }
    ```
- Return: a randonly picked question and a success flag
- Example: ```curl -X POST http://localhost:5000/quizzes -H 'Content-Type: application/json' -d '{"previous_questions":[], "quiz_category":{"type": "Science", "id": 1}}'  ```
```
{
  "question": {
    "answer": "Alexander Fleming", 
    "category": 1, 
    "difficulty": 3, 
    "id": 21, 
    "question": "Who discovered penicillin?"
  }, 
  "success": true
}
```

## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
