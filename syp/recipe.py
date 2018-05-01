# 전체 플로우 요약
# frontend.show(question)                             # 프: question 정보 보여주기
# frontend.get(response)                              # 프: input을 통해 response 획득
# frontend.send(recipe_id, question_id, response)     # 프: 답변 정보 서버로 전송
# backend.process(response)
#     updateRecipe(response)                          # 백: 답변 내용을 레시피 DB에 업데이트
#     getUpdatedRecipe()  # return updated_recipe     # 백: 업데이트된 레시피 데이터 받기
#     getNextQuestion(updated_recipe)                 # 백: 업데이트된 레시피로 다음 질문 획득 후 질문 정보 프론트로 전송
#     return (question_id, content, resources)
# frontend.show(question_id, content, resources)

from .functions import apiReturnTemplate.*, questionFilterTemplate.*
import database as db

# Connect database at the outside of lambda_handler_function
# to reuse database connection during invocations.
db.connect()


# __main lambda handler function
def main(event, context):
    # Event: {recipe_id, question_id, response}
    try:                        # Check database connection
        db.cur.execute("SELECT VERSION()")
        results = db.cur.fetchone()

        if results: continue    # if DB is connected, continue.
        else: db.connect()      # if DB is not connected, connect.
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)            # if connection error, print the error.

    # parse the request
    result = (event['recipe_id'], event['question_id'], event['response'])

    # update the response to recipe table in database
    updateRecipe(result)

    # get updated recipe and get next question with it.
    next_question = getNextQuestion(getUpdatedRecipe())

    # return the next question to front-end
    return next_question



# __other functions
def updateRecipe(response):
    db.cur.execute('INSERT INTO recipe (recipe_id, question_id, response) VALUES (%s, %s, %s)', response)
    db.conn.commit()

def getUpdatedRecipe():
    db.cur.execute('SELECT * FROM recipe WHERE recipe_id = %s ORDER BY question_order asc' % (response[recipe_id]))
    updated_recipe = db.cur.fetchall()[0]
    return updated_recipe

def getNextQuestion(recipe):
    # 이전 질문의 다음 질문 가져오기

    def __init__():
        db.cur.execute("SELECT * FROM question")
        questions = db.cur.fetchall()
        stages = ['basic, topic, lifestyle, values'] # 사실 stage도 필요없는데.. question들 속에 순서 맞춰서 잘 넣어놓는게 중요하지..
        # get all next questions
        db.cur.execute("with t1 as (select question_order from questions where question_id = recipe['last_question_id']) SELECT * FROM questions q inner join t1 on q.question_order > t1.question_order")
        # show next question which is in same stage and filtered.
        try:
            for stage in stages:
                for question in questions:
                    if question['stages'] == stage:
                        return getFilteredQuestion(question) # 이 안에서 걸러진 question들이 return 됨.
                    else:
                        pass
        finally:
            return apiReturnValue(code=200, data=getRecommendedProducts()) # 만약 더 이상 질문이 없으면 Recommended Products를 보내줌

    def getFilteredQuestion(question):
        # question은 question 테이블의 한 row
        next_question = {}
        questionFilter('topic', topic=True)
        questionFilter('seg_experience')
        questionFilter('seg_gender')
        questionFilter('seg_prenatal')
        questionFilter('seg_age')
        questionFilter('seg_vegetarian')
        questionFilter('seg_electronic')
        return next_question

    def getRecommendedProducts():
        # getRecommendedProducts():
        # questions 테이블에 어떤 제품에 점수 얼마줄건지까지 컬럼 넣어야 함.
        # 결과적으로 recipe 데이터 넣으면 모든 제품과 점수가 나오고, 그걸 for문으로 다 더하다보면 제품별 점수가 나옴.
        # 이 결과값을 recommendation 테이블에 유저별로 저장 및 return 해줌.
        db.cur.execute("SELECT product_id, score FROM questions q INNER JOIN recipe r ON q.id = r.question_id")
        product_scores = db.cur.fetchone()
        result = {}
        for product in product_scores:
            if result[product['product_id']]:
                result[product['product_id']] += product['score']
            else:
                result[product['product_id']] = product['score']
        return result
