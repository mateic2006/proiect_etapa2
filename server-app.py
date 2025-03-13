from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import pyodbc
import os

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', os.urandom(24))  

# Conectare la baza de date folosind autentificare Windows
conn = pyodbc.connect('DRIVER={ODBC Driver 18 for SQL Server};'
                      'SERVER=DESKTOP-RKGB73S;' 
                      'DATABASE=Proiect ( Scoala de soferi1);'
                      'Trusted_Connection=yes;'
                      'TrustServerCertificate=yes;')

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
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
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Get form data
        cnp_elev = request.form['cnp_elev']
        nume = request.form['nume']
        prenume = request.form['prenume']
        telefon = request.form['telefon']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        rol = "instructor" if 'switch' in request.form else "elev"

        cursor = conn.cursor()
        try:
            # Insert into Utilizatori table
            cursor.execute("""
                INSERT INTO Utilizatori (username, password, rol) 
                OUTPUT INSERTED.id_utilizator
                VALUES (?, ?, ?)
            """, (username, password, rol))

            # Get the id_utilizator of the newly inserted user
            id_utilizator = cursor.fetchone()[0]
            print(id_utilizator)
            if rol == "elev":
                # Insert into Elevi table
                data_nasterii = request.form['data_nasterii']
                cursor.execute("""
                    INSERT INTO Elevi (cnp_elev, nume, prenume, data_nasterii, telefon, email, id_utilizator) 
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (cnp_elev, nume, prenume, data_nasterii, telefon, email, id_utilizator))
            else:
                # Insert into Instructori table
                ani_experienta = request.form.get('ani_experienta', None)
                if not ani_experienta:
                    return "Ani experienta is required for instructors"
                cursor.execute("""
                    INSERT INTO Instructori (cnp_instructor, nume, prenume, telefon, email, ani_experienta, id_utilizator) 
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                 """, (cnp_elev, nume, prenume, telefon, email, ani_experienta, id_utilizator))

            conn.commit()
            return redirect(url_for('login'))
        except pyodbc.Error as e:
            conn.rollback()
            return f"Eroare la înregistrare: {str(e)}"

    return render_template('signup.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'username' not in session:
        return redirect(url_for('index'))

    username = session['username']
    tabel = 'Lectii'  # Tabelul implicit
    coloane = []
    rezultate = []

    if request.method == 'POST':
        tabel = request.form.get('tabel', 'Lectii')
        coloane = request.form.getlist('coloane')

        if coloane:
            coloane_str = ', '.join(coloane)
            cursor = conn.cursor()
            cursor.execute(f"SELECT {coloane_str} FROM {tabel}")
            rows = cursor.fetchall()
            rezultate = [dict(zip(coloane, [str(cell) for cell in row])) for row in rows]
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({
                    'status': 'success',
                    'rezultate': rezultate,
                    'coloane': coloane
                })

    return render_template('dashboard.html', username=username, tabel=tabel, coloane=coloane, rezultate=rezultate)

@app.route('/verify-email', methods=['POST'])
def verify_email():
    email = request.form['email']
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Elevi WHERE email = ?", (email,))
    user = cursor.fetchone()
    return {'exists': user is not None}

@app.route('/reset', methods=['GET', 'POST'])
def reset_password():
    if request.method == 'POST':
        if 'new_password' in request.form:
            email = request.form['email']
            new_password = request.form['new_password']
            confirm_password = request.form['confirm_password']

            if new_password != confirm_password:
                return "Passwords do not match"

            cursor = conn.cursor()
            try:
                cursor.execute("""
                    UPDATE Utilizatori
                    SET password = ?
                    FROM Utilizatori u
                    JOIN Elevi e ON u.id_utilizator = e.id_utilizator
                    WHERE e.email = ?
                """, (new_password, email))

                conn.commit()
                return redirect(url_for('login'))
            except pyodbc.Error as e:
                conn.rollback()
                return f"Eroare la resetarea parolei: {str(e)}"

    return render_template('reset.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

# Add a new route for menu toggle
@app.route('/toggle-menu', methods=['POST'])
def toggle_menu():
    return {'status': 'success'}

@app.route('/delete', methods=['GET', 'POST'])
def delete_account():
    if request.method == 'POST':
        identifier = request.json.get('identifier')
        cursor = conn.cursor()

        try:
            # Check if the identifier is either a username or email, and get id_utilizator using subqueries
            cursor.execute("""
                SELECT id_utilizator 
                FROM Utilizatori 
                WHERE username = ? 
                UNION 
                SELECT id_utilizator 
                FROM Instructori 
                WHERE email = ? 
                UNION 
                SELECT id_utilizator 
                FROM Elevi 
                WHERE email = ?
            """, (identifier, identifier, identifier))
            user = cursor.fetchone()

            if user:
                user_id = user[0]
                # Check if the user is an instructor and delete from Instructori if found
                cursor.execute("SELECT 1 FROM Instructori WHERE id_utilizator = ?", (user_id,))
                instructor = cursor.fetchone()
                if instructor:
                    cursor.execute("DELETE FROM Instructori WHERE id_utilizator = ?", (user_id,))

                # Check if the user is a student and delete from Elevi if found
                cursor.execute("SELECT 1 FROM Elevi WHERE id_utilizator = ?", (user_id,))
                student = cursor.fetchone()
                if student:
                    cursor.execute("DELETE FROM Elevi WHERE id_utilizator = ?", (user_id,))

                # delete from Utilizatori table
                cursor.execute("DELETE FROM Utilizatori WHERE id_utilizator = ?", (user_id,))
                conn.commit()
                
                return {'success': True}

            else:
                return {'success': False, 'error': 'User not found'}

        except Exception as e:
            return {'success': False, 'error': str(e)}
    return render_template('delete.html')

@app.route('/simple-query/<int:query_number>')
def simple_query(query_number):
    with conn.cursor() as cursor:
        # Interogări simple (JOIN între două sau mai multe tabele)
        queries = {
            # Elevii și instructorii care au predat lecții împreună:
            1: """
                SELECT e.nume, e.prenume, i.nume AS nume_instructor, i.prenume AS prenume_instructor
                FROM Elevi e
                JOIN Lectii l ON e.cnp_elev = l.cnp_elev
                JOIN Instructori i ON l.cnp_instructor = i.cnp_instructor;

                """,
            # Data lecției, marca și modelul vehiculului pentru fiecare lecț
            2: """
                SELECT L.data_lectie, V.marca, V.model
                FROM Lectii L
                JOIN Vehicule V ON L.serie_sasiu = V.serie_sasiu
                """,
            # Numărul de lecții predate de fiecare instructor
            3: """
                SELECT I.nume, COUNT(L.id_lectie) AS numar_lectii
                FROM Instructori I
                JOIN Lectii L ON I.cnp_instructor = L.cnp_instructor
                GROUP BY I.nume
                """,
            # Suma plătită de fiecare elev și data plății
            4: """
                SELECT E.nume, E.prenume, P.suma, P.data_plata
                FROM Elevi E
                JOIN Plati P ON E.cnp_elev = P.cnp_elev
                """,
            # Numele instructorului și marca și modelul vehiculului pe care îl folosește
            5: """
                SELECT I.nume, V.marca, V.model
                FROM Instructori I
                JOIN Instructori_Vehicule IV ON I.cnp_instructor = IV.cnp_instructor
                JOIN Vehicule V ON IV.serie_sasiu = V.serie_sasiu
                """,
            # Rating-urile lăsate de elevi pentru instructori
            6: """
                SELECT R.rating, E.nume, I.nume
                FROM Recenzii R
                JOIN Elevi E ON R.cnp_elev = E.cnp_elev
                JOIN Instructori I ON R.cnp_instructor = I.cnp_instructor
                """
        }

        cursor.execute(queries.get(query_number, ""))
        results = cursor.fetchall()

        # Conversia rezultatelor în JSON
        return jsonify([dict(zip([column[0] for column in cursor.description], row)) for row in results])

@app.route('/complex-query/<int:query_number>')
def complex_query(query_number):
    with conn.cursor() as cursor:
        # Interogări complexe (subinterogări)
        complex_queries = {
            # Numărul total de lecții predate de fiecare instructor:
            1: """
                SELECT I.nume, 
                (SELECT COUNT(*) 
                 FROM Lectii L 
                 WHERE L.cnp_instructor = I.cnp_instructor) AS total_lectii
                FROM Instructori I
                """,
            # Elevii care nu au lăsat recenzii:
            2: """
                SELECT e.nume, e.prenume
                FROM Elevi e
                WHERE NOT EXISTS (SELECT 1 FROM Recenzii r WHERE r.cnp_elev = e.cnp_elev);
                """,
            # Interogare care returnează numele instructorilor care au predat cel puțin o lecție
            3: """
                SELECT V.marca, COUNT(L.id_lectie) AS numar_lectii
                FROM Vehicule V
                JOIN Lectii L ON V.serie_sasiu = L.serie_sasiu
                GROUP BY V.marca
                HAVING COUNT(L.id_lectie) >= 1
                """,
            # Instructorii cu cea mai mare medie a rating-urilor primite:
            4: """
                SELECT i.nume, i.prenume
                FROM Instructori i
                WHERE i.cnp_instructor IN (
                    SELECT r.cnp_instructor
                    FROM Recenzii r
                    WHERE r.rating = (SELECT MAX(rating) FROM Recenzii)
                );
                """
        }

        cursor.execute(complex_queries.get(query_number, ""))
        results = cursor.fetchall()

        # Conversia rezultatelor în JSON
        return jsonify([dict(zip([column[0] for column in cursor.description], row)) for row in results])

@app.route('/interogari')
def interogari():
    return render_template('interogari.html')

if __name__ == "__main__":
    app.run(debug=True)
