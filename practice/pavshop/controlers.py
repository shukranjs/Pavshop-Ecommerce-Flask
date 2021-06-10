from pavshop import app, os, db, bcrypt, login_manager
from flask import render_template, redirect, request, url_for, flash
from werkzeug.utils import secure_filename
from pavshop.models import Blog, BlogCategory
from pavshop.forms import RegistrationForm, LoginForm, UserPostForm
from pavshop.models import User, UserPost
from pavshop.file_upload import save_picture
from flask_login import login_user, logout_user, login_required, current_user
# ADMIN INTERFACE 
@app.route("/admin-blog-list")
def blog_list():
    blogs = Blog.query.all()
    return render_template('admin/blog-list.html', blogs=blogs)

@app.route("/admin-blog-add", methods=['GET', "POST"])
def blog_add():
    categories = BlogCategory.query.all()
    if request.method == 'POST':
        file = request.files['file']
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        blog = Blog(
            title=request.form['title'],
            short_description=request.form['short-desc'],
            description=request.form['description'],
            image = filename,
            category = request.form['category']
        )
        db.session.add(blog)
        db.session.commit()
        return redirect(url_for('blog_list'))
    return render_template('admin/blog-add.html', categories=categories)

@app.route("/admin-blog-edit/<int:id>", methods=['GET', "POST"])
def blog_edit(id):
    blog = Blog.query.get_or_404(id)
    categories = BlogCategory.query.all()
    print(blog)
    if request.method == 'POST':
        file = request.files['file']
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        blog.title = request.form['title']
        blog.short_description = request.form['short-desc']
        blog.description = request.form['description']
        blog.image = filename
        blog.category = request.form['category']
        db.session.commit()
        return redirect(url_for('blog_list'))
    return render_template('admin/blog-edit.html', categories=categories)

@app.route("/admin-blog-delete/<int:id>")
def blog_delete(id):
    blog = Blog.query.get_or_404(id)
    db.session.delete(blog)
    db.session.commit()
    return redirect(url_for('blog_list'))

# USER INTERFACE ROUTES 

@app.route('/blog-list')
def user_blog_list():
    blogs = Blog.query.all()
    return render_template('blog-list.html', blogs=blogs)

@app.route('/blog-detail/<int:id>')
def blog_detail(id):
    blog = Blog.query.get_or_404(id)
    print(blog)
    return render_template('blog-detail.html', blog=blog)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user_raw_parol = form.parol.data
        parol_hashed = bcrypt.generate_password_hash(user_raw_parol).decode('utf-8')
        if form.image.data:
            image = save_picture(form.image.data)
            user = User(image=image)
        user = User(
            full_name = form.full_name.data,
            email = form.email.data,
            parol = parol_hashed,
            bio = form.bio.data,
        )
        db.session.add(user)
        db.session.commit()
        print(user.parol)
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.parol, form.parol.data):
            login_user(user)
            flash(f'{user.full_name}, you logged in successfully', 'success')
            return redirect(url_for('home'))
    return render_template('login.html', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UserPostForm()
    user_posts = UserPost.query.all()
    if form.validate_on_submit():
        user_post = UserPost(
            title = form.title.data,
            short_description = form.short_description.data,
            content = form.content.data,
            image = save_picture(form.image.data),
            author = current_user.full_name,
        )
        db.session.add(user_post)
        db.session.commit()
        return redirect(url_for('account'))
    return render_template('account.html', form=form, user_posts=user_posts)

@app.route('/home')
@app.route('/')
def home():
    return render_template('index.html')