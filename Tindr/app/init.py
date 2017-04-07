#import all files and tools needed
#yeah start with flask
#@params: Author( martins )
import imaplib
from flask import Flask,url_for,render_template,request
from flask_mail import Mail, Message
from ach import password
#now instantiate every thing needed
app=Flask(__name__)
app.secret_key='$_$pecctrums$_$'

#instantiate flaskMail
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = "email address"
app.config['MAIL_PASSWORD'] = password()
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

#instantiate imap
mailCheck = imaplib.IMAP4_SSL('imap.gmail.com')
mailCheck.login(app.config['MAIL_USERNAME'],app.config['MAIL_PASSWORD'])
mailCheck.list()
mailCheck.select('inbox')

@app.route("/loadMails")
def loadMails():
	result=""	
	typ, data = mailCheck.search(None, 'ALL')
	for num in data[0].split():
		typ, data = mailCheck.fetch(num, '(RFC822)')
		msg = email.message_from_string(data[0][1])
		result+=num
		result+=msg['Subject']
		result+="</br>"
		# return 'Message %s: %s' % (num, msg['Subject'])
		# return 'Message %s\n%s\n' % (num, data[0][1])
	return result
	mailCheck.close()
	mailCheck.logout()

@app.route("/createLabel/<mail>/")
def createMailBox(mail):
	mailCheck.create(mail)
	return "Label created successfully"


@app.route("/deleteLabel/<mail>/")
def deleteMailBox(mail):
	mailCheck.delete(mail)
	return "Label deleted successfully"

# print 
mail = Mail(app)


@app.route("/")
def home():
	return render_template("index.html")

@app.route("/mail",methods=['POST'])
def mails():
	if request.method=='POST':
		emailTo= request.form["emailTo"]
		msg= request.form["msg"]
		return send_mail_flask(emailTo,msg)


#send Message
def send_mail_flask(to,msgs):
	To=to.split(",")
	print To
	msg = Message('test',sender='joemartiny1@gmail.com', recipients=To)#use the message class to send the message
	# msg.body=msgs
	msg.html=render_template("mail.html")
	# msg.html=render_template('template.html')
	mail.send(msg)
	return "Sent"

if __name__ == '__main__':
	app.run(port=7070,debug=True)
