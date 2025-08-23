Notifications.json : contains the notification data in json format.
    nid      :   Notification id, for unique identifiaction of notifications.
    title    :   Title of the notifications.
    message  :   Description of title.
    app_icon :   name of the icon file (.ico) format stored in icon folder.
    sleep    :   duration (in seconds) after which the notification appears.

note: app_icon is set to default in health_notification.py, can change it there in notify func.

health_notification.py + notifications.json file should be installed and run on client side PC. It does not require any online communicaion from server as all the notificaions are locally stored in Json file.

To get live notifications from, it needs to be connected to Websocket end-point intended to receive the notifications from.
Code needs to be upgraded accordingly.

To make this script run in background on PC, batch and VBScripts need to added which will further call this notification python file.

Further improvements can be added to either store the communicated notification or show it without storing it.