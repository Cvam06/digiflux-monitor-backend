import time
import atexit

from apscheduler.schedulers.background import BackgroundScheduler

scheduler = None

# def print_date_time():
#     ping_all()


def start_scheduler(ping_all, app):
    with app.app_context():
        global scheduler
        scheduler = BackgroundScheduler()
        scheduler.add_job(func=ping_all, trigger="interval", seconds=60, id='website_polling')
        scheduler.start()

def stop_scheduler():
    global scheduler
    scheduler.remove_job('website_polling')
    atexit.register(lambda: scheduler.shutdown())

