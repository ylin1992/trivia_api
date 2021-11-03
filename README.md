# Trivia FUll Stack Project
This project provides a puzzles-solving game in which user is allowed to answer questions based on the selected categories, add new questions and view all questions by categories.
This project also contains frontend, backend API and testing script. Features are listed as follows, have fun!
1. Display questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer.
2. Delete questions.
3. Add questions and require that they include question and answer text.
4. Search for questions based on a text query string.
5. Play the quiz game, randomizing either all questions or within a specific category.


## Getting Started

## Backend
### Environment setup

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)


2. **Virtual Enviornment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)


3. **PIP Dependencies** - Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:
```bash
pip install -r requirements.txt
```
This will install all of the required packages we selected within the `requirements.txt` file.

### Lauch the server

1. Direct to the root folder of the project, set environment variable for flask app and run the server by the following
```
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

2. Refer to ```backend/README.md``` for more information on endpoints and backend structure

## Frontend
### Environment setup
1. **node js** - The project is designed with node js and react js, direct to ```frontend``` directory and install dependancy
```
npm i
```
2. **Lauch the frontend** - After installing all modules for node, run the following scripts to launch the frontend 
```
npm start
```
3. **Visit frontend** - Frontend is hosted at ```http://localhost:3000``` by default

4. Refer to ```frontend/README``` for more detailed information


# Author
The project is a template of [https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd0044?gclid=Cj0KCQjw5oiMBhDtARIsAJi0qk1evjd3o2g1P_fN7k7w61V1LoQb26TlotiBybLPsTh7dqdGsz8d42oaAiOpEALw_wcB&utm_campaign=12908932988_c&utm_keyword=udacity%20full%20stack_e&utm_medium=ads_r&utm_source=gsem_brand&utm_term=124509199111](Udacity Fullstack Development Nano Degree).