#How we launch the website - creates the app and turns the whole 'Website' folder into a package
from Website import create_app, db

app=create_app()

if __name__=='__main__':
    app.run(debug=True)
    