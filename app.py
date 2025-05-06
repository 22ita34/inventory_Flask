from flask import Flask, render_template, request, redirect , url_for
import mysql.connector

app = Flask(__name__)

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Ajish@2004',
    'database': 'inventory'
}

def db_conn():
    conn = mysql.connector.connect(**db_config)
    return conn, conn.cursor(dictionary=True)

# Home Route
@app.route('/')
def dashboard():
    conn, cursor = db_conn()

    cursor.execute("SELECT COUNT(*) AS count FROM product")
    product_count = cursor.fetchone()['count']

    cursor.execute("SELECT COUNT(*) AS count FROM location")
    location_count = cursor.fetchone()['count']

    # cursor.execute("SELECT COUNT(*) AS count FROM product_movements")  # Adjust table name if different
    # movement_count = cursor.fetchone()['count']

    cursor.close()
    conn.close()

    return render_template('dashboard.html', 
        product_count=product_count,
        location_count=location_count
        # movement_count=movement_count
    )

@app.route('/product')
def view_product():
    # Establish database connection
    conn, cursor = db_conn()
    
    cursor.execute("SELECT * FROM product")
    items = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return render_template('view_product.html', items=items)

@app.route('/location')
def view_location():
    conn, cursor = db_conn()
    cursor.execute("SELECT * FROM location")
    locations = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('view_location.html', locations=locations)

# Add Product Route
@app.route('/add-product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        product_name = request.form['product_name']
        price = request.form['price']
        quantity = request.form['quantity']

        conn, cursor = db_conn()
        query = "INSERT INTO product (product_name, price, quantity) VALUES (%s, %s, %s)"
        values = (product_name, price, quantity)
        cursor.execute(query, values)
        conn.commit()
        cursor.close()
        conn.close()

        return redirect('/product')  # Redirect back to view products

    return render_template('add_product.html')

@app.route('/edit-product/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    conn, cursor = db_conn()
    
    if request.method == 'POST':
        # Get updated data from the form
        product_name = request.form['product_name']
        price = request.form['price']
        quantity = request.form['quantity']
        
        # Update product in the database
        cursor.execute("""
            UPDATE product
            SET product_name = %s, price = %s, quantity = %s
            WHERE product_id = %s
        """, (product_name, price, quantity, product_id))
        conn.commit()

        return redirect('/product')
    
    # Fetch the product details to prefill the form
    cursor.execute("SELECT * FROM product WHERE product_id = %s", (product_id,))
    product = cursor.fetchone()
    
    cursor.close()
    conn.close()
    
    return render_template('edit_product.html', product=product)

@app.route('/add-location', methods=['GET', 'POST'])
def add_location():
    if request.method == 'POST':
        # Extract data from form
        location_name = request.form['location_name']
        address = request.form['address']
        city = request.form['city']
        state = request.form['state']
        country = request.form['country']
        postal_code = request.form['postal_code']
        
        # Database insertion (assuming a connection function exists)
        conn, cursor = db_conn()
        cursor.execute('''
            INSERT INTO location (location_name, address, city, state, country, postal_code)
            VALUES (%s, %s, %s, %s, %s, %s)
        ''', (location_name, address, city, state, country, postal_code))
        conn.commit()
        cursor.close()
        conn.close()

        return redirect('/location')  # Redirect to view locations page

    return render_template('add_location.html')

@app.route('/edit-location/<int:location_id>', methods=['GET', 'POST'])
def edit_location(location_id):
    conn, cursor = db_conn()

    if request.method == 'POST':
        # Get form data
        location_name = request.form['location_name']
        address = request.form['address']
        city = request.form['city']
        state = request.form['state']
        country = request.form['country']
        postal_code = request.form['postal_code']

        # Update location in the database
        update_query = """UPDATE location 
                          SET location_name = %s, address = %s, city = %s, state = %s, country = %s, postal_code = %s 
                          WHERE location_id = %s"""
        cursor.execute(update_query, (location_name, address, city, state, country, postal_code, location_id))
        conn.commit()

        # Close the connection
        cursor.close()
        conn.close()

        return redirect(url_for('view_location'))

    else:
        # Fetch current location data (using correct table name "location")
        cursor.execute("SELECT * FROM location WHERE location_id = %s", (location_id,))
        location = cursor.fetchone()

        cursor.close()
        conn.close()

        return render_template('edit_location.html', location=location)

@app.route("/add_movement", methods=["GET", "POST"])
def add_movement():
    conn, cursor = db_conn()

    # Fetch products and locations from the database
    cursor.execute("SELECT product_id, product_name FROM product")
    products = cursor.fetchall()

    cursor.execute("SELECT location_id, location_name FROM location")
    locations = cursor.fetchall()

    cursor.close()
    conn.close()

    if request.method == "POST":
        product_id = request.form["product_id"]
        movement_type = request.form["movement_type"]
        quantity = request.form["quantity"]
        from_location = request.form["from_location"]
        to_location = request.form["to_location"]
        remarks = request.form["remarks"]

        conn, cursor = db_conn()
        cursor.execute("""
            INSERT INTO product_movement (product_id, movement_type, quantity, from_location, to_location, remarks)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (product_id, movement_type, quantity, from_location, to_location, remarks))
        conn.commit()

        cursor.close()
        conn.close()

        return redirect(url_for("add_movement"))

    return render_template("add_movement.html", products=products, locations=locations)

@app.route("/movement")
def movement():
    # Retrieve movement history from the database
    conn, cursor = db_conn()
    cursor.execute("""
        SELECT pm.movement_id, pm.product_id, pm.movement_type, pm.quantity, 
               pm.from_location, pm.to_location, pm.movement_date
        FROM product_movement pm
        ORDER BY pm.movement_date DESC
    """)
    history = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template("view_movement.html", history=history)

if __name__ == '__main__':
    app.run(debug=True)
