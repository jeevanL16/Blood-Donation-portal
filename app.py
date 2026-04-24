from flask import Flask, render_template, request, redirect, url_for, session, send_file,flash, get_flashed_messages
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from flask_migrate import Migrate
from config import Config
from models import Donor, Blood_Request, Contact, Feedback,db
from forms import DonorForm, RequestForm, ContactForm, FeedbackForm
import MySQLdb
import os
from dotenv import load_dotenv

import pandas as pd
from io import BytesIO
# from werkzeug.security import check_password_hash

load_dotenv()
csrf = CSRFProtect()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    migrate.init_app(app, db)
    return app


app = create_app()

def get_db_connection():
    host = os.environ.get("DB_HOST")
    user = os.environ.get("DB_USER")
    password = os.environ.get("DB_PASSWORD")
    db = os.environ.get("DB_NAME")
    return MySQLdb.connect(host=host, user=user, password=password, db=db)

@app.route('/donor', methods=['GET', 'POST'])
def donor():
    form = DonorForm()
    if form.validate_on_submit():
        new = Donor(
            name=form.name.data,
            age=form.age.data,
            gender=form.gender.data,
            blood_group=form.blood_group.data,
            contact=form.contact.data,
            location=form.location.data
        )
        flash('Donor registration successful! After verification, you will receive details on when and where to donate blood',"success")

        db.session.add(new)
        db.session.commit()
        return redirect('/')
    
    return render_template('donor.html', form=form)

@app.route('/request', methods=['GET', 'POST'])
def blood_request():
    form = RequestForm()
    if form.validate_on_submit():
        new_request = Blood_Request(
            name=form.name.data,
            age=form.age.data,
            gender=form.gender.data,
            bloodgroup=form.bloodgroup.data,
            location=form.location.data,
            contact=form.contact.data,
            reason=form.reason.data,
            hospital=form.hospital.data
            
        )        
        flash('Your blood request has been successfully processed! After verification, the blood will be delivered to the hospital', 'success')
        db.session.add(new_request)
        db.session.commit()
        return redirect('/')
    return render_template('request.html', form=form)

admin_users = {
    'admin': os.environ.get('ADMIN_PASSWORD'),
    'jeevan': os.environ.get('JEEVAN_PASSWORD'),
    'suma': os.environ.get('SUMA_PASSWORD'),
    'chandini': os.environ.get('CHANDINI_PASSWORD'),
    'venu': os.environ.get('VENU_PASSWORD')
}

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    error = None
    if request.method == 'POST':
        username = request.form['username'].strip().lower()
        password = request.form['password']

        
        if username in admin_users and admin_users[username] == password:
            session['admin'] = username  
            return redirect('/admin/dashboard')
        else:
            error = 'Invalid username or password'
    return render_template('admin_login.html', error=error)


@app.route('/admin/dashboard')
def admin_dashboard():
    if not session.get('admin'):
        return redirect(url_for('adminlogin'))

    con = get_db_connection()
    cur = con.cursor(MySQLdb.cursors.DictCursor)

    cur.execute("SELECT * FROM donor ORDER BY id DESC")
    donors = cur.fetchall()

    cur.execute("SELECT * FROM blood_request ORDER BY id DESC")
    requests = cur.fetchall()

    cur.execute("SELECT * FROM contact  ORDER BY id DESC")
    contacts = cur.fetchall()

    cur.execute("SELECT * FROM feedback ORDER BY id DESC")
    feedback = cur.fetchall()

    con.close()
    return render_template("admin_dashboard.html", donors=donors, requests=requests, contacts=contacts, feedback=feedback)



@app.route('/export_donors_excel')
def export_donors_excel():
    con = get_db_connection()
    df = pd.read_sql("SELECT * FROM donor", con)
    con.close()

    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Donors')
    output.seek(0)
    return send_file(output, download_name="donors.xlsx", as_attachment=True)

@app.route('/export_requests_excel')
def export_requests_excel():
    con = get_db_connection()
    df = pd.read_sql("SELECT * FROM blood_request", con)
    con.close()

    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Requests')
    output.seek(0)
    return send_file(output, download_name="requests.xlsx", as_attachment=True)


@app.route('/admin/add_feedback_home/<int:id>', methods=['POST'])
def add_feedback_home(id):
    con = get_db_connection()
    cur = con.cursor()
    cur.execute("UPDATE feedback SET approved = TRUE WHERE id = %s", (id,))
    con.commit()
    con.close()
    flash("feedback added sucessfully to homepage")
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/delete_feedback/<int:id>', methods=['POST'])
def delete_feedback(id):
    con = get_db_connection()
    cur = con.cursor()
    cur.execute("DELETE FROM feedback WHERE id = %s", (id,))
    con.commit()
    con.close()
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/approve_donor/<int:id>', methods=['POST'])
def approve_donor(id):
    con = get_db_connection()
    cur = con.cursor()
    cur.execute("UPDATE donor SET approved = TRUE WHERE id = %s", (id,))
    con.commit()
    con.close()
    flash('Donor has been approved.', 'sucess')
    return redirect(url_for('admin_dashboard'))

@app.route('/reject_donor/<int:id>', methods=['POST'])
def reject_donor(id):
    donor = Donor.query.get_or_404(id)
    db.session.delete(donor)  
    db.session.commit()
    flash('Donor has been rejected and removed.', 'danger')
    return redirect(url_for('admin_dashboard')) 

@app.route('/')
def home():
    con = get_db_connection()
    cur = con.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT * FROM feedback WHERE approved = TRUE")
    approved_feedbacks = cur.fetchall()
    
    cur.execute("""
        SELECT blood_group, COUNT(*) as count
        FROM donor
        WHERE approved = TRUE
        GROUP BY blood_group
    """)
    blood_data = cur.fetchall()

    con.close()
    return render_template("index.html", feedback=approved_feedbacks,blood_availability=blood_data)



@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        new_contact = Contact(
            name=form.name.data,
            contact=form.contact.data,
            message=form.message.data
        )
        flash('Thank You For Reaching Out We Will Get Back To You Shortly',"success")
        db.session.add(new_contact)
        db.session.commit()
        return redirect('/')
    return render_template('contact.html', form=form)

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    form = FeedbackForm()
    if form.validate_on_submit():
        new = Feedback(name=form.name.data, message=form.message.data)
        flash('Thank you Feedback sent',"success")
        db.session.add(new)
        db.session.commit()
        return redirect('/')
    return render_template('feedback.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
