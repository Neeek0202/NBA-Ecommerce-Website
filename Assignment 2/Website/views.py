from flask import Blueprint, render_template, url_for, request, session, flash, redirect
from .models import Product, Category, Order
from .forms import CheckoutForm
from . import db

bp = Blueprint('main', __name__)

# Home function 

@bp.route('/')
def home():
    categories = Category.query.order_by(Category.name).all()
    return render_template('home.html', categories=categories)

# This is the product page, autogenerates products based on Category ID
@bp.route('/category/<int:categoryid>/')
def category_products(categoryid):
    products = Product.query.filter_by(category_id=categoryid).all()
    return render_template('products.html', categoryid=categoryid, products=products)

@bp.route('/product/<int:id>')
def productdetail(id):
    product = Product.query.get_or_404(id)
    return render_template('productdetail.html', product=product)


# Search function - search bar is present on all pages, uses a query.filter like function to search through the names of the products 
@bp.route('/search')
def search():
    query = request.args.get('q')
    if query:
        search = f"%{query}%"
        products = Product.query.filter(Product.name.like(search)).all()
    else:
        products = []
    return render_template('search.html', products=products)

# Referred to as "Cart" to the user
@bp.route('/order', methods=['POST','GET'])
def order():
    product_id = request.values.get('product_id')
    # retrieve order if there is one 
    if 'order_id'in session.keys(): 
        order = Order.query.get(session['order_id'])
    else:
        order = None
    # create new order if needed 
    if order is None:
        order = Order(status = False, firstname='', surname='', email='', phone='', totalcost=0) # create new order if needed
        try:
            db.session.add(order)
            db.session.commit()
            session['order_id'] = order.id
        except:
            print('failed at creating a new order')
            order = None

# Calculate total price of cart and displays 
    totalprice = 0 
    if order is not None:
        for product in order.products:
            totalprice = totalprice + product.price
    
    if product_id is not None and order is not None:
        product = Product.query.get(product_id)
        if product not in order.products:
            try:
                order.products.append(product)
                db.session.commit()
            except:
                return 'Sorry, there was an issue adding the item to your cart. Please try again!'
            return redirect(url_for('main.order'))
        else:
            flash('This item is already in cart!')
            return redirect(url_for('main.order'))
    return render_template('order.html', order = order, totalprice = totalprice)

# Function to delete item 
@bp.route('/deleteorderitem', methods=['POST']) # Delete specific cart items
def deleteorderitem():
    id=request.form['id']
    if 'order_id' in session:
        order = Order.query.get_or_404(session['order_id'])
        product_to_delete = Product.query.get(id)
        try:
            order.products.remove(product_to_delete)
            db.session.commit()
            return redirect(url_for('main.order'))
        except:
            return 'Problem deleting item from order'
    return redirect(url_for('main.order'))

# Function to remove all from cart
@bp.route('/deleteorder') 
def deleteorder():
    if 'order_id' in session:
        del session['order_id']
        flash('All items deleted')
    return redirect(url_for('main.home'))

# Checkout function - uses WTForms to validate email 
@bp.route('/checkout', methods=['POST','GET'])
def checkout():
    form = CheckoutForm() 
    if 'order_id' in session:
        order = Order.query.get_or_404(session['order_id'])
       
        if form.validate_on_submit():
            order.status = True
            order.firstname = form.firstname.data
            order.surname = form.surname.data
            order.email = form.email.data
            order.phone = form.phone.data
            totalcost = 0
            for product in order.products:
                totalcost = totalcost + product.price
            order.totalcost = totalcost
            try:
                db.session.commit()
                del session['order_id']
                flash('Thank you for your order, you will be contacted via email soon...')
                return redirect(url_for('main.home'))
            except:
                return 'Hm...There was an issue completing your order..'
    return render_template('checkout.html', form = form)
