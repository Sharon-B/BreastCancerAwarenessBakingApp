import os
from flask import Flask, render_template
if os.path.exists("env.py"):
    import env


# Create instance of Flask
app = Flask(__name__)

# Index
@app.route("/")
@app.route("/index")
def index():

    return render_template("index.html")

@app.route("/awareness")
def awareness():

    return render_template("awareness.html")


# Set how & where to run the app
if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)

