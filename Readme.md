Run Server with uvicorn:


``python uvicorn server:app``

then run clients with:

``python client.py 1 0.5``

* first arg is user_id 
* second arg is sleep_time

Now you can play with ``THROTTLING_IS_ACTIVE``, ``REQUEST_LIMIT``, ``TIME_LIMIT`` in server.py