from flask import Flask, render_template, request, session, redirect, url_for
from application import db
from application.models import User
from application.models import Pre_req
from application.forms import EnterDBInfo, RetrieveDBInfo
import base64
import time
import os
from knn import knnTest

application = Flask(__name__)
application.secret_key = 'cC1YCIWOj9GgWspgNEo2'

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

        redirect(url_for('process_upload'))
        
    if request.method == 'POST' and form2.validate():
        try:   
            userid = str(form2.userid.data)
            password = str(form2.pw.data)
            query_db = User.query.filter(User.User_id.in_([userid]),User.Pw.in_([password]))
            result =query_db.first()

            if result:
                print "login successfully"
                session['userid']=userid
                redirect(url_for('process_upload'))
            else:
                print "login failed"
                return render_template('login_failed.html',studentid =userid)
            db.session.close()
        except:
            db.session.rollback()

    return render_template('index.html', form1=form1, form2=form2)

'''
mock image for test
'''
@application.route('/extension')
def extension():
    return render_template('extension.html')

@application.route('/upload', methods=['GET', 'POST'])
def process_upload():
    transcript_image = ''
    if 'transcript_image' in session:
        transcript_image = session['transcript_image']
        print "process_upload() --> session transcript_image = " + transcript_image
    else:
        #The user are from extension
        transcript_image = request.form.get('transcript_image')
        if transcript_image != None:
            print "process_upload() --> request transcript_image = " + transcript_image
    
    #If the user has already logged in
    session_userid = session['userid']
    if session_userid != None:
        # process the image with openCV
        file_name = getImage(transcript_image)
        session['taken_course_list'] = knnTest(trainSetDir, file_name)
        
        #remove file
        #os.remove(file_name) 

        # Query course list 
        query_db2 = None
        try:
            query_db2 = Pre_req.query.order_by(Pre_req.Pre_id.desc()).limit(10)
            db.session.close()
        except:
            db.session.rollback()

        return render_template('login.html', studentid=session_userid,courseinfo = query_db2) 
    #The user are from extension and hasn't log in yet.
    #Save the image in session and go to login
    else:
        session['transcript_image'] = transcript_image
        return redirect(url_for('index'))
    
    return 'OK'

@application.route('/check')
def check_result():
    #Get checked_box_list(ex: 273, 275), the courses the student wants to take 
    checked_box_list = ['273', '275'] # mock data
    # the check result of every desired course. Ex:{'273':True, '275':'False'}
    check_result = {} 
    for desired_course in checked_box_list:
        #Query table Pre_req and find pre_list of desired_course
        pre_of_desired_course = ['202', '208']  # mock dada
        result = check_course_pre(session['taken_course_list'], pre_of_desired_course)
        check_result[desired_course] = result
    
    #Save result into DB    TODO

    #Send mail    TODO

    return "page" #TODO


def check_course_pre(taken_course_list, pre_list):
    pre_amout = sizeof(pre_list)
    count = 0
    for pre in pre_list:
        if pre in taken_course_list:
            count += 1
    #the student has taken all the pre of this course
    if count == pre_amout:
        return True
    else:
        return False
        
def getImage(transcript_image):
    transcript_image = transcript_image.replace('data:image/png;base64,', '')
    transcript_image = transcript_image.replace(' ', '+')
    image = transcript_image.decode('base64')
    print "#########: "+image
    millis = str(int(round(time.time() * 1000)))
    file_name = 'C:/test' + millis + '.png' #TODO use linux path
    f = None
    try:
        f = open(file_name, 'wb')
        f.write(image)
        f.close()
    except:
        if f != None:
            f.close()
    return file_name


if __name__ == "__main__":
    application.run(host='0.0.0.0')