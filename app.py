import os
from flask import Flask
if os.path.exists("env.py"):
    import env


# Create instance of Flask
app = Flask(__name__)


# Test route and function view
@app.route("/")
def hello():
    return "Hello World!"


# Set how & where to run the app
if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
