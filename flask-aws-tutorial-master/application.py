'''
Simple Flask application to test deployment to Amazon Web Services
Uses Elastic Beanstalk and RDS

Author: Scott Rodkey - rodkeyscott@gmail.com

Step-by-step tutorial: https://medium.com/@rodkey/deploying-a-flask-application-on-aws-a72daba6bb80
'''

from flask import Flask, render_template, request
from application import db
from application.models import User
from application.forms import EnterDBInfo, RetrieveDBInfo

# Elastic Beanstalk initalization
application = Flask(__name__)
application.debug=True
# change this to your own value
application.secret_key = 'cC1YCIWOj9GgWspgNEo2'   

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
        except:
            db.session.rollback()
        return render_template('login.html', studentid=form1.dbNotes.data)
        
    if request.method == 'POST' and form2.validate():
        try:   
            userid = str(form2.userid.data)
            password = str(form2.pw.data)
            query_db = User.query.filter(User.User_id.in_([userid]),User.Pw.in_([password]))
            result =query_db.first()
            if result:
                print "login successfully"
                print result
                return render_template('login.html',studentid =userid)
            else:
                print "login failed"
                return render_template('login_failed.html',studentid =userid)
            db.session.close()
        except:
            db.session.rollback()      

    return render_template('index.html', form1=form1, form2=form2)

if __name__ == '__main__':
    application.run(host='0.0.0.0')
