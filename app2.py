from flask import Flask, render_template, request, redirect, url_for, session
import pyodbc
import os

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', os.urandom(24))  

# Conectare la baza de date folosind autentificare Windows
conn = pyodbc.connect('DRIVER={ODBC Driver 11 for SQL Server};'
                      'SERVER=DESKTOP-EQBM2CM\\SQLEXPRESS;' 
                      'DATABASE=Proiect ( scoala de soferi);'
                      'Trusted_Connection=yes;')

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        print("Am primit o cerere POST")
        username = request.form['username']
        password = request.form['password']

        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Utilizatori WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()

        if user:
            session['username'] = user.username 
            return redirect(url_for('dashboard'))
        else:
            return "Nume utilizator sau parolă incorecte"
    else:
        print("Am primit o cerere GET")
        return render_template('login.html')



@app.route('/dashboard')
def dashboard():
    # Verifică dacă utilizatorul este autentificat
    if 'username' not in session:
        return redirect(url_for('index'))

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Lectii")
    lectii = cursor.fetchall()
    return render_template('dashboard.html', lectii=lectii)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
