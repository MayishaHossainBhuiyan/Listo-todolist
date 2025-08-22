from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Set a secret key for session management
app.secret_key = 'your_secret_key'

# Dummy database for users (You can replace this with a real database later)
users_db = {
    "admin": {"password": generate_password_hash("admin123"), "role": "admin"},
    "user1": {"password": generate_password_hash("user123"), "role": "user"},
     "Mayisha": {"password": generate_password_hash("mayisha123"), "role": "user"},
    "Yeasin": {"password": generate_password_hash("yeasin123"), "role": "user"},
    "Kafi": {"password": generate_password_hash("kafi123"), "role": "user"},
    "Juthi": {"password": generate_password_hash("juthi123"), "role": "user"},
    "Noman": {"password": generate_password_hash("noman123"), "role": "user"}
}

# In-memory "database" for tasks
tasks = {
    "user1": [],
}

@app.route('/')
def index():
    if 'username' in session:
        username = session['username']
        if users_db[username]["role"] == "admin":
            return redirect(url_for('admin_page'))
        return render_template('user_page.html', tasks=tasks.get(username, []))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in users_db and check_password_hash(users_db[username]['password'], password):
            session['username'] = username
            return redirect(url_for('index'))
        else:
            return "Invalid credentials, please try again."

    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = 'user'  # Default role for new users

        if username in users_db:
            return "Username already exists, please choose another one."
        
        # Hash the password before storing it
        users_db[username] = {"password": generate_password_hash(password), "role": role}
        tasks[username] = []  # Initialize empty task list for the new user

        return redirect(url_for('login'))

    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/admin')
def admin_page():
    if 'username' not in session or users_db[session['username']]['role'] != 'admin':
        return redirect(url_for('login'))
    return render_template('admin.html', users=users_db)

@app.route('/add_task', methods=['POST'])
def add_task():
    if 'username' in session:
        task = request.form['task']
        username = session['username']
        if username not in tasks:
            tasks[username] = []
        tasks[username].append(task)
    return redirect(url_for('index'))

@app.route('/delete_task/<int:task_id>')
def delete_task(task_id):
    if 'username' in session:
        username = session['username']
        if 0 <= task_id < len(tasks.get(username, [])):
            tasks[username].pop(task_id)
    return redirect(url_for('index'))

@app.route('/delete_user/<username>')
def delete_user(username):
    if 'username' in session and users_db[session['username']]['role'] == 'admin':
        if username in users_db:
            del users_db[username]
    return redirect(url_for('admin_page'))

if __name__ == '__main__':
    app.run(debug=True)
