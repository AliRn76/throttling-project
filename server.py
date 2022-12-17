import mysql.connector
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi import HTTPException
from datetime import datetime, timedelta

app = FastAPI()

connections = list()
user_connections = dict()

THROTTLING_IS_ACTIVE = True
REQUEST_LIMIT = 5
TIME_LIMIT = timedelta(minutes=1)


class User(BaseModel):
    id: int
    name: str
    age: int


def throttling(func):
    def wrapper(user_id: int):
        if THROTTLING_IS_ACTIVE and user_connections.get(throttling_key(user_id), 0) > REQUEST_LIMIT:
            raise HTTPException(status_code=429, detail='Too Many Request')
        return func(user_id)
    return wrapper


def round_dt(dt, delta):
    return datetime.min + round((dt - datetime.min) / delta) * delta


def throttling_key(user_id: int):
    rounded_time = round_dt(datetime.now(), TIME_LIMIT)
    return f'{rounded_time}-{user_id}'


def get_connection(user_id: int):
    try:
        db = mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            password='ali123',
            port=3306,
            database='throttling'
        )
        key = throttling_key(user_id)
        user_connections[key] = user_connections.get(key, 0) + 1
        connections.append(db)
        return db.cursor()
    except mysql.connector.errors.DatabaseError as e:
        raise HTTPException(status_code=409, detail=e.msg)


@app.get('/{user_id}')
@throttling
def get_user(user_id: int):
    connection = get_connection(user_id)
    connection.execute(f'SELECT * FROM User Where id={user_id}')
    _user = connection.fetchone()
    user = User(id=_user[0], name=_user[1], age=_user[2])
    return user.dict()
