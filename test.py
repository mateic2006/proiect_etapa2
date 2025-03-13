import pyodbc

# Listează toți driverii ODBC disponibili pe sistem
drivers = pyodbc.drivers()
print("Driverele ODBC disponibile:")
for driver in drivers:
    print(driver)