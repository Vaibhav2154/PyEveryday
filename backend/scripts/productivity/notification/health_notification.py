#code by:- Keshav Maheshwari : github-> @kehav1534
import time
import threading
from plyer import notification
import json
import asyncio
from pathlib import Path

dirPath = Path(__file__).resolve().parent  #get the path of notification folder.
myapp = "Good Health"   #name of the notification.
file_path = dirPath/'.icon'


def readJson(path=dirPath/"notifications.json", data=None):
    ## This function read the notification.json
    with open(path, "r+") as file:
        notifi_data = json.load(file)
        return notifi_data

notification_list = readJson()

def notify():
    #These are some of my reminders. You can also add your custom reminders.
    # You can make your custom reminder by adding a it into notifications.json                      
    def notifications(n):
        while True:
            try:
                time.sleep(notification_list[n]["sleep"])
                #wait for the time after which the notification is called.
                notification.notify(
                    title  = notification_list[n]["title"],
                    message = notification_list[n]["message"],
                    app_icon = str( dirPath/"icon/Logo.ico"),
                    timeout = 10,
                    app_name = myapp
                )
            except Exception as e:
                pass
            
    #Made threads of notifications so that they keep running in parallel-like fasion.
    ## runs multiple notifications.
    for mesg in range(len(notification_list)):                                       
        notify_th = threading.Thread(target= notifications, args=(mesg, ))
        notify_th.start()

notification.notify(
    title = myapp,
    message = "Application running in background.",
    app_icon = str(dirPath/"icon/smile.ico") ,
    timeout = 10,
    app_name = myapp
)
#func_list contains the list of functions which are required to be threaded
#add notify to the list
thread = threading.Thread(target=notify)
thread.start()
