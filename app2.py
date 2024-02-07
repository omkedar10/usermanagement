from flask import Flask, request, jsonify
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

def get_connection():
    return psycopg2.connect(**my_fpgdb)

@app.route('/api/users', methods=['GET'])
def get_users():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name, dob FROM users")
    users = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(users)

@app.route('/api/users', methods=['POST'])
def create_user():
    data = request.json
    name = data.get('name')
    dob = data.get('dob')

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO users (name, dob) VALUES (%s, %s) RETURNING id", (name, dob))
    new_user_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"message": "User created successfully", "user_id": new_user_id})

@app.route('/api/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.json
    name = data.get('name')
    dob = data.get('dob')

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE users SET name = %s, dob = %s WHERE id = %s", (name, dob, user_id))
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"message": "User updated successfully"})

@app.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM users WHERE id = %s", (user_id,))
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"message": "User deleted successfully"})

if __name__ == '__main__':
    app.run(debug=True)
