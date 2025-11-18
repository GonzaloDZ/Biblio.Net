import schedule
import time

def job():
    print("libro enviado aelfkn")

schedule.every(2).minutes.do(job)
schedule.every().day.at("03:00").do(job)

while True:
    schedule.run_pending()
    time.sleep(1)