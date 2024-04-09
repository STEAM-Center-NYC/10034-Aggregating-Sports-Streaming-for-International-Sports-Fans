from flask import Flask, render_template, jsonify
import sqlite3

app = Flask(__name__)

# Function to retrieve information from the database
def get_information_from_database():
    conn = sqlite3.connect('your_database.db')  # Replace 'your_database.db' with your database file
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM your_table')  # Replace 'your_table' with your table name
    rows = cursor.fetchall()
    conn.close()
    return rows

@app.route('/get_information', methods=['GET'])
def get_information():
    information = get_information_from_database()
    return jsonify(information)

if __name__ == '__main__':
    app.run(debug=True)
