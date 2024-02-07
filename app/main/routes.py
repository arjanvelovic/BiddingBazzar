from flask import render_template, request, Blueprint, redirect, url_for, current_app
from models import Item
from app.main.forms import SearchForm

main = Blueprint('main', __name__)

@main.route("/", methods=['GET', 'POST'])
@main.route("/home", methods=['GET', 'POST'])
def home():
    page = request.args.get('page', 1, type=int)
    form = SearchForm()
    if form.validate_on_submit():
        title = form.title.data
        category = form.category.data

        if title == '' and category == 'None':
            items = Item.query.order_by(Item.enddate.desc()).paginate(page=page, per_page=10)
        elif title == '' and category != 'None':
            items = Item.query.filter_by(category=category).order_by(Item.enddate.desc()).paginate(page=page, per_page=10)
        elif title != '' and category == 'None':
            items = Item.query.filter(Item.title.contains(title)).order_by(Item.enddate.desc()).paginate(page=page, per_page=10)
        else:
            items = Item.query.filter(Item.title.contains(title)).filter_by(category=category).order_by(Item.enddate.desc()).paginate(page=page, per_page=10)

        return render_template('home.html', form=form, items = items)

    elif request.method == 'GET':

        items = Item.query.order_by(Item.enddate.desc()).paginate(page=page, per_page=10)
    
        return render_template('home.html', form=form, items = items)