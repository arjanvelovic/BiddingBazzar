from datetime import datetime, timedelta
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from app import db, login_manager, app
from flask_login import UserMixin
from sqlalchemy.ext.hybrid import hybrid_property

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    phonenumber = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    datecreated = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    posts = db.relationship('Item', backref='author', lazy=True)
    bids = db.relationship('Bid', backref='bidder', lazy=True)
    watching = db.relationship('Watchlist', backref='watcher', lazy=True)

    def __repr__(self):
        return f"User{self.id}('{self.firstname}', '{self.email}', '{self.datecreated}')"
    
    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(100), nullable=False)
    image_file = db.Column(db.String(50), nullable=False, default='default2.jpg')
    price = db.Column(db.Numeric, nullable=False)
    seller = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    listeddate = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    enddate = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    hasbuyer = db.Column(db.Boolean, nullable = False, default = False)
    bidinfo = db.relationship('Bid', backref='item', lazy=True)
    watches = db.relationship('Watchlist', backref='item', lazy=True)

    def __repr__(self):
        return f"Itemid:{self.id}('{self.title}', '{self.seller}', '{self.listeddate}', '{self.enddate}', '{self.bidinfo}')"
    
    @hybrid_property
    def notactive(self):
        if datetime.utcnow() - timedelta(hours=5) >= self.enddate:
            return True
        else:
            return False
    
    @notactive.expression
    def notactive(cls):
        if datetime.utcnow() - timedelta(hours=5) >= Item.enddate:
            return True
        else:
            return False

    
class Bid(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bidvalue = db.Column(db.Numeric, nullable=False)
    bidtime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Bidid:{self.id}('{self.bidvalue}', '{self.item_id}', '{self.user_id}')"
    
class Watchlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    watching = db.Column(db.Boolean, nullable=False, default=True)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Watchlistid:{self.id}('{self.watching}', '{self.item_id}', '{self.user_id}')"