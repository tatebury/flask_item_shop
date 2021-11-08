from app import db as main
from flask import render_template, request, flash, redirect, make_response, g
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


@main.route('/market', methods=['GET'])
@login_required
def market():
    all_items = Item.query.all()
    items = [item.to_dict() for item in all_items]
    return render_template('market.html.j2', items=items)

@main.route('/create_item', methods=['GET', 'POST'])
@login_required
def create_item():
    if current_user.is_admin==False:
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
def edit_item(id):
    form = ItemEditingForm()
    if request.method == 'POST' and form.validate_on_submit():
        altered_item_data = {
            "name":form.name.data,
            "price":form.price.data,
            "img":form.img.data,
            "description":form.description.data,
        }
        item=Item.query.get(id)
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
def delete_item(id):
    if request.method == 'POST':
        item_to_delete = Item.query.get(id)
        item_to_delete.delete()
        flash(f'Item #{id} was deleted')
        return redirect(url_for('main.market'))
    
@main.route('/add_item/<int:id>', methods=['GET','POST'])
def add_item(id):
    if request.method == 'POST':
        item_to_add = Item.query.get(id)
        item_to_add.add_to_cart(user=current_user)
        flash(f'{item_to_add.name} was added to your cart')
        return redirect(url_for('main.market'))



# @main.route('/makeanadminplease/<int:id>', methods=['GET', 'POST'])
# @login_required
# def makeanadminplease(id):
    
#     current_user.make_self_admin()
#     return render_template('index.html.j2')


# # Look up a specific item by its id
# @main.get("/item")
# @token_auth.login_required()
# def get_item():
#     id = request.get_json().get('id')
#     if not id:
#         return make_response("Invalid Payload",400)
#     item = Item.query.get(id)
#     if item is None:
#         return make_response("Invalid item id", 400)
#     return make_response(item.to_dict(),200)

# ## Look up all Items
# @main.get("/all_items")
# @token_auth.login_required()
# def get_all_items():
#     all_items = Item.query.all()
#     items = [item.to_dict() for item in all_items]
#     return make_response({"items":items},200)


# # This will create a new ITEM
#     # name   # description   # price   # img 
# @main.post("/item")
# @token_auth.login_required()
# def post_item():
#     if not g.current_user.is_admin:
#         return make_response("You Are not Admin",403)
#     item_dict = request.get_json()
#     if not all(key in item_dict for key in ('name','description','price')):
#         return make_response("Invalid Payload",400)
#     item = Item(**item_dict)
#     item.save()
#     return make_response(f"Item {item.name} was created with the id {item.id}",201)

# # This will alter the item by looking up from its id
# @main.patch("/item")
# @token_auth.login_required()
# def patch_item():
#     if not g.current_user.is_admin:
#         return make_response("You Are not Admin",403)
#     item_dict = request.get_json()
#     if not item_dict.get('id'):
#         return make_response("Invalid Payload",400)
#     item = Item.query.get(item_dict['id'])
#     item.from_dict(item_dict)
#     item.save()
#     return make_response(f'Item {item.id} was edited', 200)

# # This will delete an Item by its id
# @main.delete("/item")
# @token_auth.login_required()
# def delete_item():
#     if not g.current_user.is_admin:
#         return make_response("You Are not Admin",403)
#     id = request.get_json().get('id')
#     if not id:
#         return make_response("Invalid Payload",400)
#     item_to_delete = Item.query.get(id)
#     if item_to_delete is None:
#         return make_response("Invalid item id", 400)
#     item_to_delete.delete()
#     return make_response(f"Item id {id} has been deleted")