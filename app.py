import json
import random

from flask import Flask, render_template

import config

from stats import STATS

app = Flask(__name__)
app.debug = config.DEBUG

@app.route("/")
def home():
    STATS.success += 1
    return render_template("index.html")

@app.route("/work/")
def work():
    with STATS.latency.time():
        x = 0
        for a in range(random.randint(10000, 1000000)):
            x += a
    return json.dumps({"number": a})

def main():
    app.run()

if __name__ == "__main__":
    main()