import os
import random
import secrets
from flask import Flask, redirect, render_template,request, session, url_for,flash,g
import sqlite3
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SECRET_KEY'] = 'plantem_key'


# Function to check if user is logged in
def is_logged_in():
  return 'uname' in session


@app.route('/')
def home():
    if is_logged_in():
        uname = session['uname']
        return render_template('home.html', uname=uname)
    else:
        return render_template('home.html' )
    
# Configure upload folder (adjust path as needed)
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')


# Create products database if not exists
def create_products_table():
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS products (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    price REAL NOT NULL,
                    image TEXT NOT NULL
                    )''')
    conn.commit()
    conn.close()
create_products_table()


# Function to add a product
def add_product(name, image, price):
  conn = sqlite3.connect('products.db')
  cursor = conn.cursor()
  cursor.execute("""INSERT INTO products (name, price, image ) VALUES (?, ?, ?)""",  (name, price,image))
  conn.commit()
  conn.close()


# Routes (updated)
@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
  if not is_logged_in() or session['uname'] != 'admin':
    return redirect(url_for('login'))  # Redirect to login if not admin or not logged in
  if request.method == 'POST':
    name = request.form['name']
    image = request.form['image']  # Assuming image URL or path
    price = float(request.form['price'])
    add_product(name,  price, image )
    return render_template('add_product_success.html')  # Redirect to success page
  else:
    return render_template('add_product.html')
  

@app.route('/about')
def about():
    return render_template('about.html' )


@app.route('/search', methods=['GET'])
def search():
    # Get the search query from the URL query parameters
    query = request.args.get('query')
    return render_template('search.html', searchquery=query)


@app.route('/indoor')
def indoor():
    return render_template('indoor.html' )


@app.route('/outdoor')
def outdoor():
    return render_template('outdoor.html' )


@app.route('/seeds')
def seeds():
    return render_template('seeds.html' )


# Route for the signup page
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method=='GET': # If the request is GET we return the sign up page and forms
        return render_template('signup.html')
    elif request.method == 'POST':
        uname = request.form['uname']
        mobile = request.form['mobile']
        email = request.form['email']
        password = request.form['password']
        # Check if the username or email already exists in the database
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM users WHERE uname = ? OR email = ?", (uname, email))
        existing_user = cursor.fetchone()
        if existing_user:
            flash('Username or email already exists. Please choose a different one.', 'error')
            return redirect(url_for('signup'))
        # Insert the new user into the database
        cursor.execute("INSERT INTO users (uname, mobile, email, password) VALUES (?, ?, ?, ?)", (uname, mobile, email, password))
        db.commit()
        # Redirect the user to the login page after successful signup
        print("Redirecting to login page...")
        # flash('Sign up successful! Please log in.', 'success')
        return redirect(url_for('login'))
    

# Function to add product to cart
def addToCart(plantName, price):
    # Retrieve the cart items from session or initialize an empty list
    cartItems = session.get('cart', [])
    # Add the selected product to the cart
    cartItems.append({'name': plantName, 'price': price})
    # Update the session with the modified cart items
    session['cart'] = cartItems
    # Optionally, you can provide feedback to the user
    return 'Added ' + plantName + ' to cart.'


@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    product_name = request.form.get('plant_name')
    product_price = float(request.form.get('price'))
    if 'cart' not in session:
        session['cart'] = []
    session['cart'].append({'name': product_name, 'price': product_price})
    # Set a flash message to indicate the product has been added to the cart
    flash(f'Added {product_name} to cart successfully!', 'success')
    return redirect(url_for('cart'))


@app.route('/cart')
def cart():
    cartItems = session.get('cart', [])
    total_price = sum(item['price'] for item in cartItems)
    return render_template('cart.html', cartItems=cartItems, total_price=total_price)


@app.route('/payment', methods=['POST'])
def payment():
    # Process the payment here
    # For demonstration purposes, let's assume the payment is successful
    # You can perform any necessary payment processing or validation
    # Clear the cart (empty the session)
    session.pop('cart', None)
    # Redirect to the home page
    return redirect(url_for('home'))


@app.route('/location')
def location():
    return render_template('location.html' )


@app.route('/checkout')
def checkout():
    cart_items = session.get('cart', [])
    total_price = sum(item['price'] for item in cart_items)
    return render_template('checkout.html', total_price=total_price)


# Function to get the database connection
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect('users.db')
    return g.db


# Function to close the database connection
@app.teardown_appcontext
def close_db(error):
    if 'db' in g:
        g.db.close()


# Function to generate OTP
def generate_otp():
    return secrets.token_hex(4)


# Function to authenticate user based on OTP
def authenticate_user(otp):
    # Placeholder for authentication logic
    # For demonstration, let's assume the OTP is valid if it matches '1234'
    return otp == '1234'


# Route for the login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        uname = request.form['uname']
        password = request.form['password']
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT password FROM users WHERE uname = ?", (uname,))
        user = cursor.fetchone()
        if user and user[0] == password:
            session['uname'] = uname
            otp = generate_otp()
            session['otp'] = otp
            return redirect(url_for('login_otp'))  # Redirect to login OTP page
        else:
            return render_template('login.html', message="Invalid username or password.")
    return render_template('login.html')


# Route for the login OTP page
@app.route('/login_otp', methods=['GET', 'POST'])
def login_otp():
    if 'uname' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        otp_entered = request.form['otp']
        otp_expected = session.get('otp')
        if otp_entered == otp_expected and authenticate_user(otp_entered):
            # OTP authentication successful
            flash("OTP authentication successful. You are logged in.")
            return redirect(url_for('home'))
        else:
            return render_template('login_otp.html', message="Invalid OTP. Please try again.")
    return render_template('login_otp.html')


# Route for the forgot password page
@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']
        if new_password != confirm_password:
            flash('Passwords do not match. Please try again.', 'error')
            return redirect(url_for('forgot_password'))
        # Update the password in the database
        db = get_db()
        cursor = db.cursor()
        cursor.execute("UPDATE users SET password = ? WHERE email = ?", (new_password, email))
        db.commit()
        flash('Your password has been successfully updated.', 'success')
        return redirect(url_for('login'))
    return render_template('forgot_password.html')


@app.route('/logout')
def logout():
  session.pop('uname', None)
  return redirect(url_for('home'))
if __name__ == '__main__':
   app.run(debug=True,port=8000)
