# CMPE273-Team-Project
```python

@app.route('/upload', Method="POST")
def process_upload():
    file = session.get('ihateyou', None)
    if file is None:
        file = request.form['file']

    if logged_in():
        # process the image with openCV
        session['class_list'] = list from opencv
        return result # view
    else:
        session['ihateyou'] = file
        return redirect_login

@app.route('/login')
def login():
    file = session.get('ihateyou', None)
    # process login as normal

    if file is None:
        return "manual_upload" # another view
    else:
        return "upload"

def logged_in():
    return db.check(username) = "OK" and db.check(password) = "OK"


```
~~AWS EC2 ip: ec2-54-183-11-0.us-west-1.compute.amazonaws.com~~ (ran out of credit)
