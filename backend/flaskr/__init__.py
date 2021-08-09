import os
from re import search
from flask import(
  Flask,
   request,
    abort, 
    jsonify)
from flask.globals import current_app
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
import sys
from sqlalchemy.orm import selectin_polymorphic, selectinload


from sqlalchemy.sql.operators import startswith_op
from werkzeug.wrappers import Response


from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10
ZERO=0
#create paginate for questions
def paginateQustions(request , selection):
   page = request.args.get('page' , 1 , type=int)
   start =(page-1)*QUESTIONS_PER_PAGE
   end = start + QUESTIONS_PER_PAGE
   questions = [question.format() for question  in selection]
  #return current questions 
   return  questions[start:end]
   

#test_config=None
def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  CORS(app)
  @app.after_request
  def after_request(response):
    response.headers.add ('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    response.headers.add ('Access-Control-Allow-Headers', 'GET, POST, PATCH, DELETE, OPTION')
    return response 
   
  # get request all avaliable categories 
  @app.route('/categories', methods=['GET'] )
  def categories ():
     categories = Category.query.order_by(Category.id).all()
     Category_List = {category.id: category.type for category in categories}
    

     if len (Category_List) ==ZERO:
          abort(404)
     return jsonify({
            'success': True,
            'categories': Category_List
        })

  @app.route('/questions', methods=['GET'])
  def questions():
   selectin = Question.query.order_by(Question.id).all()
   now_questions =paginateQustions(request , selectin)
   if len(now_questions)==ZERO:
        abort(404)
   
   Category_List = {category.id: category.type for category in categories}
  
   return jsonify({
    'success': True,
    'questions':  now_questions, 
     'total_of_questions':len(selectin),
     'categories':Category_List
  })
   
    
    
  

  #using after rquest 
  #after_request()
  #get Category
  #categories()
      
  #get questions()
  #questions()
  

  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 
  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions/<int:id>' , methods=['DELETE'])  
  def delete_questions(id):
      question = Question.query.filter(Question.id == id ).one_or_none()
      if question is None: 
         abort(404)  
      question.delete()
     
      return jsonify ({
        'success':True ,             
      })
      

      

   
 # Create an endpoint to POST a new question, 
  #which will require the question and answer text, 
  #category, and difficulty score.

 
  @app.route('/questions/add' , methods=['POST'])
  def add_question():
     body =request.get_json()
     newQuestions = body.get('question',None)
     newAnswer=body.get('answer',None)
     newDifficulty = body.get('difficulty' ,None)
     newCategory = body.get('category' , None)

     try:
      question = Question(
        question = newQuestions ,
      answer =newAnswer , 
      difficulty =newDifficulty,
      category=newCategory
     )
     

      question.insert()
      return jsonify({
                'success': True,
                'message':'Question successfully added'
                
            }),201
     except:
        abort(422)
   
   
 # Create a POST endpoint to get questions based on a search term. 
  #It should return any questions for whom the search term 
  #is a substring of the question. 

  
  @app.route('/questions/search', methods=['POST'])
  def search_question():

      search_term = request.get_json()['searchTerm']
      selcet = Question.query.filter(Question.question.ilike(f'%{search_term}%')).all()
      reslult_current_q = paginateQustions(request ,selcet )
      categories =Category.query.all()
      body={}
      for category in categories:
        body[category.id] = category.type
        if reslult_current_q == ZERO:
         abort(404)


      return jsonify({
           'success': True,
           'questions':reslult_current_q,
           'total_questions':len(selcet),
           'categories' :body,
           'reslult_current_q':'all'
            
      }),200

  
  #Create a GET endpoint to get questions based on category. 

  #TEST: In the "List" tab / main screen, clicking on one of the 
  #categories in the left column will cause only questions of that 
  #category to be shown. 
  
  @app.route('/categories/<int:id>/questions' , methods=[ 'GET'])
  def get_questions_based_category(id):
    selection = Question.query.filter(Question.category==id).all()
    category = Category.query.get(id)
    result_q = paginateQustions(request , selection)
    if len(result_q) ==ZERO: 
      abort( 404)
    return jsonify({
      'success': True,
       'questions':result_q,
       'total_questions':len(result_q),
       'current_category':category.type
    }),200
  
  
  #Create a POST endpoint to get questions to play the quiz. 
  #This endpoint should take category and previous question parameters 
  #and return a random questions within the given category, 
  #if provided, and that is not one of the previous questions. 
  @app.route('/quizzes' , methods=['POST'])
  def game_quiz():
    try:
     body= request.get_json()
     previous_question = body['previous_questions']
     quiz_category = body['quiz_category']['id']
     if  quiz_category !=ZERO:
       selection = Question.query.filter(Question.category==id, Question.id.notin_( previous_question)).all()
     
     result = [question.format() for question in selection]
     if selection:
       question =result [random.randint(0,len(selection)-1)]
     else:
       question =None
      
       return jsonify({ 
         'success': True,
         'question':question

        }) 
 
    except:
       abort(422)
  #@TODO: 
  #Create error handlers for all expected errors 
  #including 404 and 422. 
  @app.errorhandler(404)
  def not_found_404(error):
     return jsonify({
       'success':False,
       'message': 'Resource Not Found',
       'error':404

     }),404
  @app.errorhandler(405)
  def method_not_allowed(error):
    return jsonify({
        "success":False,
        "message": "Method Not Alowed",
        "error": 405
      }),405
  @app.errorhandler(422)
  def unprocessable_entity(error):
    return jsonify({
        "success":False,
        "message": "unprocessable entity",
        "error": 422
      }),422

  @app.errorhandler(400)
  def  bad_request(error):
    return jsonify({
        "success":False,
        "message": "Bad request",
        "error": 400
      }),400

  @app.errorhandler(500)
  def server_error_500(error):
    return jsonify({
        'success':False,
        'message':"server error",
        'error':500
      }),500
      
  return app






