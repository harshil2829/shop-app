from flask import Flask, render_template, redirect, session, request
import sqlite3

app = Flask(__name__)
app.secret_key = "secret123"


# Initialize DB
def init_db():
    conn = sqlite3.connect("shop.db")
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS products(
        id INTEGER PRIMARY KEY,
        name TEXT,
        price INTEGER
    )
    """)

    # Insert sample products
    c.execute("SELECT COUNT(*) FROM products")
    if c.fetchone()[0] == 0:

        products = [
            ("Laptop", 50000),
            ("Mobile", 20000),
            ("Headphones", 2000),
            ("Keyboard", 1500)
        ]

        c.executemany(
            "INSERT INTO products(name,price) VALUES(?,?)",
            products
        )

    conn.commit()
    conn.close()


@app.route("/")
def index():

    conn = sqlite3.connect("shop.db")
    c = conn.cursor()

    c.execute("SELECT * FROM products")
    data = c.fetchall()

    conn.close()

    return render_template("index.html", products=data)


@app.route("/add/<int:id>")
def add(id):

    cart = session.get("cart", [])
    cart.append(id)

    session["cart"] = cart

    return redirect("/")


@app.route("/cart")
def cart():

    cart = session.get("cart", [])

    conn = sqlite3.connect("shop.db")
    c = conn.cursor()

    items = []

    for pid in cart:
        c.execute("SELECT * FROM products WHERE id=?", (pid,))
        items.append(c.fetchone())

    conn.close()

    total = sum(i[2] for i in items)

    return render_template(
        "cart.html",
        items=items,
        total=total
    )


@app.route("/checkout")
def checkout():

    session.clear()

    return render_template("checkout.html")


if __name__ == "__main__":

    init_db()
    app.run(debug=True)
