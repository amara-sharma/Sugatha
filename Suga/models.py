from Suga import db,app,login
from datetime import datetime
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as ser

@login.user_loader
def user_loader(id):
    return FoodGetters.query.get(int(id))


class FoodDonors(db.Model,UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(20),nullable=False)
    contactno=db.Column(db.String(20),nullable=False)
    city=db.Column(db.String(120),nullable=False)
    address=db.Column(db.String(60),nullable=False)
    email=db.Column(db.String(20),nullable=False)
    tfood=db.Column(db.String(20),nullable=False)
    date=db.Column(db.DateTime,default=datetime.utcnow)
    taken=db.Column(db.String(20),default="False")
    def __repr__(self):
        return f"FoodDonors('{self.id}','{self.name}','{self.contactno}','{self.email}','{self.city}','{self.address}','{self.date}','{self.taken}','{self.tfood}')"

class FoodGetters(db.Model,UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(20),nullable=False)
    year=db.Column(db.String(20),nullable=False)
    city=db.Column(db.String(20),nullable=False)
    email=db.Column(db.String(20),nullable=False,unique=True)
    password=db.Column(db.String(20),nullable=False)
    mobileno=db.Column(db.String(20),nullable=False)
    address=db.Column(db.String(20),nullable=False)
    pic=db.Column(db.String(20),nullable=False)
    takenfoodid=db.Column(db.String(50))
    volunteer=db.Column(db.String(20),default="False")
    count=db.Column(db.Integer,default=0)
    date=db.Column(db.DateTime,default=datetime.utcnow)
    def __repr__(self):
        return f"FoodGetters('{self.id}','{self.name}','{self.email}','{self.city}','{self.pic}','{self.mobileno}','{self.volunteer}','{self.count}')"

    def set_idtoken(self,expire_sec=1800):
        s=ser(app.config['SECRET_KEY'],1800)
        return s.dumps({'user_id':self.id}).decode('utf-8')
    
    @staticmethod
    def verify_token(token):
        s=ser(app.config['SECRET_KEY'])
        try:
            user_id=s.loads(token)['user_id']
        except:
            return None
        return FoodGetters.query.get(user_id)
class notifyme(db.Model,UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    foodid=db.Column(db.Integer)
    userid=db.Column(db.String(20))
    def __repr__(self):
       return f"notifyme('{self.foodid}','{self.userid}')"
