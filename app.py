from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import mysql.connector
from mysql.connector import Error
import config

app = Flask(__name__)
app.secret_key = config.Config.SECRET_KEY

# Database connection function
def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host=config.Config.MYSQL_HOST,
            port=config.Config.MYSQL_PORT,
            user=config.Config.MYSQL_USER,
            password=config.Config.MYSQL_PASSWORD,
            database=config.Config.MYSQL_DB
        )
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

# Helper function to execute queries and fetch results
def execute_query(query, params=None, fetch_one=False, fetch_all=False, commit=False):
    connection = get_db_connection()
    if not connection:
        return None
    
    try:
        cursor = connection.cursor(dictionary=True)
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        result = None
        if fetch_one:
            result = cursor.fetchone()
        elif fetch_all:
            result = cursor.fetchall()
        elif commit:
            connection.commit()
            result = cursor.lastrowid
        
        cursor.close()
        connection.close()
        return result
    except Error as e:
        print(f"Error executing query: {e}")
        connection.close()
        return None

# Home page
@app.route('/')
def index():
    recent_notices = execute_query("""
        SELECT * FROM notices 
        WHERE expiry_date IS NULL OR expiry_date >= %s 
        ORDER BY created_at DESC 
        LIMIT 3
    """, (datetime.now().date(),), fetch_all=True)
    
    return render_template('index.html', recent_notices=recent_notices or [])

# About page
@app.route('/about')
def about():
    return render_template('about.html')

# Login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        if session['role'] == 'admin':
            return redirect(url_for('admin_dashboard'))
        else:
            return redirect(url_for('student_dashboard'))
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = execute_query(
            "SELECT * FROM users WHERE username = %s", 
            (username,), 
            fetch_one=True
        )
        
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['role'] = user['role']
            
            if user['role'] == 'admin':
                return redirect(url_for('admin_dashboard'))
            else:
                return redirect(url_for('student_dashboard'))
        else:
            flash('Invalid username or password', 'danger')
    
    return render_template('login.html')

# Signup page
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if 'user_id' in session:
        if session['role'] == 'admin':
            return redirect(url_for('admin_dashboard'))
        else:
            return redirect(url_for('student_dashboard'))
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = "student"
        hashed_password = generate_password_hash(password)
        
        try:
            result = execute_query(
                "INSERT INTO users (username, password, role) VALUES (%s, %s, %s)",
                (username, hashed_password, role),
                commit=True
            )
            
            if result:
                flash('Registration successful! Please login.', 'success')
                return redirect(url_for('login'))
            else:
                flash('Registration failed. Please try again.', 'danger')
        except Exception as e:
            flash('Username already exists', 'danger')
    
    return render_template('signup.html')

# Admin dashboard
@app.route('/admin/dashboard')
def admin_dashboard():
    if 'user_id' not in session or session['role'] != 'admin':
        flash('Please login as admin to access this page', 'danger')
        return redirect(url_for('login'))
    
    total_notices_result = execute_query(
        "SELECT COUNT(*) as total_notices FROM notices", 
        fetch_one=True
    )
    total_notices = total_notices_result['total_notices'] if total_notices_result else 0
    
    recent_notices = execute_query("""
        SELECT notices.*, users.username 
        FROM notices 
        JOIN users ON notices.user_id = users.id 
        ORDER BY notices.created_at DESC 
        LIMIT 5
    """, fetch_all=True)
    
    return render_template('admin_dashboard.html', 
                          total_notices=total_notices,
                          recent_notices=recent_notices or [])

# Add notice
@app.route('/add_notice', methods=['POST'])
def add_notice():
    if 'user_id' not in session or session['role'] != 'admin':
        flash('Please login as admin to perform this action', 'danger')
        return redirect(url_for('login'))
    
    title = request.form['title']
    content = request.form['content']
    category = request.form.get('category', 'general')
    expiry_date = request.form.get('expiry_date')
    user_id = session['user_id']
    
    result = execute_query(
        "INSERT INTO notices (title, content, category, expiry_date, user_id) VALUES (%s, %s, %s, %s, %s)",
        (title, content, category, expiry_date, user_id),
        commit=True
    )
    
    if result:
        flash('Notice published successfully!', 'success')
    else:
        flash('Failed to publish notice. Please try again.', 'danger')
    
    return redirect(url_for('admin_dashboard'))

# Student dashboard
@app.route('/student/dashboard')
def student_dashboard():
    if 'user_id' not in session or session['role'] != 'student':
        flash('Please login as student to access this page', 'danger')
        return redirect(url_for('login'))
    
    notices = execute_query("""
        SELECT * FROM notices 
        WHERE expiry_date IS NULL OR expiry_date >= %s 
        ORDER BY created_at DESC
    """, (datetime.now().date(),), fetch_all=True)
    
    return render_template('student_dashboard.html', notices=notices or [])

# View a specific notice
@app.route('/notice/<int:notice_id>')
def view_notice(notice_id):
    if 'user_id' not in session:
        flash('Please login to view this notice', 'danger')
        return redirect(url_for('login'))
    
    notice = execute_query("""
        SELECT notices.*, users.username 
        FROM notices 
        JOIN users ON notices.user_id = users.id 
        WHERE notices.id = %s
    """, (notice_id,), fetch_one=True)
    
    if not notice:
        flash('Notice not found', 'danger')
        if session.get('role') == 'student':
            return redirect(url_for('student_dashboard'))
        else:
            return redirect(url_for('admin_dashboard'))
    
    return render_template('view_notice.html', notice=notice)

# Logout
@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out successfully', 'info')
    return redirect(url_for('index'))

# Error handlers
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)