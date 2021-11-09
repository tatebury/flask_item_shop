from app import db as main
from flask import render_template, request, flash, redirect, make_response, g
from werkzeug.datastructures import MultiDict
from app.blueprints.auth.auth import token_auth
from flask.helpers import url_for
import requests
from app.models import User, Item
from . forms import ItemCreationForm, ItemEditingForm
from flask_login import login_required, current_user
from .import bp as main

@main.route('/', methods=['GET'])
@login_required
def index():
    
    return render_template('index.html.j2')


@main.route('/market', methods=['GET', 'POST'])
@login_required
def market():
    all_items = Item.query.all()
    items = [item.to_dict() for item in all_items]
    cart_total = 0
    for item in Item.query.filter_by(owner=current_user.id):
        cart_total += int(item.price)
    return render_template('market.html.j2', items=items, cart_total=cart_total)

@main.route('/create_item', methods=['GET', 'POST'])
@login_required
def create_item():
    if current_user.is_admin!=True:
        return redirect(url_for('main.market'))
    form = ItemCreationForm()
    if request.method == 'POST' and form.validate_on_submit():
        try:
            new_item_data = {
                "name":form.name.data,
                "price":form.price.data,
                "img":form.img.data,
                "description":form.description.data,
            }
            #create and empty item
            new_item_object = Item()
            # build item with form data
            new_item_object.from_dict(new_item_data)
            # save item to database
            new_item_object.save()
        except:
            error_string = "There was an unexpected Error creating the item. Please Try again."
            flash(error_string)
            return render_template('create_item.html.j2',form=form, error = error_string)
        return redirect(url_for('main.market'))
    return render_template('create_item.html.j2', form = form)

@main.route('/edit_item/<int:id>', methods=['GET','POST'])
@login_required
def edit_item(id):
    if current_user.is_admin!=True:
        return redirect(url_for('main.market'))
    item=Item.query.get(id)
    if request.method == 'GET':
        form = ItemEditingForm(formdata=MultiDict({'name': item.name, 
                                                   'price': item.price, 
                                                   'img': item.img,
                                                   'description': item.description}))
    else:
        form = ItemEditingForm()
    if request.method == 'POST' and form.validate_on_submit():
        altered_item_data = {
            "name":form.name.data,
            "price":form.price.data,
            "img":form.img.data,
            "description":form.description.data,
        }
        
        try:
            item.from_dict(altered_item_data)
            item.save()
            flash('item edited', 'success')
        except:
            flash('There was an unexpected error', 'danger')
            return redirect(url_for('main.edit_item'))
        return redirect(url_for('main.market'))
    return render_template('edit_item.html.j2', form = form)

@main.route('/delete_item/<int:id>', methods=['GET','POST'])
@login_required
def delete_item(id):
    if current_user.is_admin!=True:
        return redirect(url_for('main.market'))
    if request.method == 'POST':
        item_to_delete = Item.query.get(id)
        item_to_delete.delete()
        flash(f'Item #{id} was deleted')
        return redirect(url_for('main.market'))
    
@main.route('/add_item/<int:id>', methods=['GET','POST'])
@login_required
def add_item(id):
    if request.method == 'POST':
        item_to_add = Item.query.get(id)
        item_to_add.add_to_cart(user=current_user)
        flash(f'{item_to_add.name} was added to your cart')
        return redirect(url_for('main.market'))

@main.route('/remove_item/<int:id>', methods=['GET','POST'])
@login_required
def remove_item(id):
    if request.method == 'POST':
        item_to_remove = Item.query.get(id)
        item_to_remove.remove_from_cart()
        flash(f'{item_to_remove.name} was removed to your cart')
        return redirect(url_for('main.market'))
    
@main.route('/show_item/<int:id>', methods=['GET','POST'])
@login_required
def show_item(id):
    if request.method == 'POST':
        item_to_show = Item.query.get(id)
        return render_template('show_item.html.j2', item = item_to_show)

@main.route('/empty_cart', methods=['GET', 'POST'])
@login_required
def empty_cart():
    for item in Item.query.filter_by(owner=current_user.id):
        item.remove_from_cart()
    return redirect(url_for('main.market'))

