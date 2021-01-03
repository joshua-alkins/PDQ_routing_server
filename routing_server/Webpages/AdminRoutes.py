from flask import Blueprint
from flask import render_template, redirect, url_for, request, session

from werkzeug.security import generate_password_hash

from ..Database import DB as DB

admin_webpages = Blueprint('admin_webpages', __name__, template_folder='templates')

# @admin_webpages.route('/')
# def index():
#     return redirect(url_for('admin_webpages.add_driver'))

@admin_webpages.route('/login', methods=["POST","GET"])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        if username=='admin' and password=='password':
            session['username'] = username
            return redirect(url_for('admin_webpages.add_driver'))
        else:
            return render_template('admin_login.html')
    else:
        return render_template('admin_login.html')

@admin_webpages.route('/add-driver', methods=["POST", "GET"])
def add_driver():
    if 'username' in session:
        if request.method == "POST":
            # check all fields are entered
            
            driver_name = request.form['name']
            email = request.form['email']
            license_plate = request.form['license']

            # check email not in db

            password = generate_password_hash('password'+license_plate)

            DB.add_driver(driver_name,email,license_plate,password)
            # show success message 
            return render_template('success_page.html')
        else:
            return render_template('add_driver_form.html')
    else:
        return redirect(url_for('admin_webpages.login'))

# @admin_webpages.route('/edit-driver')
# def edit_driver():
#     return ""

# @admin_webpages.route('/add-admin')
# def add_admin():
#     return ""