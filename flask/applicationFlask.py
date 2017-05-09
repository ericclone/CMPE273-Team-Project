from flask import Flask, render_template, request, session, redirect, url_for
from application import db
from application.models import *
from application.forms import EnterDBInfo, RetrieveDBInfo
import base64
import time
import os
from knn import knnTest
from flask_mail import Mail,  Message
#from flask_mysqldb import MySQL

import traceback

application = Flask(__name__)
# application.secret_key = 'cC1YCIWOj9GgWspgNEo2'
application.secret_key = os.urandom(32)

application.config.update(
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = 465,
    MAIL_USE_SSL = True,
    MAIL_USERNAME = 'sjsu.cmpe273.test@gmail.com',
    MAIL_PASSWORD = 'sjsu1234',
    MYSQL_USER = 'flask',
    MYSQL_PASSWORD = '12345678',
    MYSQL_DB = 'flaskdb',
    MYSQL_HOST = 'flasktest.cmjjsvadtatr.us-west-2.rds.amazonaws.com'
)
mail = Mail(application)
# mysql = MySQL(application)

'''
Log in and sign up page form submit
If log in, verify user.
If sign up, insert user into DB.
'''
@application.route('/', methods=['GET', 'POST'])
@application.route('/index', methods=['GET', 'POST'])
def index():
    
    form1 = EnterDBInfo(request.form)
    form2 = RetrieveDBInfo(request.form)

    if request.method == 'POST' and form1.validate():
        data_entered = User(User_id=form1.dbNotes.data,Name=form1.dbNotes2.data,Type ='Student',Pw =form1.dbNotes3.data,Email = form1.dbNotes4.data)
        
        try:     
            db.session.add(data_entered)
            db.session.commit()
            db.session.close()
            session['userid']=form1.dbNotes.data
        except:
            db.session.rollback()

        return redirect(url_for('process_upload'))
        
    if request.method == 'POST' and form2.validate():
        try:   
            userid = str(form2.userid.data)
            password = str(form2.pw.data)
            query_db = User.query.filter(User.User_id.in_([userid]),User.Pw.in_([password]))
            result =query_db.first()

            if result:
                print "login successfully"
                session['userid']=userid
                return redirect(url_for('process_upload'))
            else:
                print "login failed"
                return render_template('login_failed.html',studentid =userid)
            db.session.close()
        except:
            db.session.rollback()

    print "Nothing worked"
    return render_template('index.html', form1=form1, form2=form2)

'''
mock image for test
'''
@application.route('/extension')
def extension():
    return render_template('extension.html')

def getPrereq(desired_course):
    statement = 'SELECT Pre_course FROM Pre_req WHERE Course = %s' % desired_course
    if desired_course is None:
        statement = 'SELECT Pre_course FROM Pre_req'
    result = db.engine.execute(statement)
    result_list = []
    for row in result:
        if row['Pre_course'] != 'None':
            result_list.append(row['Pre_course'])
    return set(result_list)

@application.route('/upload', methods=['GET', 'POST'])
def process_upload():
    transcript_image = None
    image_file_name = 'no_file'
    
    if 'image_file_name' in session:
        image_file_name = session['image_file_name']
        print "process_upload() --> image_file_name = " + image_file_name
    else:
        #The user are from extension
        transcript_image = request.form.get('transcript_image', None)
        if transcript_image is not None:
            print "process_upload() --> request transcript_image = "# + transcript_image
        else:
            print "transcript_image is None"
    # print "before checking username ", len(transcript_image)
    #If the user has already logged in
    session_userid = session.get('userid', None)
    if session_userid is not None:
        # process the image with openCV
        trainSetDir = trainSetDir = "../myChainSet"
        courseList = getPrereq(None)
        session['taken_course_list'] = knnTest(trainSetDir, image_file_name, courseList)
        print session['taken_course_list']
        
        # remove file
        # os.remove(image_file_name) 

        # Query course list 
        query_db2 = None
        try:
            query_db2 = Pre_req.query.order_by(Pre_req.Pre_id.desc())
            db.session.close()
        except:
            db.session.rollback()

        return render_template('login.html', studentid=session_userid,courseinfo = query_db2) 
    #The user are from extension and hasn't log in yet.
    #Save the image in file system and save file name in session and then go to login
    else:
       
        imgFileName = getImage(transcript_image)
        session['image_file_name'] = imgFileName
        print "image file name : ", imgFileName
        return redirect(url_for('index'))
    
    return 'OK'

@application.route('/check', methods=['GET', 'POST'])
def check_result():
    #Get checked_box_list(ex: 273, 275), the courses the student wants to take 
    if request.method =='POST':
        course_check = request.form['result'];
    checked_box_list = course_check.split(",");

    # checked_box_list = ['273', '275'] # mock data
    # the check result of every desired course. Ex:{'273':True, '275':'False'}
    check_result = {} 
    for desired_course in checked_box_list:
        #Query table Pre_req and find pre_list of desired_course
        result = check_course_pre(session['taken_course_list'], desired_course)
        course_enter = Pre_student(User_id=session['userid'],Course =desired_course,Status=result)
          
        try:     
           db.session.add(course_enter)
           db.session.commit()        
           db.session.close()
        except:
           db.session.rollback()

    
        check_result[desired_course] = result
    
   
    return render_template('confirmation.html', course_result = check_result)

@application.route("/send_mail", methods=['GET', 'POST'])
def send_mail():
    email = "hq1992518@gmail.com"
    msg = mail.send_message(
        'Hello',
        sender='sjsu.cmpe273.test@gmail.com',
        recipients=[email],
        body="Testing"
    )
    return email

@application.route("/confirmation", methods=['GET', 'POST'])
def confirmation():
    '''
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * from flaskdb.Pre_student")
    data = cursor.fetchall()
    #return str(data)
    '''
    test = "CMPE273"
    return render_template('confirmation.html', test = test)    

def check_course_pre(taken_course_list, desired_course):
    pre_set = getPrereq(desired_course)
    for pre in pre_set:
        if pre not in taken_course_list:
            return 'n'
    return 'y'
        
def getImage(transcript_image):
    transcript_image = transcript_image.replace('data:image/png;base64,', '')
    transcript_image = transcript_image.replace(' ', '+')
    image = transcript_image.decode('base64')
    # print "#########: " + image
    millis = str(int(round(time.time() * 1000)))
    file_name = 'temp/' + millis + '.png' #TODO use linux path
    f = None
    try:
        f = open(file_name, 'wb')
        print "Saving file ", file_name, f.write(image)
        f.close()
    except Exception as e:
        if f != None:
            f.close()
        traceback.print_exc()
    return file_name


if __name__ == "__main__":
    application.run(debug = True, host='0.0.0.0')
