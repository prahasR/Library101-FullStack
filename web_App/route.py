from flask import Flask, render_template, url_for, flash, redirect, request
import os
import secrets
from PIL import Image
from web_App import app, db, bcrypt, login_manager
from web_App.forms import RegistrationForm, SelectionForm, LoginForm, Book_regForm, LibLoginForm, UpdateAccountForm,ManageBookForm, PostForm
from web_App.models import User , Post, Librarian, Book, Irequest
from flask_login import login_user, current_user, logout_user, login_required

@app.route("/")
@app.route("/home", methods=['GET', 'POST'])
def home():
    books=Book.query.all()
    form=SelectionForm(request.form)
    new=Book.query.order_by(Book.id.desc()).limit(5)
    search=[]
    #if request.method =='POST':
    #    print(search)
    #    if (form.data['category'] == 'author'):
    #        print("...",search)
    #        search=Book.query.filter_by(writer=form.input_.data).order_by(Book.rating.desc()).all()
    return render_template('all_books.html', books=books, new=new, form=form, search=search)

def save_picture(form_picture, folder):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/'+folder, picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

@app.route("/book/<int:book_id>",  methods=['GET', 'POST'])
def book_page(book_id):
    
    posts = Post.query.filter_by(book_id=book_id).order_by(Post.rating.desc()).all()
    book=Book.query.get_or_404(book_id)
    same_author=Book.query.filter_by(writer=book.writer).order_by(Book.rating.desc()).limit(5)
    same_genre=Book.query.filter_by(genre=book.genre).order_by(Book.rating.desc()).limit(5)
    image_file = url_for('static', filename='book_pics/' + book.img_file)
    form= PostForm()
    form1= SelectionForm()
    form2=Book_regForm()
    already_post=False
    print(already_post)
    for i in posts:
      print( i.username,book_id, already_post)
      if(current_user.is_authenticated):
        if(current_user.username == i.username):
            print("post found", i.username, book_id, already_post)
            already_post=True
            break
        else:
            print("not found",book_id,i.username )
            already_post=False
      image_file = url_for('static', filename='book_pics/' + book.img_file)
      if form.validate_on_submit():
        post1=Post(username=current_user.username,rating=form.rating.data, description=form.description.data, content=form.content.data, book_id=book_id)
        book.rating=int((book.rating+form.rating.data)//(len(posts)+1))
        db.session.add(post1)
        db.session.commit()
        return redirect(url_for('book_page', book_id=book_id))
 
    
      return render_template('book.html', already_post=already_post,title=book.title, book=book, form=form, posts=posts, image_file=image_file, form1=form1, form2=form2, same_genre=same_genre, same_author=same_author)



@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user1 = Librarian.query.filter_by(token=form.token.data).first()
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user2= User(username= form.username.data, email=form.email.data, password=hashed_password, token=form.token.data)
        print(user2.token)
        if(user1 or (not form.token.data)):
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            db.session.add(user2)
            db.session.commit()
            flash(f'Account created for {form.username.data}!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Register Unsuccessful. Data not found', 'danger')
            return redirect(url_for('register'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():  
    if current_user.is_authenticated:
        print(current_user.username)
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if (user and bcrypt.check_password_hash(user.password, form.password.data)):
            login_user(user, form.remember.data)
            #login_manager.login_view='login'
            flash(f'You logged in as {user.username}', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/book/<int:book_id>/book_registeration", methods=['GET', 'POST'])
@login_required
def book_reg(book_id):
    book=Book.query.get_or_404(book_id)
    form = Book_regForm()
    if form.validate_on_submit():
        book1 = Book.query.filter_by(id=form.book_entry_id.data).first()
        i1=Irequest(book_name=form.book_name.data, book_entry_id=form.book_entry_id.data, user_name=form.username.data, duration=form.duration.data)
        if(book1 and (book1.availability>=1)):
            db.session.add(i1)
            db.session.commit()
            flash(f'the book got successfully registered for {form.username.data} book id is {form.book_entry_id.data}!', 'success')
            
            return redirect(url_for('account'))
        else:
            flash('Sorry the Book is not available. Try later', 'danger')
            return redirect(url_for('home'))
    elif request.method =='GET':
        form.username.data=current_user.username
        form.book_name.data=book.title
        form.book_entry_id.data=book.id
    return render_template('book_reg.html', title='Book Register', form=form, book=book)

@app.route("/librarian_login", methods=['GET', 'POST'])
def lib_login():
    if current_user.is_authenticated:
        print(current_user.username)
        return redirect(url_for('home'))
    form = LibLoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(token=form.token.data).first()
        if user and form.password.data==user.password: #and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, form.remember.data)
            #login_manager.login_view='lib_login'
            flash(f'You logged in as Librarian', 'success')
            return redirect(url_for('home'))
        else:
            
            print("lib")
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('lib_login.html', title='Login', form=form)
#print(library_access)
#print('hi how')
@app.route("/logout")
def logout():  
    logout_user()
    return redirect(url_for('home'))


@app.route("/account",  methods=['GET', 'POST'])
@login_required
def account(): 
    requests = Irequest.query.filter_by(user_name=current_user.username).all()
    form=UpdateAccountForm()
    folder='profile_pics'
    if form.validate_on_submit():
        print("yyyyy",form.picture.data)
        if form.picture.data:
            print("yyyyy",form.picture.data)
            picture_file = save_picture(form.picture.data, folder)
            current_user.image_file = picture_file
        current_user.username=form.username.data
        current_user.email=form.email.data
        db.session.commit()
        flash("You account has been Updated", 'success')
        return redirect(url_for('account'))
    elif request.method =='GET':
        form.username.data=current_user.username
        form.email.data=current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    print(image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form, requests=requests)

@app.route("/issue_requests")
@login_required
def issue_request():  
    reqs=Irequest.query.all()
    return render_template('requests.html', title='Book Issue Requests', reqs=reqs)

@app.route("/manage_book",methods=['GET', 'POST'])
@login_required
def manage_book(): 
    if(current_user.token): 
        books=Book.query.all()
        return render_template('manage1.html', title='Manage Books', books=books)
    else:
        flash(f'You must be a Librarian to access this feature!', 'danger')
        return redirect(url_for('home'))

@app.route("/manage_book/<int:book_id>",methods=['GET', 'POST'])
@login_required
def edit_book(book_id):
    if(current_user.token):
        book=Book.query.get_or_404(book_id)
        form= ManageBookForm()
        if form.validate_on_submit():
        #picture_file = save_picture(form.picture.data)
        #current_user.image_file = picture_file
            book.title=form.name.data
            book.publisher=form.publisher.data
            book.summary=form.summary.data
            book.writer=form.writen_by.data
            book.availability=form.availability.data
            db.session.commit()
            flash(" Updated", 'success')
            return redirect(url_for('manage_book'))
        elif request.method =='GET':
            form.name.data=book.title
            form.writen_by.data=book.writer
            form.publisher.data=book.publisher
            form.summary.data=book.summary
            form.availability.data=book.availability
        return render_template('manage.html', title=book.title, book=book, form=form)
    else:
        flash(f'You must be a Librarian to access this feature!', 'danger')
        return redirect(url_for('home'))

@app.route("/manage_book/add_book", methods=['GET', 'POST'])
@login_required
def add_book():
    if(current_user.token):
        form = ManageBookForm()
        folder='book_pics'
        if form.validate_on_submit():
            print("xxxxxxx", form.picture.data)
            if form.picture.data:
                picture_file = save_picture(form.picture.data, folder)
                print(picture_file)
                book= Book(genre=form.genre.data, img_file = str(picture_file),title= form.name.data, writer=form.writen_by.data, publisher=form.publisher.data, summary=form.summary.data, availability=form.availability.data)
                db.session.add(book)
                db.session.commit()
                flash(f'Book added to Databas with title{form.genre.data}!', 'success')
            else:
                print('not happening')
                book= Book(genre=form.genre.data,title= form.name.data, writer=form.writen_by.data, publisher=form.publisher.data, summary=form.summary.data, availability=form.availability.data)

           
            #user2= User(username= form.username.data, email=form.email.data, password=hashed_password, token=form.token.data)
                db.session.add(book)
                db.session.commit()
                flash(f'Book added to Databas with title {form.name.data}!', 'success')

            return redirect(url_for('manage_book'))
        return render_template('manage.html', title='Add Book', form=form)

    else:
        flash(f'You must be a Librarian to access this feature!', 'danger')
        return redirect(url_for('home'))

@app.route("/delete_request/<int:request_id>",methods=['GET', 'POST'])
@login_required
def delete_confirmation(request_id):

    if(current_user.token):
        request=Irequest.query.get_or_404(request_id)
        book=request.issued
        user=request.issuer
        #flash(f'Do You really want to delete issue request for book id{book.id} requested by user: {user.username} ')
        return render_template('del_conf.html', title='Confirmation', request=request, book=book, user=user)

    else:
        flash("Method not allowed")
        return redirect(url_for('home'))

@app.route("/delete_confirmed/<int:request_id>",methods=['GET', 'POST'])
@login_required
def deleted(request_id):
    if(current_user.token):
        request=Irequest.query.get_or_404(request_id)
        book=request.issued
        user=request.issuer
        request.confirmation_status= 'Rejected'
        db.session.commit()
        flash('Deleted','success')
        return redirect(url_for('issue_request'))
    else:
        flash("Method not allowed", 'danger')
        return redirect(url_for('home'))

@app.route("/confirm_request/<int:request_id>",methods=['GET', 'POST'])
@login_required
def issue_confirmation(request_id):

    if(current_user.token):
        request=Irequest.query.get_or_404(request_id)
        book=request.issued
        user=request.issuer
        #flash(f'Do You really want to delete issue request for book id{book.id} requested by user: {user.username} ')
        return render_template('issue_conf.html', title='Confirmation', request=request, book=book, user=user)

    else:
        flash("Method not allowed")
        return redirect(url_for('home'))

@app.route("/issue_confirmed/<int:request_id>",methods=['GET', 'POST'])
@login_required
def confirmed(request_id):
    if(current_user.token):
        request=Irequest.query.get_or_404(request_id)
        request.confirmation_status='Confirmed'
        book=request.issued
        user=request.issuer
        book1=Book.query.get_or_404(book.id)
        book1_availability=book1.availability
        book1.availability=(book1_availability-1)
        db.session.commit()
        flash('Confirmed','success')
        return redirect(url_for('issue_request'))
    else:
        flash("Method not allowed", 'danger')
        return redirect(url_for('home'))

@app.route("/author/<string:author_name>", methods=['GET', 'POST'])
def author(author_name):
    book_by_author = Book.query.filter_by(writer=author_name).all()
    name=author_name
    #image_file = url_for('static', filename='book_pics/' + .image_file)
    return render_template('author.html', title='Author', book_by_author=book_by_author, name=name )


@app.route("/publisher/<string:publisher_name>", methods=['GET', 'POST'])
def publisher(publisher_name):
    book_by_publisher = Book.query.filter_by(publisher=publisher_name).all()
    name=publisher_name
    return render_template('publisher.html', title='Publisher', book_by_publisher=book_by_publisher, name=name)

@app.route("/deletebook/<int:book_id>",methods=['GET', 'POST'])
@login_required
def delete_book(book_id):
    if(current_user.token):
        deletebook=Book.query.get_or_404(book_id)
        #book=request.issued
        #user=request.issuer
        #request.confirmation_status= 'Rejected'
        db.session.delete(deletebook)
        db.session.commit()
        flash('Deleted','success')
        return redirect(url_for('manage_book'))
    else:
        flash("Method not allowed", 'danger')
        return redirect(url_for('home'))