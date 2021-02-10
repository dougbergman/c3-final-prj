import logging
import azure.functions as func
#import psycopg2
import os
from datetime import datetime
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def main(msg: func.ServiceBusMessage):

    notification_id = int(msg.get_body().decode('utf-8'))
    logging.info('Python ServiceBus queue trigger processed message: %s',notification_id)

    # TODO: Get connection to database
    
    dbname="techconfdb"
    user="azureadmin@techconfdb"
    password="Cyclone22!"
    host="techconfdb.postgres.database.azure.com"
    sslmode = "require"
 
    #cursor = connection.cursor()
    conn_string = "host={0} user={1} dbname={2} password={3} sslmode={4}".format(host, user, dbname, password, sslmode)
    conn = psycopg2.connect(conn_string)
    print("Connection established")
    logging.info('after connetion:')
    
    try:
        #notification_id = msg.get_body().decode('utf-8')
        notification_query = cursor.execute("SELECT message, subject FROM notification WHERE id = {};".format(notification_id))
        logging.info('after query: %s',notification_query)
        logging.info('try:')
        print("func: notif query")
   # try:
        # TODO: Get notification message and subject from database using the notification_id
        notification_query = cursor.execute("SELECT message, subject FROM notification WHERE id = {};".format(notification_id))
        message = Message(str(notification.id))        
        print("*** func : get not and subj")

        # TODO: Get attendees email and name
        notification_query = cursor.execute("SELECT message, subject FROM notification WHERE id = {};".format(notification_id))
  
        # TODO: Loop through each attendee and send an email with a personalized subject
        #attendees = Attendee.query.all()
        for attendee in attendees:
                    subject = '{}: {}'.format(attendee[0], notification_query[0][1])
                    logging.info('subject : %s',subject)
                    body = notification_query[0][0]
                    message = Mail(
                        from_email=ADMIN_EMAIL_ADDRESS,
                        to_emails=attendee[1]
                        subject=subject,
                        plain_text_content=body)
        try:
            sg=SendGridAPIClient("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")
            sg.send(message)
            print ("** func: send message")
    
        except Exception as e:
            print(e.message)

        # TODO: Update the notification table by setting the completed date and updating the status with the total number of attendees notified
        notification.completed_date = datetime.utcnow()
        notification.status = 'Notified {} attendees'.format(len(attendees))
    except (Exception, psycopg2.DatabaseError) as error:
        logging.error(error)
    finally:
        logging.info('after finally')
        print("Func finally done")
        