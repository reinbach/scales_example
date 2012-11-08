from flask import Flask, render_template

import config

from stats import STATS

app = Flask(__name__)
app.debug = config.DEBUG

@app.route("/")
def home():
    STATS.success += 1
    return render_template("index.html")

def main():
    app.run()

if __name__ == "__main__":
    main()