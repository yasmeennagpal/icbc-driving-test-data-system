import pyodbc

# Connection string with encryption disabled
conn = pyodbc.connect(
    'DRIVER={ODBC Driver 18 for SQL Server};'
    'SERVER=YASMEEN28;'
    'DATABASE=ICBC_DrivingTests;'
    'Trusted_Connection=yes;'
    'Encrypt=no;'
)

cursor = conn.cursor()

# Test query
cursor.execute("SELECT * FROM DrivingTests")
rows = cursor.fetchall()

for row in rows:
    print(row)

conn.close()

def add_driving_test(driver_license, test_date, location, examiner_id, result, error_count):
    import pyodbc

    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 18 for SQL Server};'
        'SERVER=YASMEEN28;'
        'DATABASE=ICBC_DrivingTests;'
        'Trusted_Connection=yes;'
        'Encrypt=no;'
    )
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO DrivingTests
        (DriverLicenseNumber, TestDate, TestLocation, ExaminerID, Result, ErrorCount)
        VALUES (?, ?, ?, ?, ?, ?)
    """, driver_license, test_date, location, examiner_id, result, error_count)

    conn.commit()
    conn.close()
    print(f"Driving test for {driver_license} added successfully!")

def get_all_driving_tests():
    import pyodbc

    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 18 for SQL Server};'
        'SERVER=YASMEEN28;'
        'DATABASE=ICBC_DrivingTests;'
        'Trusted_Connection=yes;'
        'Encrypt=no;'
    )
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM DrivingTests")
    rows = cursor.fetchall()
    
    for row in rows:
        print(row)
    
    conn.close()

def get_tests_by_result(result):
    import pyodbc

    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 18 for SQL Server};'
        'SERVER=YASMEEN28;'
        'DATABASE=ICBC_DrivingTests;'
        'Trusted_Connection=yes;'
        'Encrypt=no;'
    )
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM DrivingTests WHERE Result = ?", result)
    rows = cursor.fetchall()
    
    for row in rows:
        print(row)
    
    conn.close()

# Example:
# get_tests_by_result('FAIL')

