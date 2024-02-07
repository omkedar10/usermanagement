from flask import Flask, render_template, redirect, url_for, request, jsonify
import psycopg2

app = Flask(__name__)

# PostgreSQL connection parameters
my_fpgdb = {
    'dbname': 'my_fpgdb',
    'user': 'postgres',
    'password': 'localhost',
    'host': 'localhost',
    'port': '5432'
}

@app.route('/')
def display_users():
    # Fetch data from the database
    with psycopg2.connect(**my_fpgdb) as conn, conn.cursor() as cur:
        cur.execute("SELECT * FROM users;")
        data = cur.fetchall()

    return render_template('index.html', data=data)

@app.route('/api/insert', methods=['POST'])
def insert_data():
    data = request.json  # Assuming JSON data is sent in the request body

    # Extract data from the JSON payload
    name = data.get('name')
    dob = data.get('dob')

    # Insert data into the database
    with psycopg2.connect(**my_fpgdb) as conn, conn.cursor() as cur:
        cur.execute("INSERT INTO users (name, dob) VALUES (%s, %s);", (name, dob))

    return jsonify({"message": "Data inserted successfully"})

@app.route('/api/edit/<int:user_id>', methods=['PUT'])
def edit_user(user_id):
    data = request.json  # Assuming JSON data is sent in the request body

    # Extract data from the JSON payload
    name = data.get('name')
    dob = data.get('dob')

    # Update data in the database
    with psycopg2.connect(**my_fpgdb) as conn, conn.cursor() as cur:
        cur.execute("UPDATE users SET name = %s, dob = %s WHERE id = %s;", (name, dob, user_id))

    return jsonify({"message": "Data updated successfully"})

@app.route('/api/delete/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    # Delete data from the database
    with psycopg2.connect(**my_fpgdb) as conn, conn.cursor() as cur:
        cur.execute("DELETE FROM users WHERE id = %s;", (user_id,))

    return jsonify({"message": "User deleted successfully"})

if __name__ == '__main__':
    app.run(debug=True)
