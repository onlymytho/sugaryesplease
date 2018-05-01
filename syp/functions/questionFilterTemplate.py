def questionFilter(segment_column, topic=False):
    """ question에 column으로 추가할 사항들을 함수로 만들어놓음. question을 검증하고 보여줄지 여부를 결정"""

    # DB의 question 테이블에서 segment_column에 가능한 값이 어떤 것들이 있는지 확인하는 작업
    try:
        db.cur.execute('SELECT distinct %s FROM question' % (segment_column))
        response_list = db.cur.fetchall()[0]
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)            # if connection error, print the error.
        return apiReturnValue(code=500, error_type=e, error_message="Database connection is failed.")

    # recipe에 있는 segment_column의 값이 response_list에 있는 값과 일치하거나 null일 때만 해당 질문을 보여주는 로직
    try:
        if topic == False:
            for rcp in recipe:
                for response_item in response_list:  # 맞는 question을 찾았으면, question의 가능 답변 목록인 response_list를 바탕으로
                    if rcp[segment_column] == response_item: # 해당 question의 response가 response와 같을 경우,
                        if question[segment_column] == response_item or null:
                            next_question = question
                        else: continue
                    elif !rcp[segment_column] and !question[segment_column]: # recipe에서 segment_column 관련 값이 없거나 question에 해당 segment_column가 없으면
                        next_question = question
                    else: continue
        elif topic == True:
            for rcp in recipe:
                for response_item in response_list:  # 맞는 question을 찾았으면, question의 가능 답변 목록인 response_list를 바탕으로
                    if rcp[segment_column][response_item]: # 해당 question의 response가 response와 같을 경우,
                        if question[segment_column] == response_item or null:
                            next_question = question
                        else: continue
                    elif !rcp[segment_column][response_item] and !question[segment_column]: # recipe에서 segment_column 관련 값이 없거나 question에 해당 segment_column가 없으면
                        next_question = question
                    else: continue
    except WrongAccessException as e: # gender가 null 일 때, question에 gender가 있으면 뭔가 잘못된 것. 유저가 다이렉트링크로 들어왔거나, 플로우가 잘못된 것.
        return apiReturnValue(code=403, error_type=e, error_message="Invalid access is detected.")



# def gender():
#     try:
#         if recipe['gender'] == "male":
#             if question['gender'] == "male" or null: next_question = question
#             else: pass
#         elif recipe['gender'] == "female":
#             if question['gender'] == "female" or null: next_question = question
#             else: pass
#         elif recipe['gender'] == null and question['gender'] == False: next_question = question
#     except WrongAccessException as e: # gender가 null 일 때, question에 gender가 있으면 뭔가 잘못된 것. 유저가 다이렉트링크로 들어왔거나, 플로우가 잘못된 것.
#         return {"statusCode": 503, # 숫자 다시 제대로 보내야 함
#                 "message": "WrongAccessException"}
#
# if recipe[column] == response_item:
#     if question[column] == response_item or null: next_question = question
#     else: continue
# elif recipe[column] == null and question[column]
