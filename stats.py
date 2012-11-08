import pusher

from greplin import scales

STATS = scales.collection(
    "/web",
    scales.IntStat('errors'),
    scales.IntStat('success'),
)

def main():
    pusher.PeriodicPusher("localhost", 5001, "/web", 5).run()

if __name__ == "__main__":
    main()