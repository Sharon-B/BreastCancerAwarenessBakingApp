import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env


# Create instance of Flask
app = Flask(__name__)

# Set up configurations for MongoDB
app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
# Set up secret key
app.secret_key = os.environ.get("SECRET_KEY")

# Create an instance of PyMongo
mongo = PyMongo(app)


# Index
@app.route("/")
@app.route("/index")
def index():
    recipes = mongo.db.recipes.find()
    return render_template("index.html", recipes=recipes)


@app.route("/awareness")
def awareness():
    return render_template("awareness.html")


@app.route("/gallery")
def gallery():
    return render_template("gallery.html")


# Register
@app.route("/register", methods=["GET", "POST"])
def register():
    """
    Register a new user and add them to the database
    """
    if request.method == "POST":

        # check if username already exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            flash("Username already exists, please choose another")
            return redirect(url_for("register"))

        # check if email already exists in db
        existing_email = mongo.db.users.find_one(
            {"email": request.form.get("email").lower()})

        if existing_email:
            flash("Email already registered")
            return redirect(url_for("register"))

        register_user = {
            "username": request.form.get("username").lower(),
            "email": request.form.get("email"),
            "password": generate_password_hash(request.form.get("password"))
        }
        # Add new user to the db
        mongo.db.users.insert_one(register_user)

        # put the new user into 'session' cookie
        session["user"] = request.form.get("username").lower()
        flash("Registration Successful!")
        return redirect(url_for("index"))

    return render_template("register.html", title="Register")


# Log In
@app.route("/login", methods=["GET", "POST"])
def login():
    """
    Check if username & password match existing user & Login user
    """
    if request.method == "POST":
        # check if username exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            # Ensure hashed password matches user input
            if check_password_hash(
                    existing_user["password"], request.form.get("password")):
                session["user"] = request.form.get("username").lower()
                flash("Welcome, {}".format(
                    request.form.get("username")))
                return redirect(url_for("index"))

            else:
                # If invalid password match
                flash("Incorrect Username/Password")
                return redirect(url_for("login"))

        else:
            # If username doesn't exist
            flash("Incorrect Username/Password")
            return redirect(url_for("login"))

    return render_template("login.html", title="Log In")


# Log Out
@app.route("/logout")
def logout():
    """
    Clears the session & redirects to login page
    """
    session.pop("user")
    flash("You are now logged out")
    return redirect(url_for("login"))


# Recipes
@app.route("/recipes")
def recipes():
    """
    Displays all recipes
    """
    recipes = mongo.db.recipes.find()
    return render_template(
        "recipes.html", recipes=recipes, title="All Recipes")


# Set how & where to run the app
if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)