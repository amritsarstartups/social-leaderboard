from apscheduler.schedulers.blocking import BlockingScheduler
from mods.ext.Tagdump import hashtag_fetch_tw, hashtag_fetch_insta
from mods.ext.Stats import calculate_stats
from time import time

def tasks():
	t1 = time()
	print("Starting Schedular")
	start_date_tw  = "2017-06-14"
	hashtags = ['lifeatstatusbrew', 'sbcon']
	for h in hashtags:
		hashtag_fetch_tw(h, start_date_tw)
		hashtag_fetch_insta(h)
	calculate_stats()
	print("Task Complete")
	t2  = time()
	print("Task completed in %s sec", t2-t1)


tasks()
sched = BlockingScheduler()
@sched.scheduled_job('interval', minutes=4)
def timed_job():
	try: 
		tasks()
	except Exception as e: 
		print("Schedular Error", e)

sched.start()
	