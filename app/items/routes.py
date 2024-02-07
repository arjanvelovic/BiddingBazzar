from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from flask_login import current_user, login_required
from app import db
from models import Item, Bid, Watchlist
from app.items.forms import ItemForm, BidForm, WatchlistForm
from wtforms.validators import  NumberRange
from datetime import datetime, timedelta
from app.items.utils import save_picture

items = Blueprint('items', __name__)

@items.route("/item/new", methods=['GET', 'POST'])
@login_required
def new_item():
    form = ItemForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
        else:
            picture_file = 'default2.jpg'
        item = Item(title=form.title.data, description=form.description.data, category=form.category.data, image_file=picture_file, price=form.price.data, author=current_user, enddate=datetime.utcnow() + timedelta(days=7) - timedelta(hours=5))
        db.session.add(item)
        db.session.commit()
        flash('Your listing is live!', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_item.html', title='List Item',
                           form=form, legend='List Item')

@items.route("/item/<int:item_id>", methods=['GET', 'POST'])
def item(item_id):
    item = Item.query.get_or_404(item_id)

    bidform = BidForm()
    watchlistform = WatchlistForm()
    bidform.bidvalue.validators = [NumberRange(min=item.price+1, message='You must beat the current bid by atleast $1.00')]

    if current_user.is_authenticated:
        if bidform.validate_on_submit():
            if Bid.query.filter_by(item_id=item_id).all():
                bid = Bid.query.filter_by(item_id=item_id).first()
                bid.bidvalue = bidform.bidvalue.data
                bid.user_id = current_user.id
                bid.bidtime = datetime.utcnow()
            else:
                bid = Bid(bidvalue=bidform.bidvalue.data, item_id=item_id, user_id=current_user.id)
                item.hasbuyer = True
                db.session.add(bid)
            
            item.price = bidform.bidvalue.data
            db.session.commit()
            flash('You have the highest bid!', 'success')
            return redirect(url_for('items.item', item_id=item.id))
        
        watchlistform.watching.data = Watchlist.query.filter_by(item_id=item_id, user_id=current_user.id).all()

        if watchlistform.validate_on_submit():
            if watchlistform.watching.raw_data:
                watchlist = Watchlist(watching = True, item_id=item_id, user_id=current_user.id)
                db.session.add(watchlist)
                flash('Added to Watch List', 'success')
            else:
                watchlist = Watchlist.query.filter_by(item_id=item_id, user_id=current_user.id).first()
                try:
                    db.session.delete(watchlist)
                    flash('Removed from Watch List', 'success')
                except:
                    print("Something went wrong")

            db.session.commit()
            return redirect(url_for('items.item', item_id=item.id))

    return render_template('item.html', title=item.title, item=item, bidform=bidform, watchlistform = watchlistform)

@items.route("/item/<int:item_id>/update", methods=['GET', 'POST'])
@login_required
def update_item(item_id):
    item = Item.query.get_or_404(item_id)
    if item.author != current_user:
        abort(403)
    form = ItemForm()
    if form.validate_on_submit() and item.notactive:
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
        else:
            picture_file = item.image_file
        itemrelist = Item(title=form.title.data, description=form.description.data, category=form.category.data, image_file=picture_file, price=form.price.data, author=current_user, enddate=datetime.utcnow() + timedelta(days=7) - timedelta(hours=5))
        db.session.add(itemrelist)
        db.session.commit()
        flash('Your have relisted the item!', 'success')
        return redirect(url_for('main.home'))

    elif form.validate_on_submit() and item.notactive == False:
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
        else:
            picture_file = item.image_file
        item.title = form.title.data
        item.description = form.description.data
        item.category = form.category.data
        item.image_file = picture_file
        item.price = form.price.data
        item.hasbuyer = False
        item.enddate = datetime.utcnow() + timedelta(minutes=10) - timedelta(hours=5)
        db.session.commit()

        flash('Your item has been updated!', 'success')
        return redirect(url_for('items.item', item_id=item.id))
    elif request.method == 'GET':
        form.title.data = item.title
        form.description.data = item.description
        form.category.data = item.category
        form.price.data = item.price
        if item.notactive:
            return render_template('create_item.html', title='Relist Item', form=form, legend='Relist Item')
        else:
            return render_template('create_item.html', title='Update Item', form=form, legend='Update Item')


@items.route("/item/<int:item_id>/delete", methods=['POST'])
@login_required
def delete_item(item_id):
    item = Item.query.get_or_404(item_id)
    if item.author != current_user:
        abort(403)
    db.session.delete(item)
    db.session.commit()
    flash('Your item has been deleted', 'success')
    return redirect(url_for('main.home'))