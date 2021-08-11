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
  

  @app.route('/questions', methods=['GET'])
  def questions():
   selectin = Question.query.order_by(Question.id).all()
   now_questions =paginateQustions(request , selectin)
   categories = Category.query.order_by(Category.id).all()
   if len(now_questions)==ZERO:
        abort(404)
   
   Category_List = {category.id: category.type for category in categories}
  
   return jsonify({
    'success': True,
    'questions':  now_questions, 
     'total_of_questions':len(selectin),
     'categories':Category_List
  })
   
  @app.route('/categories' ,  methods=['GET'])  
  def get_categories():
        categories = Category.query.order_by(Category.id).all()
        Category_List = {category.id: category.type for category in categories}
        # abort 404 if no categories found
        if (len(Category_List) == ZERO):
            abort(404)
        # return data to view
        return jsonify({
            'success': True,
            'categories': Category_List
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
        'success':True             
      })
      

      

   
 # Create an endpoint to POST a new question, 
  #which will require the question and answer text, 
  #category, and difficulty score.

 
  @app.route('/questions' , methods=['POST'])
  def add_question():
    body = request.get_json()
    
    if body.get('searchTerm'):
            search_term = body.get('searchTerm')
            selection = Question.query.filter(Question.question.ilike(f'%{search_term}%')).all()
            if len(selection) == ZERO:
                abort(404)
            questions_current =paginateQustions(request, selection)
            total_q = len(Question.query.all())
            # return results
            return jsonify({
                'success': True,
                'questions': questions_current,
                'total_questions':total_q 
            })
    else:
      body =request.get_json()
      newQuestions = body.get('question','')
      newAnswer=body.get('answer','')
      newDifficulty = body.get('difficulty' ,'')
      newCategory = body.get('category' , '')
    
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
     previous_question = body.get('previous_questions' ,None ) 
     quiz_category = body.get('quiz_category' ,None)
     categoryid = quiz_category['id']

     if quiz_category is None or previous_question is None:
        abort(400)
     if categoryid == ZERO:
       question_all = Question.query.filter( Question.id.notin_(previous_question)).all()
     else:
       question_all = Question.query.filter(Question.id.notin_(previous_question), Question.category == categoryid).all()
       Aquestion =None
     if  question_all:
           Aquestion = random.choice( question_all)
         
     return jsonify({ 
         'success': True,
         'question':Aquestion.format()

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





