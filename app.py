import pyodbc

# Conectare la baza de date folosind autentificare Windows și ODBC Driver 11 for SQL Server
conn = pyodbc.connect('DRIVER={ODBC Driver 11 for SQL Server};'
                      'SERVER=DESKTOP-EQBM2CM\\SQLEXPRESS;'
                      'DATABASE=Proiect ( scoala de soferi);'
                      'Trusted_Connection=yes;')

# Creează cursorul pentru a executa interogări
cursor = conn.cursor()

# Execută o interogare SQL pentru a verifica conexiunea
cursor.execute('SELECT * FROM Utilizatori')

# Parcurge și afișează rezultatele pentru a verifica funcționalitatea conexiunii
for row in cursor.fetchall():
    print(row)

