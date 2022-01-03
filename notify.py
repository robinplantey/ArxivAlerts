import os
from gi import require_version
from subprocess import call

require_version('Notify', '0.7')
from gi.repository import Notify, GLib

mainloop = GLib.MainLoop()
Notify.init("Arxiv Alert")

def callback(notif, action):
    call(["xdg-open", "publications.html"])
    mainloop.quit()

def desktopNotification():
    notification = Notify.Notification.new("New articles")
    notification.add_action("action_click", "Open", callback)
    notification.set_urgency(1)
    notification.set_timeout(30000)
    notification.show()
    mainloop.run()
