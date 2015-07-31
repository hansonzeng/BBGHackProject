#!/usr/bin/python
from flask import *
app = Flask(__name__)

@app.route("/api")
def hello():
    return render_template("page.html")

if __name__ == "__main__":
    app.debug = True
    app.run()
