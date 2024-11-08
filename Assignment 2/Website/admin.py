from flask import Blueprint
from . import db
from .models import Product, Category
from sqlalchemy.exc import SQLAlchemyError

bp = Blueprint('admin', __name__, url_prefix='/admin')

@bp.route('/dbseed/')
def dbseed():
    p1 = Product(category_id=1, name='Lebron James Swingman Jersey', price=125.00, description="When you want that step closer to a genuine NBA garment you can't go wrong with this. Constructed with superb care and quality materials this is an excellent facsimile of the players' own alternate kit.", image='lebron-jersey.jpg')
    p2 = Product(category_id=1, name='Stephen Curry Swingman Jersey', price=110.00, description="Get a real professional feel with this excellent reproduction item. Made from performance-grade material and fashioned after your favourite team's strip you'll look and feel the part every time you wear it!", image='curry-jersey.jpg')
    p3 = Product(category_id=1, name='Kevin Durant Swingman Jersey', price=150.00, description="Go for a different but no less authentic look. This jersey boasts exceptional design and build quality for the ultimate in basketball clothing.", image='durant-jersey.jpg')
    p4 = Product(category_id=2, name='Celtics 2024 Championship Cap', price=50.00, description="Show your pride in the Boston Celtics taking home the 2024 NBA Championship with this iconic 9FIFTY cap. Featuring 3D graphics proclaiming the team's victory and a classic silhouette synonymous with the 9FIFTY design it's the perfect tribute to the Celtics' victory that no fan should be without this season.", image='celtichat.jpg')
    p5 = Product(category_id=2, name='Lakers Cap', price=40.00, description="For real street style you can't beat this. Branded with your team's details you can wear this day or night, rain or shine, and carry a torch for the team you love anywhere you go.", image='lakerscap.png')
    c1 = Category(id=1, name='Jerseys', image = 'jerseys.png')
    c2 = Category(id=2, name='Caps', image = 'caps.png')

    try:
        db.session.add_all([p1, p2, p3, p4, p5, c1, c2])
        db.session.commit()
    except:
        return 'There was an issue adding the products and categories in dbseed function'

    return 'DATA LOADED'
