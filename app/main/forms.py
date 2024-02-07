from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField

class SearchForm(FlaskForm):
    CATEGORIES = [
        (None,'Search Category'),
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
    title = StringField('Title', render_kw={"placeholder": "Search Title"})
    category = SelectField('Categories', choices = CATEGORIES)
    submit = SubmitField('Search Item')