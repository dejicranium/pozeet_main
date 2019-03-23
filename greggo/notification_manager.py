import smtplib



class NotificationManger:
    def __init(self, notif):
        # get attributes from notif

        # the notification type
        self.type = notif.activity_type

        # the user to whom the notification is to be sent
        self.concerned = notif.user_id

        # in case the notification is to be broadcasted to a lot of users at once
        self.concerned_users = []

        # user's notification batch_id

        # get_user_notification_batch_id()


if __name__ == "__main__":
    s = smtplib.SMTP()
    s.connect('email-smtp.us-east-1.amazonaws.com', 587)
    s.starttls()
    s.login('AKIAINQFNUTBP2ZIEGYA', 'BMBAaqd2awU0y4v85LV6L7hLYv9muYO96oAHkw24kC2Z')

    msg = "From: notifications@pozeet.com\nTo: itisdeji@gmail.com\nSubject: You are Lame\n\nJust wanted to say hi ni o"

    print("Attempting to send")
    try:
        s.sendmail('notifications@pozeet.com', 'itisdeji@gmail.com', msg)
        s.se
    except Exception as e:
        print(e)
    else:
        print("Sent")