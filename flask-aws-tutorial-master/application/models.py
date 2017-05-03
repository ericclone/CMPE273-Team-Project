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
