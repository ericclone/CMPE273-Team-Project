from application import db

class User(db.Model):
    # id = db.Column(db.Integer, primary_key=True)
    # notes = db.Column(db.String(128), index=True, unique=False)
    __tablename__ = 'User'
    
    User_id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(128), index=True, unique=False)
    Type = db.Column(db.String(128), index=True, unique=False)
    Pw = db.Column(db.String(128), index=True, unique=False)
    Email = db.Column(db.String(128), index=True, unique=False)
    
    def __init__(self, User_id,Name,Type,Pw,Email):
        self.User_id = User_id
        self.Name = Name
        self.Type = Type
        self.Pw = Pw
        self.Email = Email

    def __repr__(self):

        return '<User %r>' % self.Name

class Pre_req(db.Model):
    # id = db.Column(db.Integer, primary_key=True)
    # notes = db.Column(db.String(128), index=True, unique=False)
    __tablename__ = 'Pre_req'
    
    Pre_id = db.Column(db.Integer, primary_key=True)
    Course = db.Column(db.String(128), index=True, unique=False)
    Pre_course = db.Column(db.String(128), index=True, unique=False)
    
    def __init__(self, Pre_id,Course,Pre_course):
        self.Pre_id = Pre_id
        self.Course = Course
        self.Pre_course = Pre_course
       

    def __repr__(self):

        return '<Pre_req %r>' % self.Course
    
class Pre_student(db.Model):
    # id = db.Column(db.Integer, primary_key=True)
    # notes = db.Column(db.String(128), index=True, unique=False)
    __tablename__ = 'Pre_student'
    
    Pres_id = db.Column(db.Integer, primary_key=True)
    User_id = db.Column(db.String(128), index=True, unique=False)
    Course = db.Column(db.String(128), index=True, unique=False)
    Status = db.Column(db.String(128), index=True, unique=False)
    
    def __init__(self, Pres_id,User_id,Course,Status):
        self.Pres_id = Pres_id
        self.User_id = User_id
        self.Course = Course
        self.Status = Status
       

    def __repr__(self):

        return '<Pre_student %r>' % self.Status

