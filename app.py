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

@app.route("/metric/time/")
def metric_time():
    with STATS.latency.time():
        x = 0
        for a in range(random.randint(10000, 1000000)):
            x += a
    return json.dumps({"number": a})

@app.route("/metric/counter/")
def metric_counter():
    STATS.counter += 1
    return json.dumps({"counter": "+1"})

@app.route("/metric/metered/")
def metric_metered():
    STATS.hits.mark()
    return json.dumps({"hits": "metered"})

def main():
    app.run()

if __name__ == "__main__":
    main()