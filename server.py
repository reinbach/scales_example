import gevent

from gevent import monkey

monkey.patch_all()

from app import main as app
from stats import main as stats

if __name__ == "__main__":
    gevent.joinall([
        gevent.spawn(app),
        gevent.spawn(stats)
    ])
