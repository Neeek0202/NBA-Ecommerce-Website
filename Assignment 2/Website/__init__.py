from flask import Flask, render_template #Import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy() # Initialize the SQLAlchemy instance

# Function that creates the web application 
def create_app(): 
    app = Flask(__name__) # name of the module/package that is calling this app 
    app.debug = True
    app.secret_key = 'Website420'

    # set the app configuration data 
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sqldatabase.db'

    # initialize db with flask app
    db.init_app(app)

    bootstrap = Bootstrap(app)

    # add the Blueprint
    from . import views
    app.register_blueprint(views.bp)

    #from . import admin
    #app.register_blueprint(admin.bp)

    # inbuilt function that takes error as parameters
    @app.errorhandler(404)
    def not_found(e):
        return render_template("404.html")

    @app.errorhandler(500)
    def internal_error(e):
        return render_template("500.html")

    return app
