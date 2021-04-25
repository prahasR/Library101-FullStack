from web_App import app, db

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
    #db.create_all()
