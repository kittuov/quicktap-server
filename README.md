# quicktap-server
## installation
* You require `python > 3.4` or `python3 with asyncio` 
* install the dependencies `pip install requirements.txt`
* run dev server with `python3 manage.py runserver 0.0.0.0:8000` 
* it runs the http server on port 8000 and websocket server at 8001

> in case you dont have those ports available, you can change http port right in the runserver command, and Websocket port at `QuickTap > settings.py > WEBSOCKET_PORT `

> Note:
> you can use localhost:8000/admin to manage edit various database entries
