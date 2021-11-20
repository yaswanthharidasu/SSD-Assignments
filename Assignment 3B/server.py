from enum import unique
from flask import Flask, json, request, jsonify
from flask_login.mixins import UserMixin
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_manager, login_user, logout_user, login_required, UserMixin
import pymysql
from sqlalchemy.orm import backref

# Initializing the App
app = Flask(__name__)

# Database
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:''@localhost/ssd'
app.config['SECRET_KEY'] = 'secretkey'
db = SQLAlchemy(app)

# Login
login_manager = LoginManager()
login_manager.init_app(app)


class Item(UserMixin, db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True,
                   nullable=False, autoincrement=False)
    half = db.Column(db.Integer, nullable=False)
    full = db.Column(db.Integer, nullable=False)


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    is_chef = db.Column(db.Boolean, default=False)
    db.relationship('Transaction', backref='users')

    def get_id(self):
        return self.id


class Transaction(UserMixin, db.Model):
    __tablename__ = 'transactions'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    tip_percentage = db.Column(db.Float(2), nullable=False)
    no_of_persons = db.Column(db.Integer, nullable=False)
    half_items = db.Column(db.JSON, nullable=False)
    full_items = db.Column(db.JSON, nullable=False)
    items_amount = db.Column(db.Float(4), nullable=False)
    total_amount = db.Column(db.Float(4), nullable=False)
    draw_amount = db.Column(db.Float(4), nullable=False)
    date = db.Column(db.String(20), default='', nullable=False)


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route('/', methods=['GET'])
def initialize():
    return "Server running at 8080...."

# ===================================== Authentication ============================================


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    user = request.get_json()
    user = json.loads(user)
    username = user["username"]
    password = user["password"]
    # Check if username already exist in db
    check_name = User.query.filter_by(username=username).first()
    response = {}
    if check_name is not None:
        response = {
            "status": False,
            "message": "Username already exists"
        }
    else:
        newUser = User(username=username, password=password)
        db.session.add(newUser)
        db.session.commit()
        response = {
            "status": True,
            "message": "Registered Successfully"
        }
    return json.dumps(response)


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    user = request.get_json()
    user = json.loads(user)
    username = user["username"]
    password = user["password"]
    # Check if username exist in db
    check_name = User.query.filter_by(username=username).first()
    response = {}
    if check_name is None:
        response = {
            "status": False,
            "message": "No user exists with the username",
            "type": "none"
        }
    else:
        if check_name.password != password:
            response = {
                "status": False,
                "message": "Incorrect password",
                "type": "none"
            }
        else:
            login_user(check_name)
            response = {
                "status": True,
                "message": "Signedin Successfully"
            }
            # Checking the type of logged in user
            if check_name.username == "chef":
                response["type"] = "chef"
            else:
                response["type"] = "user"
    return json.dumps(response)


@app.route('/signout', methods=['GET'])
@login_required
def signout():
    logout_user()
    response = {
        "status": True,
        "message": "Signedout Successfully"
    }
    return json.dumps(response)

# =================================== Common routes ===============================================


@app.route('/retrieveMenu', methods=['GET'])
@login_required
def retrieveMenu():
    items = Item.query.all()
    response = ""
    d = dict()
    for item in items:
        d[item.id] = {"half": item.half, "full": item.full}
    response = json.dumps(d, indent=4)
    return response


@app.route('/storeTransaction', methods=['POST'])
@login_required
def storeTransaction():
    transaction = request.get_json()
    transaction = json.loads(transaction)
    username = transaction["username"]
    # Find user id by username
    check_name = User.query.filter_by(username=username).first()
    user_id = check_name.id
    tip_percentage = transaction["tip_percentage"]
    no_of_persons = transaction["no_of_persons"]
    half_items = json.dumps(transaction["half_items"])
    full_items = json.dumps(transaction["full_items"])
    items_amount = transaction["items_amount"]
    total_amount = transaction["total_amount"]
    draw_amount = transaction["draw_amount"]
    date = transaction["date"]

    newTransaction = Transaction(
        user_id=user_id, tip_percentage=tip_percentage,
        no_of_persons=no_of_persons, half_items=half_items,
        full_items=full_items, items_amount=items_amount,
        total_amount=total_amount, draw_amount=draw_amount,
        date=date
    )
    db.session.add(newTransaction)
    db.session.commit()
    response = {
        "status": True,
        "message": "Transaction stored Successfully"
    }

    return response


@app.route('/getTransactions/<username>', methods=['GET'])
@login_required
def getTransactions(username):
    check_name = User.query.filter_by(username=username).first()
    user_id = check_name.id
    transactions = Transaction.query.filter_by(user_id=user_id).all()
    print(transactions)
    d = dict()
    count = 1
    for item in transactions:
        d[count] = {
            "tip_percentage": item.tip_percentage,
            "no_of_persons": item.no_of_persons,
            "half_items": item.half_items,
            "full_items": item.full_items,
            "items_amount": item.items_amount,
            "total_amount": item.total_amount,
            "draw_amount": item.draw_amount,
            "date": item.date
        }
        count += 1
    response = json.dumps(d, indent=4)
    return response


# =================================== Chef Routes =================================================

@app.route('/addItem', methods=['POST'])
@login_required
def addItem():
    data = request.get_json()
    item = json.loads(data)
    id = item["id"]
    half = item["half"]
    full = item["full"]
    check_id = Item.query.filter_by(id=id).first()
    response = {}
    if check_id is not None:
        response = {
            "message": "Item with id already exists"
        }
    else:
        newItem = Item(id=id, half=half, full=full)
        db.session.add(newItem)
        db.session.commit()
        response = {
            "message": "Item added to the menu"
        }
    return json.dumps(response)

# =================================== Utility Methods =============================================


@app.route('/getUsers', methods=['GET'])
def getAllUsers():
    users = User.query.all()
    response = ""
    for user in users:
        response += user.username + "\n"
    return response


@app.route('/deleteall', methods=['DELETE'])
def deleteAll():
    db.session.query(User).delete()
    db.session.commit()
    return "Deleted all data"


def addChef():
    # Adding chef in the db
    check_name = User.query.filter_by(username="chef").first()
    if check_name is None:
        newUser = User(username="chef", password="chef", is_chef=True)
        db.session.add(newUser)
        db.session.commit()


def addMenu():
    pass


if __name__ == "__main__":
    db.create_all()
    addChef()
    app.run(port=8080, debug=True)
