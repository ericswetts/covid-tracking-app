from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import re

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///covid.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# DB
db = SQLAlchemy(app)
class Users(db.Model):
    # primary_key makes it so that this value is unique and can be used to identify this record.
    id = db.Column('user_id',db.Integer, primary_key=True)
    username = db.Column(db.String(24))
    email = db.Column(db.String(64))
    pwd = db.Column(db.String(64))

    # Constructor
    def __init__(self, username, email, pwd):
        self.username = username
        self.email = email
        self.pwd = pwd

# Routes!
@app.route("/api/users", methods=["GET", "POST", "DELETE"])
def users():
    method = request.method
    if (method.lower() == "get"):  # READ
        users = Users.query.all()
        # Get all values from db
        return jsonify([{"id": i.id, "username": i.username, "email": i.email, "pwd": i.pwd} for i in users])
    elif (method.lower() == "post"):  # CREATE
        try:
            username = request.json["username"]
            email = request.json["email"]
            pwd = request.json["pwd"]
            if (username and pwd and email):  # Checks if username, pwd or email are empty
                try:
                    user = Users(username, email, pwd)  # Creates a new record
                    db.session.add(user)  # Adds the record for committing
                    db.session.commit()  # Saves our changes
                    return jsonify({"success": True, "cool": "beans"})
                except Exception as e:
                    return ({"error": e})
            else:
                # jsonify converts python vars to json
                return jsonify({"error": "Invalid form"})
        except:
            return jsonify({"error": "Invalid form"})
    elif (method.lower() == "delete"):  # DESTROY
        try:
            uid = request.json["id"]
            if (uid):
                try:
                    # Gets user with id = uid (because id is primary key)
                    user = Users.query.get(uid)
                    db.session.delete(user)  # Delete the user
                    db.session.commit()  # Save
                    return jsonify({"success": True})
                except Exception as e:
                    return jsonify({"error": e})
            else:
                return jsonify({"error": "Invalid form"})
        except:
            return jsonify({"error": "m"})


# @app.route("/")
# def index():
#     db.create_all()
#     return("hello squirrels")



#functions to connect backend to frontend?
def getUsers():
    users = Users.query.all()
    return [{"id": i.id, "username": i.username, "email": i.email, "password": i.pwd} for i in users]

def addUser(username, email, pwd):
    if (username and pwd and email):
        try:
            user = Users(username, email, pwd)
            db.session.add(user)
            db.session.commit()
            return True
        except Exception as e:
            print(e)
            return False
    else:
        return False

def removeUser(uid):
    uid = request.json["id"]
    if (uid):
        try:
            user = Users.query.get(uid)
            db.session.delete(user)
            db.session.commit()
            return True
        except Exception as e:
            print(e)
            return False
    else:
        return False


#Login and register check

@app.route("/api/login", methods=["POST"])
def login():
    try:
        email = request.json["email"]
        password = request.json["pwd"]
        if (email and password):
            users = getUsers()
            # Check if user exists
            return jsonify(len(list(filter(lambda x: x["email"] == email and x["password"] == password, users))) == 1)
        else:
            return jsonify({"error": "invalid form"})
    except:
        return jsonify({"error": "Invalid form"})

@app.route("/api/register", methods=["POST"])
def register():
    users = getUsers()
    try:
        email = request.json["email"]
        email = email.lower()
        password = request.json["pwd"]
        username = request.json["username"]
        # Check to see if user already exists
        users = getUsers()

        if(len(list(filter(lambda x: x["email"] == email, users))) == 1):
            return jsonify({"error": "not unique email"})
        # Email validation check
        if not re.match(r"[\w\._]{5,}@\w{3,}.\w{2,4}", email):
            return jsonify({"error": "regex thing"})
        addUser(username, email, password)
        return jsonify({"success": True})
    except:
        return jsonify({"error": "Something else is broken"})


if __name__ == "__main__":
    app.run(debug=True)
