from flask import Flask, render_template, redirect, url_for, flash, request, session
from flask_sqlalchemy import SQLAlchemy
from forms import SignupForm, LoginForm, AddProductForm
from model import db, User, Product
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'f8d4e252c495a2f3d283e4a27fa7b61c'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@127.0.0.1:3306/retail_shop'  # Update with your MySQL credentials
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.route('/')
def home():
    search_query = request.args.get('search', '')
    products = Product.query.filter(Product.name.contains(search_query)).all() if search_query else Product.query.all()
    return render_template('home.html', products=products, hero_image_url='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS6KIaF1q_5pjj7wjMYywZnkgHAE_uFfLbCig&s')



@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        new_user = User(
            username=form.username.data,
            email=form.email.data,
        )
        new_user.set_password(form.password.data)  # Use the method to set the hashed password
        db.session.add(new_user)
        db.session.commit()
        flash('Signup successful! You can now log in.', 'success')
        return redirect(url_for('login'))
    return render_template('signup.html', form=form)


from flask import session, flash, redirect, url_for, render_template
from werkzeug.security import check_password_hash

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):  # Use the method to check the password
            session['user_id'] = user.id
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login failed. Check your username and password.', 'danger')
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    form = AddProductForm()

    if form.validate_on_submit():
        new_product = Product(
            name=form.name.data,
            price=form.price.data,
            unit=form.unit.data,
            category=form.category.data  # Use the string category directly
        )
        db.session.add(new_product)
        db.session.commit()
        flash('Product added successfully!', 'success')
        return redirect(url_for('dashboard'))

    products = Product.query.all()
    return render_template('dashboard.html', form=form, products=products)

@app.route('/products', methods=['GET', 'POST'])
def products():
    products = Product.query.all()
    return render_template('products.html', products=products)

@app.route('/edit_product/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    product = Product.query.get_or_404(product_id)
    form = AddProductForm(obj=product)  # Pre-fill the form with product data

    if form.validate_on_submit():
        product.name = form.name.data
        product.category = form.category.data
        product.price = form.price.data
        product.unit = form.unit.data
        
        db.session.commit()
        flash('Product updated successfully!', 'success')
        return redirect(url_for('dashboard'))

    return render_template('edit_product.html', form=form, product=product)

@app.route('/delete_product/<int:product_id>', methods=['POST'])
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    flash('Product deleted successfully!', 'success')
    return redirect(url_for('products'))

if __name__ == '__main__':
    app.run(debug=True)
