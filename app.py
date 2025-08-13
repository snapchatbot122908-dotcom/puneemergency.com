from flask import Flask, render_template, request, redirect, url_for, session
from data import contacts
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
template_dir = os.path.join(BASE_DIR, 'templates')
static_dir = os.path.join(BASE_DIR, 'static')

app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
app.secret_key = 'supersecretkey'

ADMIN_USER = "Aniket Gokul Abhang"
ADMIN_PASS = "Jiv@2908"

@app.route('/')
def index():
    search = request.args.get('search', '').lower()
    category = request.args.get('category', 'All')

    filtered = contacts
    if category != 'All':
        filtered = [c for c in filtered if c['category'] == category]
    if search:
        filtered = [c for c in filtered if search in c['name'].lower() or search in c['category'].lower()]

    categories = ["All"] + sorted(list(set(c['category'] for c in contacts)))
    return render_template('index.html', contacts=filtered, categories=categories, active_cat=category, search=search)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == ADMIN_USER and password == ADMIN_PASS:
            session['admin_logged_in'] = True
            return redirect(url_for('admin_panel'))
        else:
            return render_template('admin.html', error="Invalid credentials")
    return render_template('admin.html')

@app.route('/admin/panel')
def admin_panel():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin'))
    return render_template('admin_panel.html', contacts=contacts)

@app.route('/logout')
def logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)