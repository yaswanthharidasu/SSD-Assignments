from flask import Flask
from flask_login import LoginManager, login_manager, login_user, logout_user, login_required, UserMixin
import pymysql
import sys

# Initialize the App
app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# Login
login_manager = LoginManager()
login_manager.init_app(app)

# Connect to the database
try:
    db = pymysql.connect(host="localhost", port=3306,
                         db="ssd", user="root", password="")
    print("===============CONNECTED TO DATABASE=================")
    cursor = db.cursor()

    # Create User and Menu Tables if not exists
    menu_table = """CREATE TABLE IF NOT EXISTS MENU(
                ID INT NOT NULL PRIMARY KEY,
                HALF INT NOT NULL,
                FULL INT NOT NULL)"""

    user_table = """CREATE TABLE IF NOT EXISTS USER(
                USERNAME VARCHAR(20) NOT NULL PRIMARY KEY,
                PASSWORD VARCHAR(20) NOT NULL)"""

    cursor.execute(menu_table)
    cursor.execute(user_table)

    # Insert chef into the user table if not exists
    try:
        insert_chef = """INSERT IGNORE INTO USER (USERNAME, PASSWORD)
                        VALUES ('chef', 'chef')"""
        cursor.execute(insert_chef)
        db.commit()
    except pymysql.Error as err:
        print(err)

except pymysql.MySQLError as err:
    print("============ERROR: While connecting to db==============")
    print(err)
    sys.exit()


class User(UserMixin):
    pass

# ========================================== Routes ===============================================


@app.route('/', methods=['GET'])
def initialize():
    return "Server running at 8080...."


if __name__ == "__main__":
    app.run(port=8080, debug=True)
