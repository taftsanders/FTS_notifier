import notify2

APP_NAME = 'FTS_Notifier'

# Construct a linux notifier to send notifications to the OS
def notification(caseNumber, message, severity):
    notify2.init(APP_NAME)
    if severity == 'critical':
        n = notify2.Notification(caseNumber, message, './dialog-error.svg')
        n.set_urgency(notify2.URGENCY_CRITICAL)
        n.show()
    elif severity == 'warning':
        n = notify2.Notification(caseNumber, message, './dialog-warning.svg')
        n.set_urgency(notify2.URGENCY_CRITICAL)
        n.show()
    elif severity == 'normal':
        n = notify2.Notification(caseNumber, message, './dialog-information.svg')
        n.set_urgency(notify2.URGENCY_NORMAL)
        n.timeout(300000)
        n.show()
    elif severity == 'low':
        n = notify2.Notification(caseNumber, message, './dialog-positive.svg')
        n.set_urgency(notify2.URGENCY_LOW)
        n.show()