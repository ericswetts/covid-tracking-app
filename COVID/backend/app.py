from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///covid.db"

# DB
db = SQLAlchemy(app)
class Users(db.Model):
    id = db.Column('user_id', db.Integer, primary_key = True) # primary_key makes it so that this value is unique and can be used to identify this record.
    username = db.Column(db.String(24))
    email = db.Column(db.String(64))
    pwd = db.Column(db.String(64))

    # Constructor
    def __init__(self, username, email, pwd):
        self.username = username
        self.email = email
        self.pwd = pwd

# routes!
@app.route("/api/users", methods=["GET", "POST", "DELETE"])

def users():
    method = request.method
    if (method.lower() == "get"): # READ
        users = Users.query.all()
        return jsonify([{"id": i.id, "username": i.username, "email": i.email, "password": i.pwd} for i in users]) # Get all values from db
    elif (method.lower() == "post"): # CREATE
        try:
            username = request.json["username"]
            email = request.json["email"]
            pwd = request.json["pwd"]
            if (username and pwd and email): # Checks if username, pwd or email are empty
                try:
                    user = Users(username, email, pwd) # Creates a new record
                    db.session.add(user) # Adds the record for committing
                    db.session.commit() # Saves our changes
                    return jsonify({"success": True})
                except Exception as e:
                    return ({"error": e})
            else:
                return jsonify({"error": "Invalid form"}) # jsonify converts python vars to json
        except:
            return jsonify({"error": "Invalid form"})
    elif (method.lower() == "delete"): # DESTROY
        try:
            uid = request.json["id"]
            if (uid):
                try:
                    user = Users.query.get(uid) # Gets user with id = uid (because id is primary key)
                    db.session.delete(user) # Delete the user
                    db.session.commit() # Save
                    return jsonify({"success": True})
                except Exception as e:
                    return jsonify({"error": e})
            else:
                return jsonify({"error": "Invalid form"})
        except:
            return jsonify({"error": "m"})