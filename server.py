import mysql.connector
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi import HTTPException

app = FastAPI()

connections = list()
user_connections = dict()

REQUEST_LIMIT = 50


class User(BaseModel):
    id: int
    name: str
    age: int


def throttling(func):
    def wrapper(user_id: int):
        if user_connections.get(user_id, 0) > REQUEST_LIMIT:
            raise HTTPException(status_code=429, detail='Too Many Request')
        return func(user_id)
    return wrapper


def get_connection(user_id: int):
    try:
        db = mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            password='ali123',
            port=3306,
            database='throttling'
        )
        user_connections[user_id] = user_connections.get(user_id, 0) + 1
        connections.append(db)
        return db.cursor()
    except mysql.connector.errors.DatabaseError as e:
        raise HTTPException(status_code=409, detail=e.msg)


@app.get('/{user_id}')
def get_user(user_id: int):
    connection = get_connection(user_id)
    connection.execute(f'SELECT * FROM User Where id={user_id}')
    _user = connection.fetchone()
    user = User(id=_user[0], name=_user[1], age=_user[2])
    return user.dict()
