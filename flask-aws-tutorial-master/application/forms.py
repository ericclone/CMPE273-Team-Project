from flask.ext.wtf import Form
from wtforms import TextField, validators,ValidationError

def id_validator(form,field):
    	checkid = field.data
    	valid_chars ='0123456789'
    	chars =list(checkid)
    	for char in chars:
    		if char not in valid_chars:
    			raise ValidationError('Invalid SJSU ID')

class EnterDBInfo(Form):
    dbNotes = TextField(label='Items to add to DB', description="db_enter", validators=[validators.required(), id_validator]) 
    dbNotes2 = TextField(label='Items to add to DB', description="db_enter", validators=[validators.required(), validators.Length(min=0, max=128, message=u'Enter 128 characters or less')]) 
    dbNotes4 = TextField(label='Email Address', description="db_enter", validators=[validators.required(), validators.Email()])   
    dbNotes3 = TextField(label ='New Password',validators =[validators.required(),validators.EqualTo('confirm',message ='Passwords must match')])
    confirm = TextField(label ='Repeat Password',validators =[validators.required()])  

    
             

class RetrieveDBInfo(Form):
    userid = TextField(label='Items to add to DB', description="db_get", validators=[validators.required(), id_validator]) 
    pw = TextField(label ='Password', description ="db_get", validators =[validators.required()]) 
