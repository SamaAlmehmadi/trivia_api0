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
## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

### Running the server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export Flask_APP=flaskr 
export FLASK_ENV=development
flask run
```

setting the `FLASK_ENV` varbile to `development` will deltct file  will detect file changes and restart the server automatically.
setting the `FLASK_ENV` varbile to `flaskr` directs flask to use the flaskr directory and the `__init__.py`

### Running Your Frontend in Dev Mode

The frontend app was built using create-react-app. In order to run the app in development mode use ```npm start```. You can change the script in the ```package.json``` file. 

Open [http://localhost:3000](http://localhost:3000) to view it in the browser. The page will reload if you make edits.<br>
```bash
npm start
```

## API Reference
### Gtting Start 
- Back Base URL : http://127.0.0.1:5000/
- Front Base URL: http://127.0.0.1:3000/

## Erorr Handling 
the Erorr formated like : 
```js 
'success': Flalse ,
'error':400,
'message' :'Bad request error'

 ```
 The error codes currently returned are:

  - 400 – Bad request error
  - 404 – resource not found
  - 422 – Uncrossable entity
  - 500 – Internal error, please try again.

  ## Endpoints
  ### GET /categories
  - sample curl `curl http://127.0.0.1:5000/categories`
 ```js  {
        'categories': {
            '1': 'Science', 
            '2': 'Art", 
            '3': 'Geography', 
            '4': 'History', 
            '5': 'Entertainment', 
            '6': 'Sports'
        }, 
        'success': True
    }
```
### GET /questions
- sample curl `curl http://127.0.0.1:5000/questions`
 ```js     {
    "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
    },
    "questions": [
        {
            "answer": "Tom Cruise",
            "category": 5,
            "difficulty": 4,
            "id": 4,
            "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
        },
       
    ],
    "success": True,
    "total_questions": 19
}
```
### DELETE /questions/int:id
```js 
{
          "success": True,
        }
```
### POST / questions
Sample: `curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{'question': 'what is my age?', 'answer': '21', 'difficulty': 4, 'category' : 4})'`

```js 
{
          "success": True,
        }
```

### POST /questions/search
- Request body {seachTerm:string}
EXample:
```js
{
  "questions": [
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    }
  ],
  "success": True,
  "total_questions": 1,
  "categories": {1: "Science", 2: "Art", 3: "Geography", 4: "History", 5: "Entertainment", 6: "Sports"},
  "current_category" : "all"
}
 ```

### GET/categories/int:id/questions
 - search besed on categories
 - Example 
 ```js
 {
  "current_category": "Science",
  "questions": [
    {
      "answer": "The Liver",
      "category": 1,
      "difficulty": 4,
      "id": 20,
      "question": "What is the heaviest organ in the human body?"
    },
   
  ],
  "success": true,
  "total_questions": 3
}


 
  ```

  ### POST  /quizzes
 - Example

 ```js 
 {
    "success": true,
    "question": {
    "answer": "George Washington Carver",
    "category": 4,
    "difficulty": 2,
    "id": 12,
    "question": "Who invented Peanut Butter?"
  }
}   
 ``` 

## Athors 
Sama Almehmadi 
Udacity team provided fornt end files 