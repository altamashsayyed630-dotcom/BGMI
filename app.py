import csv
import os
import ssl
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import mysql.connector
import razorpay

app = Flask(__name__)
app.secret_key = "my_secret_key_123"

RAZORPAY_KEY_ID = "rzp_test_REPlDVTyFCXpJM"
RAZORPAY_KEY_SECRET = "63hXKAAdfkKgAZv5ntD4EERi"

razorpay_client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))


def get_db_connection():
    return mysql.connector.connect(
        host=os.environ.get("DB_HOST"),
        port=int(os.environ.get("DB_PORT", 3306)),
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASSWORD"),
        database=os.environ.get("DB_NAME"),
        ssl_disabled=True
    )


@app.route('/')
def index():
    return redirect(url_for('login'))


@app.route('/sign', methods=['GET', 'POST'])
def sign():
    if request.method == 'POST':
        name = request.form['name']
        email_id = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash("Passwords do not match!", "error")
            return redirect(url_for('sign'))

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO sign (name, email_id, password, confirm_password) VALUES (%s, %s, %s, %s)",
            (name, email_id, password, confirm_password)
        )
        conn.commit()
        cursor.close()
        conn.close()

        flash("Signup successful! Please login.", "success")
        return redirect(url_for('login'))

    return render_template('sign.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email_id = request.form['email_id']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM sign WHERE email_id=%s AND password=%s", (email_id, password))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user:
            return redirect(url_for('home'))
        else:
            flash("Invalid credentials!", "error")
            return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/table')
def table():
    data = []
    try:
        with open('static/point.csv', newline='', encoding='utf-8') as csvfile:
            csvreader = csv.reader(csvfile)
            headers = next(csvreader)
            for row in csvreader:
                data.append(row)
    except FileNotFoundError:
        flash("point.csv file not found!", "error")
        headers = []
    return render_template('table.html', headers=headers, data=data, title="Points Table")


@app.route('/Highlight')
def Highlight():
    videos = [
        "https://bgmi-highlights.s3.ap-south-1.amazonaws.com/WhatsApp+Video+2025-08-15+at+20.03.24_203ecab4.mp4",
        "https://bgmi-highlights.s3.ap-south-1.amazonaws.com/videopythoo2.mp4",
        "https://bgmi-highlights.s3.ap-south-1.amazonaws.com/video3.mp4"
    ]
    return render_template('Highlight.html', videos=videos)


@app.route('/data')
def show_data():
    data = []
    try:
        with open('static/data.csv', newline='', encoding='utf-8') as csvfile:
            csvreader = csv.reader(csvfile)
            headers = next(csvreader)
            for row in csvreader:
                data.append(row)
    except FileNotFoundError:
        flash("data.csv file not found!", "error")
        headers = []
    return render_template('table.html', headers=headers, data=data, title="Data Table")


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email_id = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('Message')
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO contact_us (name, email_id, subject, Message) VALUES (%s, %s, %s, %s)",
            (name, email_id, subject, message)
        )
        conn.commit()
        cursor.close()
        conn.close()
        flash("Message sent successfully!", "success")
        return redirect(url_for('contact'))
    return render_template('contact.html')


@app.route('/serviceRequest', methods=['GET', 'POST'])
def serviceRequest():
    if request.method == 'POST':
        form_data = (
            request.form.get('Full_Name'),
            request.form.get('In_game_Name'),
            request.form.get('BGMI_UID'),
            request.form.get('phone_number'),
            request.form.get('email'),
            request.form.get('Age_DOB'),
            request.form.get('City'),
            request.form.get('Team_Name'),
            request.form.get('Role_in_team'),
            request.form.get('Device_Name')
        )
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            query = """INSERT INTO service_request
            (Full_Name, In_game_Name, BGMI_UID, phone_number, email, Age_DOB, City, Team_Name, Role_in_team, Device_Name)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            cursor.execute(query, form_data)
            conn.commit()
            cursor.close()
            conn.close()
            return redirect(url_for('payment'))
        except mysql.connector.Error as err:
            flash(f"Database error: {err}", "error")
            return redirect(url_for('serviceRequest'))
        except Exception as e:
            flash("An unexpected error occurred.", "error")
            return redirect(url_for('serviceRequest'))
    return render_template('serviceRequest.html')


@app.route('/payment')
def payment():
    return render_template('payment.html', razorpay_key_id=RAZORPAY_KEY_ID)


@app.route('/create_order', methods=['POST'])
def create_order():
    try:
        data = request.get_json()
        if not data or 'amount' not in data:
            return jsonify({'error': 'Amount is required'}), 400
        amount = int(data['amount']) * 100
        order_data = {'amount': amount, 'currency': "INR", 'payment_capture': '1'}
        order = razorpay_client.order.create(data=order_data)
        return jsonify(order)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
