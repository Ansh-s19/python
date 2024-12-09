from flask import Flask, render_template, redirect, request, session, url_for, flash
import mysql.connector as db
app = Flask(__name__)
app.secret_key = "gymsupps_secret_key"

products = [
    {"id": 1, "name": "Whey-Protein", "price": 2200, "image": "th.jpg"},
    {"id": 2, "name": "Creatine", "price": 639, "image": "th (1).jpg"},
    {"id": 3, "name": "Multivitamin", "price": 550, "image": "OIP (3).jpg"},
    {"id": 4, "name": "Fish Oil", "price": 499, "image": "OIP (5).jpg"},
    {"id": 5, "name": "Mass Gainer", "price": 1800, "image": "OIP (4).jpg"},
    {"id": 6, "name": "Shaker", "price": 399, "image": "th (2).jpg"},
    {"id": 7, "name": "Isolate protein", "price": 3399, "image": "OIP (6).jpg"},
    {"id": 8, "name": "L-carnitine", "price": 599, "image": "OIP (7).jpg"},
]


cart = {}


users = {}




# sql = "insert into gymsupps values(null,  '{}', '{}', '{}')".format( products.id, products.name, products.price)

# cursor = connection.cursor()
# cursor.execute(sql)
# connection.commit()
@app.route("/home1")
def landing_page():
    return render_template("home1.html")

@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/products")
def product_page():
    return render_template("products.html", products=products)

@app.route("/cart", methods=["GET", "POST"])
def cart_page():
    global cart
    if request.method == "POST":
        product_id = int(request.form.get("product_id"))
        action = request.form.get("action")
        
        
        if action == "add":
            if product_id in cart:
                cart[product_id]["quantity"] += 1
            else:
                product = next((p for p in products if p["id"] == product_id), None)
                if product:
                    cart[product_id] = {"name": product["name"], "price": product["price"], "quantity": 1}

       
        elif action == "remove":
            if product_id in cart:
                if cart[product_id]["quantity"] > 1:
                    cart[product_id]["quantity"] -= 1
                else:
                    del cart[product_id]

    # Calculate total cost
    total = sum(item["price"] * item["quantity"] for item in cart.values())
    return render_template("cart.html", cart=cart, total=total)

@app.route("/payment")
def payment():
    global cart
    total = sum(item["price"] * item["quantity"] for item in cart.values())
    return render_template("payment.html", total=total)

@app.route("/clear_cart")
def clear_cart():
    session.pop('cart', None)
    return redirect(url_for('home'))

@app.route('/buy', methods=['POST'])
def buy():
    card_number = request.form['card_number']
    expiry_date = request.form['expiry_date']
    cvv = request.form['cvv']

  
    if card_number and expiry_date and cvv:
        
        session.pop('cart', None)  # Remove the cart
        flash("Order placed successfully!")
        return redirect(url_for('success'))
    else:
        flash("Payment failed! Please try again.")
        return redirect(url_for('home'))

@app.route('/success')
def success():
    return render_template('success.html')

@app.route("/customer_support")
def customer_support():
    return render_template("customer_support.html")


@app.route("/", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
       
        if username in users:
            flash("Username already exists! Please choose a different one.")
        else:
            users[username] = password
            session["user"] = username  
            flash("Registration successful! Redirecting to home.")
            return redirect(url_for('landing_page'))  

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if users.get(username) == password:
            session["user"] = username  
            flash("Login successful!")
            return redirect(url_for('landing_page'))  
        else:
            flash("Invalid credentials. Please try again.")
            return redirect(url_for('login'))

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("user", None)
    flash("You have been logged out!")
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)  