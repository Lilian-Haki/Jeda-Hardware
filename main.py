from configs.base_config import *
from unicodedata import category
from flask_login import UserMixin,login_required
from flask import Flask, render_template, request, redirect, url_for, flash, session, make_response
from werkzeug.security import generate_password_hash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from functools import wraps
import os
import flask
import flask_login
from datetime import date
from sqlalchemy import func
import psycopg2
import json
import ast
import pdfkit
from datetime import datetime
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:lilian@localhost:5432/tnd'
app.config["SECRET_KEY"] = "#trialanderror"
conn = psycopg2.connect(user="postgres", password="lilian",
                        host="localhost", port="5432", database="tnd")
# Open a cursor to perform database operations
cur = conn.cursor()
# app.config.from_object(Development)
db = SQLAlchemy(app)
#solving working out of application context
app.app_context().push()
# from models.Patient import Patient
# from models.Staff import Staff
# from models.Appointment import Appointment
# from models.Role import Role
# from models.charges import Charges
# from models.visitors import Visitors
# from models.inventory import Inventory
# from utils.init_roles import *

class Category(db.Model):
    __tablename__ = 'category'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), unique=True, nullable=False)


class Products(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    supplier = db.Column(db.String(80),  nullable=False)
    product_name = db.Column(db.String(80), nullable=False)
    category = db.Column(db.String(80),  nullable=False)
    buying_price = db.Column(db.Integer, nullable=False)
    selling_price = db.Column(db.Integer, nullable=False)
    stock_quantity = db.Column(db.Integer, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))

    #rel = db.relationship('Payment', backref='products', lazy=True)

    #products_id = db.relationship('Payment', backref='products_id', lazy=True , primaryjoin="Products.id == Post.products_id")

class Customer(db.Model):
    __tablename__ = 'customers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80),  nullable=False)
    email_address = db.Column(db.String(80),unique=True, nullable=False)
    phone_number = db.Column(db.String(13),  nullable=False)
    #relat = db.relationship('Payment', backref='customers', lazy=True)
    #relat = relationship("Payment", backref=db.backref("customers", lazy="joined"))

class Suppliers(db.Model):
    __tablename__ = 'suppliers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80),  nullable=False)
    contact = db.Column(db.String(13),  nullable=False)
    email_address = db.Column(db.String(80),unique=True, nullable=False)

class Payment(db.Model):
    __tablename__ = 'payment'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    customers_id = db.Column(db.Integer, db.ForeignKey('customers.id'))
    service_offered = db.Column(db.String(80),  nullable=True)
    cost = db.Column(db.Integer, nullable=True)
    quantity = db.Column(db.Integer, nullable=True)
    subtotal = db.Column(db.Integer, nullable=True)
    time_of_offering = db.Column(db.DateTime(
        timezone=True), server_default=func.now())

class Sales(db.Model):
    __tablename__ = 'sales'
    id = db.Column(db.Integer, primary_key=True)
    pid = db.Column(db.Integer, db.ForeignKey('products.id'))
    product_name = db.Column(db.String(80),  nullable=True)
    quantity_bought = db.Column(db.Integer, nullable=True)
    total_paid = db.Column(db.Integer, nullable=True)
    time_of_offering = db.Column(db.DateTime(
        timezone=True), server_default=func.now())

class Invoices(db.Model):
    __tablename__ = 'invoices'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    customers_id = db.Column(db.Integer, db.ForeignKey('customers.id'))

    payment_id = db.Column(db.Integer, db.ForeignKey('payment.id'))
    service_offered = db.Column(db.String(80),  nullable=True)
    cost = db.Column(db.Integer, nullable=True)
    quantity = db.Column(db.Integer, nullable=True)
    subtotal = db.Column(db.Integer, nullable=True)
    time_of_offering = db.Column(db.DateTime(
        timezone=True), server_default=func.now())

    






class Admin(UserMixin,db.Model):
    __tablename__ = 'admin'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)

    def insert(self):
        db.add(self)
        db.commit()

        return self
    # @classmethod
    # def find_user_byId(cls, user_id):
    #     return cls.query.filter_by(id = user_id).first()

    # authenticate password
    @classmethod
    def check_password(cls, email, password):
        record = cls.query.filter_by(email=email).first()

        if record and check_password_hash(record.password, password):
            return True
        else:
            return False

    @classmethod
    def check_email_exists(cls, email):
        record = cls.query.filter_by(email=email).first()

        if record:
            return True
        else:
            return False

    # fetch by email
    @classmethod
    def fetch_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

def seeding():
    category = ['Doors', 'Wall', 'Electronics', ' Roof']

    for category in category:
        exists = Category.query.filter_by(name=category).first()

        if not exists:
            new_category = Category(name=category)
            db.session.add(new_category)
            db.session.commit()
            
                
db.create_all()

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized! Please log in', 'danger')

            return redirect(url_for('login', next=request.url))
    return wrap

 
@app.route('/staff', methods=['GET', 'POST'])
@login_required
def staff():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        hashed_password = generate_password_hash(password=hashed_password)


        # check that email does not exist before registering the user
        if Admin.check_email_exists(email):
            flash(
                "The user already exists. Please try registering with a different email.", "danger")
        else:
            new_staff_member = Admin(username=username, email=email, password=password)

            db.session.add(new_staff_member)
            db.session.commit()

            flash("Staff member successfully registered", "success")

    logged_in = session['logged_in']
    username = session['username']
    admin = Admin.query.all()

    return render_template('staff.html', admin=admin,  logged_in=logged_in, username=username)

@app.route('/', methods=['GET', 'POST'])
def login():
    if flask.request.method == 'POST':
        email = flask.request.form['email']
        password = flask.request.form['password']
        
        
        # check if email exist
        if Admin.check_email_exists(email=email):
            # if the email exists check if password is correct
            if Admin.check_password(email=email, password=password):
                session['logged_in'] = True
                session['username'] = Admin.fetch_by_email(email).username
                session['id'] = Admin.fetch_by_email(email).id

                return redirect(url_for('dashboard'))
            else:
                flash("Incorrect password", "danger")

                return render_template('login.html')
        else:
            flash("Email does not exist", "danger")

    return render_template("login.html")

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        hashed_password = generate_password_hash(password=password)


        # check that email does not exist before registering the user
        if Admin.check_email_exists(email):
            flash(
                "The user already exists. Please try registering with a different email.", "danger")
        else:
            new_staff_member = Admin(username=username, email=email, password=hashed_password)

            db.session.add(new_staff_member)
            db.session.commit()

            flash(
                "You have successfully signed up. You can now log in to your account.", "success")

            return redirect(url_for('login'))


    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    session.clear()
    flash('You have been logged out', 'success')

    return redirect(url_for('login'))


@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    logged_in = session['logged_in']
    username = session['username']
    cur.execute("select count(id) from products")
    data1 = cur.fetchone()
    cur.execute("select count(id) from customers")
    data2 = cur.fetchone()
    cur.execute("select count(id) from suppliers")
    data3 = cur.fetchone()
    cur.execute("select count(id) from sales")
    data4 = cur.fetchone()
    cur.execute("select sum(total_paid) from sales")
    data5 = cur.fetchone()
    cur.execute("SELECT product_name, SUM(total_paid) AS total FROM sales GROUP BY product_name")
    graph = cur.fetchall()
    
    v = []
    y = []

    for i in graph:
        v.append(i[0])
        y.append(i[1])
    print(y)
    print(v)


    return render_template('dashboard.html', logged_in=logged_in, username=username, data1=data1,data2=data2,data3=data3,data4=data4,data5=data5, y=y, v=v, graph=graph)

@app.route("/products", methods=["GET", "POST"])
@login_required
def products():
    logged_in = session['logged_in']
    username = session['username']

    if request.method == "POST":
        supplier = request.form["supplier"]
        product_name = request.form["product_name"]
        category = request.form["category"]
        buying_price = request.form["buying_price"]
        selling_price = request.form["selling_price"]
        stock_quantity = request.form["stock_quantity"]
        cur.execute("INSERT INTO products(supplier,product_name,category,buying_price,selling_price,stock_quantity) values(%s,%s,%s,%s,%s,%s)",
                    (supplier,product_name,category, buying_price, selling_price, stock_quantity))
        conn.commit()
        
        return redirect("/products")

    else:

        products = Category.query.all()
        cur.execute("SELECT category FROM products")

        cur.execute("SELECT * FROM products")
        data = cur.fetchall()
        return render_template("products.html", logged_in=logged_in, username=username, data=data,products=products)

@app.route('/edit_products', methods=['POST'])
@login_required
def edit_products():
    if request.method == 'POST':
        id = request.form["id"]
        supplier = request.form["supplier"]
        product_name = request.form["product_name"]
        category = request.form["category"]
        buying_price = request.form["buying_price"]
        selling_price = request.form["selling_price"]
        stock_quantity = request.form["stock_quantity"]
        
        product_to_edit = Products.query.filter_by(id=id).first()
        product_to_edit.supplier = supplier
        product_to_edit.product_name = product_name
        product_to_edit.category = category
        product_to_edit.buying_price = buying_price
        product_to_edit.selling_price = selling_price
        product_to_edit.stock_quantity = stock_quantity

        db.session.add(product_to_edit)
        db.session.commit()

        flash("Product successfully edited", "success")      

        return redirect(url_for('products'))

@app.route("/customers", methods=["GET", "POST"])
@login_required    
def customers():
    logged_in = session['logged_in']
    username = session['username']

    if request.method == "POST":
        name = request.form["name"]
        email_address = request.form["email_address"]
        phone_number = request.form["phone_number"]
        
        cur.execute("INSERT INTO customers(name,email_address,phone_number) values(%s,%s,%s)",
                    (name, email_address, phone_number))
        conn.commit()
        return redirect("/customers")

    else:
        cur.execute("SELECT * FROM customers")
        data = cur.fetchall()
        return render_template("customers.html", data=data, logged_in=logged_in, username=username)

@app.route('/edit_customers', methods=['POST'])
@login_required
def edit_customers():
    if request.method == "POST":
        id = request.form["id"]
        name = request.form["name"]
        email_address = request.form["email_address"]
        phone_number = request.form["phone_number"]
        
        item_to_edit = Customer.query.filter_by(id=id).first()
        item_to_edit.name = name
        item_to_edit.email_address = email_address
        item_to_edit.phone_number = phone_number
        
        db.session.add(item_to_edit)
        db.session.commit()


        flash("Customer successfully edited", "success")      

        return redirect(url_for('customers'))

@app.route("/suppliers", methods=["GET", "POST"])
@login_required    
def suppliers():
    logged_in = session['logged_in']
    username = session['username']

    if request.method == "POST":
        name = request.form["name"]
        contact = request.form["contact"]
        email_address = request.form["email_address"]
        
        cur.execute("INSERT INTO suppliers(name,contact,email_address) values(%s,%s,%s)",
                    (name,contact,email_address))
        conn.commit()
        return redirect("/suppliers")

    else:
        cur.execute("SELECT * FROM suppliers")
        data = cur.fetchall()
        return render_template("supplier.html", data=data, logged_in=logged_in, username=username)

@app.route("/edit_supplier", methods=["GET", "POST"])
@login_required   
def edit_supplier():
    if request.method == "POST":
        id = request.form["id"]
        name = request.form["name"]
        contact = request.form["contact"]
        email_address = request.form["email_address"]
        
        item_to_edit = Suppliers.query.filter_by(id=id).first()
        item_to_edit.name = name
        item_to_edit.contact = contact
        item_to_edit.email_address = email_address
        
        db.session.add(item_to_edit)
        db.session.commit()

       
        return redirect(url_for('suppliers'))

@app.route('/payment', methods=['POST', 'GET'])
@login_required
def payment():
    logged_in = session['logged_in']
    username = session['username']

    if request.method == 'POST':
        phone_number = request.form['phone_number']
        customer = Customer.query.filter_by(phone_number=phone_number).first()
        if customer:
            session['paymentid'] = customer.id
            customers = Customer.query.filter_by(phone_number=phone_number).all()

            return redirect(url_for("chargestable", customers=customers))
        else:
            return render_template("telephoneform.html")
    else:

        return render_template("telephoneform.html", logged_in=logged_in, username=username)

@app.route('/chargestable', methods=['POST', 'GET'])
@login_required
def chargestable():
    logged_in = session['logged_in']
    username = session['username']
    x = session['paymentid']
    payment = Payment.query.filter_by(customers_id=x).all()
    total_cost = Payment.query.with_entities(
        func.sum(Payment.subtotal)).filter(Payment.customers_id == x).first()
    
    total_cost = total_cost[0]
    products = Products.query.all()
    customer = Customer.query.filter(Customer.id == x)

    return render_template('invoicing.html',payment=payment, products=products, customer=customer, total_cost=total_cost, logged_in=logged_in, username=username)


@app.route('/bill', methods=['POST', 'GET'])
@login_required
def bill():
    if request.method == 'POST':
        service_offered = request.form['service_offered']
        quantity = request.form["stock_quantity"]
        cur.execute("SELECT stock_quantity FROM products where product_name=%s", [service_offered])
        stock_quantity = cur.fetchone()
        squantity= stock_quantity[0]
        
        rem = int(squantity)-int(quantity)
        if rem < 0:
            pass
            flash("products are less than the requested amount for purchase")
            return redirect('/chargestable')
        else:
            cost = Products.query.filter_by(product_name=service_offered).first()
            cost = cost.selling_price
            subtotal = int(cost) * int(quantity)
            time_of_offering = datetime.now()
            cur.execute("INSERT INTO sales(product_name,quantity_bought,total_paid,time_of_offering) values(%s,%s,%s,%s)", (
                service_offered,quantity,subtotal,time_of_offering))

            cur.execute("UPDATE products set stock_quantity=%(rem)s where product_name=%(product_name)s", {
                        "product_name": service_offered, "rem": rem})
            conn.commit()
            
            x = session['paymentid']
            cur.execute("SELECT id FROM products where product_name=%s", [service_offered])
            y = cur.fetchone()
            payment = Payment(
            customers_id=x,product_id=y, service_offered=service_offered,cost=cost,quantity=quantity,subtotal=subtotal,time_of_offering=time_of_offering)
            db.session.add(payment)
            db.session.commit()
            return redirect('/chargestable')


@app.route('/paybill', methods=['POST', 'GET'])
@login_required
def paybill():
    if request.method == 'POST':

        service_offered = request.form['service_offered']
        subtotal = request.form['subtotal']
        time_of_offering = datetime.now()

        subtotal = int(subtotal)
        subtotal = -abs(int(subtotal))

        x = session['paymentid']
        payment = Payment(
            customers_id=x, service_offered=service_offered, subtotal=subtotal,time_of_offering=time_of_offering)
        db.session.add(payment)
        db.session.commit()

        return redirect('/chargestable')


@app.route('/sales', methods=['GET', 'POST'])
@login_required
def sales():
    logged_in = session['logged_in']
    username = session['username']
    cur.execute("SELECT * FROM sales")
    data = cur.fetchall()
    return render_template("sales.html", data=data, logged_in=logged_in, username=username)

@app.route("/salesrange")
def salesrange():
    logged_in = session['logged_in']
    username = session['username']

    return render_template('salesrange.html', logged_in=logged_in, username=username)

@app.route('/sales_report', methods=["POST", "GET"])
def vis_repo():
    logged_in = session['logged_in']
    username = session['username']
    if request.method == "POST":
        startdate = request.form['startdate']
        enddate = request.form['enddate']
        data = {"startdate": startdate, "enddate": enddate}
        return redirect(url_for('vis_repo', x=data))
    else:
        # try:
        x = request.args['x']
        d = ast.literal_eval(x)
        startdate = d["startdate"]
        enddate = d["enddate"]
        print(type(startdate))
        x = datetime.strptime(startdate, '%Y-%m-%d')
        x = datetime.strptime(enddate, '%Y-%m-%d')
        sales = Sales.query.filter(
            Sales.time_of_offering.between(startdate, enddate)).all()
        return render_template("salesrepo.html", sales=sales, logged_in=logged_in, username=username)

@app.route('/help', methods=['GET', 'POST'])
@login_required
def help():

    return render_template('help.html')

@app.route('/about', methods=['GET', 'POST'])
@login_required
def about():

    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)
