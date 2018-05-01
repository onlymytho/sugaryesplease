import database as db
import json
from datetime import datetime

# Connect database at the outside of lambda_handler_function to reuse database connection during invocations.
db.connect()

# Lambda_handler_function
def hello(event, context):

    first_name = event['first_name']
    last_name = event['last_name']
    email = event['email']
    created_at = datetime.now()
    query = 'INSERT INTO users (id, email, first_name, last_name, created_at) VALUES (default, %s, %s, %s, %s);'
    data = (email, first_name, last_name, created_at)

    db.cur.execute(query, data)
    db.conn.commit()

    users = db.cur.execute('SELECT * from users')

    body = {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "result": users
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body),
        "users": json.dumps(users)
    }

    return response
