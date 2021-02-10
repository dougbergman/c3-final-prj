from app import app, db, queue_client
from datetime import datetime
from app.models import Attendee, Conference, Notification
from flask import render_template, session, request, redirect, url_for, flash, make_response, session
from azure.servicebus import Message
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import logging

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/Registration', methods=['POST', 'GET'])
def registration():
    if request.method == 'POST':
        attendee = Attendee()
        attendee.first_name = request.form['first_name']
        attendee.last_name = request.form['last_name']
        attendee.email = request.form['email']
        attendee.job_position = request.form['job_position']
        attendee.company = request.form['company']
        attendee.city = request.form['city']
        attendee.state = request.form['state']
        attendee.interests = request.form['interest']
        attendee.comments = request.form['message']
        attendee.conference_id = app.config.get('CONFERENCE_ID')

        try:
            db.session.add(attendee)
            db.session.commit()
            print("*** registering now!!")
            session['message'] = 'Thank you, {} {}, for registering!'.format(attendee.first_name, attendee.last_name)
            return redirect('/Registration')
        except:
            logging.error('Error occured while saving your information')

    else:
        if 'message' in session:
            message = session['message']
            session.pop('message', None)
            return render_template('registration.html', message=message)
        else:
             return render_template('registration.html')

@app.route('/Attendees')
def attendees():
    print("*** attendee")
    attendees = Attendee.query.order_by(Attendee.submitted_date).all()
    return render_template('attendees.html', attendees=attendees)


@app.route('/Notifications')
def notifications():
    print("*** notifications ")
    notifications = Notification.query.order_by(Notification.id).all()
    return render_template('notifications.html', notifications=notifications)

@app.route('/Notification', methods=['POST', 'GET'])
def notification():
    print("*** notification ")
    if request.method == 'POST':
        notification = Notification()
        notification.message = request.form['message']
        notification.subject = request.form['subject']
        notification.status = 'Notifications submitted'
        notification.submitted_date = datetime.utcnow()

        try:
            db.session.add(notification)
            db.session.commit()

            ##################################################
            ## TODO: Refactor This logic into an Azure Function
            ## Code below will be replaced by a message queue
            #################################################
            #attendees = Attendee.query.all()

            #for attendee in attendees:
             #   subject = '{}: {}'.format(attendee.first_name, notification.subject)
              #  send_email(attendee.email, subject, notification.message)
            print("*** after send mail ")
            #notification.completed_date = datetime.utcnow()
            #notification.status = 'Notified {} attendees'.format(len(attendees))
            db.session.commit()
            # TODO Call servicebus queue_client to enqueue notification ID
           
            sb = ServiceBusClient.from_connection_string(app.config.get(SERVICE_BUS_CONNECTION_STRING))
            queue_client = sb.get_queue(SERVICE_BUS_QUEUE_NAME)
            
            notifId = notification.id
            msg = Message(notifId)
            queue_client.send(msg)
            
            
            print ("before sb client")


 
            print ("after sb client")
            #################################################
            ## END of TODO
            #################################################

            return redirect('/Notifications')
        except :
            logging.error('log unable to save notification')

    else:
        return render_template('notification.html')




def send_email(email, subject, body):
    print("*** send email")
    if not app.config.get('SENDGRID_API_KEY'):
        message = Mail(
            from_email=app.config.get('ADMIN_EMAIL_ADDRESS'),
            to_emails=email,
            subject=subject,
            plain_text_content=body)

        sg = SendGridAPIClient(app.config.get('SENDGRID_API_KEY'))
        sg.send(message)
