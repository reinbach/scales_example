from greplin import scales
from greplin.scales.meter import MeterStat

import config
import pusher

STATS = scales.collection(
    "/web",
    scales.IntStat('errors'),
    scales.IntStat('success'),
    scales.PmfStat('latency'),
    scales.IntStat('counter'),
    MeterStat('hits'),
)

def main():
    """Periodically send metrics out"""
    stat_server = pusher.PeriodicPusher("localhost", 5001, "/stats", 5)
    for allowed in config.STAT_RULES_ALLOWED:
      stat_server.allow(allowed)
    stat_server.run()

if __name__ == "__main__":
    main()