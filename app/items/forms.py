from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, BooleanField, TextAreaField, SelectField, DecimalField
from wtforms.validators import DataRequired

class ItemForm(FlaskForm):
    CATEGORIES = [
        (None,'--- select a category ---'),
        ('Business & Industrial','Business & Industrial'),
        ('Collectibles','Collectibles'),
        ('Electronics','Electronics'),
        ('Fashion','Fashion'),
        ('Home & Garden','Home & Garden'),
        ('Jewelry','Jewelry'),
        ('Motors','Motors'),
        ('Sporting Goods','Sporting Goods'),
        ('Toys','Toys'),
        ('Other','Other')
    ]
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    price = DecimalField('Starting Price', places = 2, validators=[DataRequired()])
    category = SelectField('Categories', choices = CATEGORIES, validators=[DataRequired()])
    picture = FileField('Upload Item Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('List Item')

class BidForm(FlaskForm):
    bidvalue = DecimalField('Place a Bid', validators=[DataRequired()])
    submit = SubmitField('Place Bid')

class WatchlistForm(FlaskForm):
    watching = BooleanField('Add to Watchlist')
    submit = SubmitField('Watchlist')