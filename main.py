from flask import Flask, render_template, request, redirect, url_for, send_from_directory, send_file, make_response
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_sqlalchemy import SQLAlchemy
# from wfms import Details
import csv
from io import StringIO
import os
import uuid  # Add this import statement

from flask import Flask, render_template, request, redirect, url_for, flash
from itsdangerous import URLSafeTimedSerializer

from flask_mail import Mail, Message

from werkzeug.security import generate_password_hash, check_password_hash

from dotenv import load_dotenv

app = Flask(__name__)

# Load environment variables from .env file
load_dotenv()

# Configuration from environment variables
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS') == 'True'

# Set the secret key
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT'))
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS') == 'True'
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')

db = SQLAlchemy(app)
mail = Mail(app)
# serializer = URLSafeTimedSerializer(app.secret_key)
serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])

# User model
class User(db.Model, UserMixin):

    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False) 
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), nullable=False)


# Define the SQLAlchemy model for the `details` table
class Details(db.Model):
    __tablename__ = 'details'

    order_id = db.Column(db.String, primary_key=True)
    amount = db.Column(db.Integer)
    profit = db.Column(db.Integer)
    quantity = db.Column(db.Integer)
    category = db.Column(db.String)
    sub_category = db.Column(db.String)
    paymentMode = db.Column(db.String(255))


# Define the SQLAlchemy model for the `orders` table
class Orders(db.Model):
    __tablename__ = 'orders'

    Order_ID = db.Column(db.String, primary_key=True)
    Order_Date = db.Column(db.DateTime)
    CustomerName = db.Column(db.String)
    State = db.Column(db.String)
    City = db.Column(db.String)


# Define the SQLAlchemy model for the `attendance` table
class Attendance(db.Model):
    __tablename__ = 'attendance'

    Employee_ID = db.Column(db.BigInteger, primary_key=True)
    Employee_Name = db.Column(db.Text)
    Attendance = db.Column(db.Text)
    Date = db.Column(db.DateTime)
    Total_Work_Hours = db.Column(db.Integer)
    City_Name = db.Column(db.Text)
    Region = db.Column(db.Text)
    State = db.Column(db.Text)


# Login manager setup
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).get(int(user_id))


@app.route('/home')
@login_required
def home():
    role = current_user.role if current_user.is_authenticated else None
    if role == 'admin':
        return render_template('home.html')
    else:
        return redirect(url_for('dashboard'))


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', message='Invalid username or password')
    return render_template('login.html')


#=================Landing Page Route=========================
@app.route('/dashboard')
@login_required
def dashboard():
    role = current_user.role if current_user.is_authenticated else None
    return render_template('dashboard.html', role=role)


#=================Dashboards Route=========================

@app.route('/attendance')
@login_required
def attendance():
    role = current_user.role if current_user.is_authenticated else None
    return render_template('attendance.html', role=role)


@app.route('/attendancewhite')
@login_required
def attendanceWhite():
    role = current_user.role if current_user.is_authenticated else None
    return render_template('attendanceWhite.html', role=role)


@app.route('/salesdashboard')
@login_required
def salesDashboard():
    role = current_user.role if current_user.is_authenticated else None
    return render_template('salesDashboard.html', role=role)


@app.route('/wfmsdashboard')
@login_required
def wfmsDashboard():
    role = current_user.role if current_user.is_authenticated else None
    return render_template('wfmsDashboard.html', role=role)


#=================Reports Route=========================

@app.route('/detailsreport')
@login_required
def detailsReport():
    # Fetch data from the details table
    details_data = Details.query.all()  # Assuming Details is your SQLAlchemy model

    # Generate the CSV file dynamically (replace this with your CSV generation logic)
    # For demonstration purposes, I'm just creating a static file name
    csv_filename = "reportone.csv"
    # csv_filename = "reportone.csv"

    # Pass the data and CSV filename to the HTML template
    return render_template('detailsreport.html', details_data=details_data, csv_filename=csv_filename, report_type='Details Report')


@app.route('/ordersreport')
@login_required
def ordersReport():
    # Fetch data from the orders table
    orders_data = Orders.query.all()  # Assuming Orders is your SQLAlchemy model

    # Pass the data to the HTML template
    return render_template('ordersreport.html', orders_data=orders_data, report_type='Orders Report')


@app.route('/attendancereport')
@login_required
def attendanceReport():
    # Fetch data from the orders table
    attendance_data = Attendance.query.all()  # Assuming Orders is your SQLAlchemy model

    # Pass the data to the HTML template
    return render_template('attendancereport.html', attendance_data=attendance_data, report_type='Attendance Report')


#=================Download CSV Route=========================

@app.route('/download_csv_details', methods=['POST'])
def download_csv_details():
    if request.method == 'POST':
        # Fetch data from the database (assuming you have a method to do this)
        details_data = Details.query.all()  # Assuming Details is your SQLAlchemy model

        if not details_data:
            return "No data found to generate CSV", 404  # Not found

        try:
            # Convert data to CSV format
            csv_buffer = StringIO()
            csv_writer = csv.writer(csv_buffer)

            # Write CSV headers
            csv_writer.writerow(['order_id', 'amount', 'profit', 'quantity', 'category', 'sub_category', 'paymentMode'])

            # Write data rows
            for row in details_data:
                csv_writer.writerow([row.order_id, row.amount, row.profit, row.quantity, row.category, row.sub_category, row.paymentMode])

            # Generate a temporary CSV filename
            # temp_csv_filename = str(uuid.uuid4()) + '.csv'
            temp_csv_filename = 'DetailsReport.csv'
            csv_directory = './csv'

            # Write CSV data to a temporary file in the CSV directory
            with open(os.path.join(csv_directory, temp_csv_filename), 'w', newline='') as csv_file:
                csv_file.write(csv_buffer.getvalue())

            # Return the CSV file as a download
            return send_file(os.path.join(csv_directory, temp_csv_filename), as_attachment=True)

        except Exception as e:
            return f"Error generating CSV: {str(e)}", 500  # Internal server error

    else:
        return "Method not allowed", 405  # Method not allowed


@app.route('/download_csv_orders', methods=['POST'])
@login_required
def download_csv_orders():
    # Fetch data from the Orders table
    orders_data = Orders.query.all()

    if not orders_data:
        return "No data found to generate CSV", 404  # Not found

    try:
        # Create a StringIO object to write CSV data
        csv_buffer = StringIO()
        csv_writer = csv.writer(csv_buffer)

        # Write CSV headers
        csv_writer.writerow(['Order_ID', 'Order_Date', 'CustomerName', 'State', 'City'])

        # Write data rows
        for order in orders_data:
            csv_writer.writerow([order.Order_ID, order.Order_Date, order.CustomerName, order.State, order.City])

        # Set the StringIO object's cursor position to the beginning
        csv_buffer.seek(0)

        # Create a response object
        response = make_response(csv_buffer.getvalue())
        
        # Set the appropriate Content-Type and Content-Disposition headers
        response.headers['Content-Type'] = 'text/csv'
        response.headers['Content-Disposition'] = 'attachment; filename=orders_report.csv'

        return response

    except Exception as e:
        return f"Error generating CSV: {str(e)}", 500  # Internal server error


@app.route('/download_csv_attendance', methods=['POST'])
@login_required
def download_csv_attendance():
    # Fetch data from the Orders table
    attendance_data = Attendance.query.all()

    if not attendance_data:
        return "No data found to generate CSV", 404  # Not found

    try:
        # Create a StringIO object to write CSV data
        csv_buffer = StringIO()
        csv_writer = csv.writer(csv_buffer)

        # Write CSV headers
        csv_writer.writerow(['Employee_ID', 'Employee_Name', 'Attendance', 'Date', 'Total_Work_Hours', 'City_Name', 'Region', 'State'])

        # Write data rows
        for attendance in attendance_data:
            csv_writer.writerow([attendance.Employee_ID, attendance.Employee_Name, attendance.Attendance, attendance.Date, attendance.Total_Work_Hours, attendance.City_Name, attendance.Region, attendance.State])

        # Set the StringIO object's cursor position to the beginning
        csv_buffer.seek(0)

        # Create a response object
        response = make_response(csv_buffer.getvalue())
        
        # Set the appropriate Content-Type and Content-Disposition headers
        response.headers['Content-Type'] = 'text/csv'
        response.headers['Content-Disposition'] = 'attachment; filename=Attendance_Report.csv'

        return response

    except Exception as e:
        return f"Error generating CSV: {str(e)}", 500  # Internal server error


#=================Forget password=========================

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        user = User.query.filter_by(email=email).first()
        if user:
            token = serializer.dumps(email, salt='password-reset-salt')
            send_email(user.email, token)
            flash('Password reset link sent to your email.')
        else:
            flash('No account found with that email.')
        return redirect(url_for('login'))
    return render_template('forgot_password.html')

def send_email(to_email, token):
    reset_url = url_for('reset_password', token=token, _external=True)
    msg = Message('Password Reset Request',
                  sender='your_email@example.com',
                  recipients=[to_email])
    msg.body = f'Please click the link to reset your password: {reset_url}'
    mail.send(msg)

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    try:
        email = serializer.loads(token, salt='password-reset-salt', max_age=3600)
    except:
        flash('The password reset link is invalid or has expired.')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        new_password = request.form['password']
        hashed_password = generate_password_hash(new_password)
        user = User.query.filter_by(email=email).first()
        if user:
            user.password = hashed_password
            db.session.commit()
            flash('Your password has been updated!')
            return redirect(url_for('login'))
    
    return render_template('reset_password.html', token=token)



def update_password(email, new_password):
    # Implement password update logic here
    print(f'Update password for {email} to {new_password}')


#=================Logout=========================

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


if __name__ == '__main__':
    # with app.app_context():
    #     db.create_all()
    print("Starting the Flask application...")
    app.run(debug=True)
