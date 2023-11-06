# JWT Authentication for Flask
This is source code for a video I made when demonstrating how to implement JWT Authentication for Flask REST APIs. This videos series walks through the following.
- Project SetUp
- Database Management with Flask-SQLAlchemy
- User Account Creation
- JWT Authentication with Flask-JWT-Extended


Install requirements
```bash
pip install requirements.txt
```

Create a `.env` file and set environment variables
```
FLASK_SECRET_KEY=<your-secret-key>
FLASK_DEBUG=<your-debug-boolean-value>
FLASK_SQLALCHEMY_DATABASE_URI=<your-sqlalchemy-db-uri>
FLASK_SQLALCHEMY_ECHO=<your-sqlalchemy-echo-value>
```

Create a `FLASK_APP` environment variable. 
```bash
export FLASK_APP=src/
```

Create the database by running 
```bash
flask shell
```

Finally run the application with
```flask run```