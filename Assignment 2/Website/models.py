from . import db 

class Product(db.Model):
    __tablename__ = "products"
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=False)
    name = db.Column(db.String(64), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text(500), nullable=False)
    image = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        str = "id: {}, CategoryID {}, Name: {}, Price: {}, Description: {}, Image: {}" 
        str =str.format( self.id, self.category_id,self.name,self.price, self.description, self.image)
        return str

class Category(db.Model):
    __tablename__ = "categories"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    image = db.Column(db.String(60), nullable=False)
    products = db.relationship("Product", backref=db.backref("category")) #establishes one-to-many relationship with the 'Product' model, meaning each category can have multiple products. 
    

    def __repr__(self):
        str = "Id: {}, Name: {}, Image: {}\n"
        str =str.format( self.id, self.name,self.image)
        return str 


orderdetails = db.Table('orderdetails', 
                        db.Column('order_id', db.Integer, db.ForeignKey('orders.id'), nullable=False),
                        db.Column('product_id', db.Integer, db.ForeignKey('products.id'), nullable=False),
                        db.PrimaryKeyConstraint('order_id', 'product_id')) #establishes many to many relationship between 'Order' and 'Product' 


class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Boolean, default=False)
    firstname = db.Column(db.String(64))
    surname = db.Column(db.String(64))
    email = db.Column(db.String(128))
    phone = db.Column(db.String(32))
    totalcost = db.Column(db.Float)
    date = db.Column(db.DateTime)
    products = db.relationship("Product", secondary=orderdetails, backref="orders") #establishes a many to many relationship with 'Product' using orderdetails association table 

    def __repr__(self):
        str = "id: {}, Status: {}, Firstname: {}, Surname: {}, Email: {}, Phone: {}, Date: {}, Products: {}, Total Cost: {}\n"
        str = str.format(self.id, self.status, self.firstname, self.surname, self.email, self.phone, self.date, self.products, self.totalcost, self.size)
        return str
