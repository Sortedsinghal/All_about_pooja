from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

def init_db():
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()
    c.execute('DROP TABLE IF EXISTS products')
    c.execute('CREATE TABLE products (id INTEGER PRIMARY KEY, name TEXT, category TEXT)')

    product_data = [
        ("YSL👠", "Heels👠"),
        ("Christian louboutin👠", "Heels👠"),
        ("Mach and Mach👠", "Heels👠"),
        ("Cesare Paciotti👠", "Heels👠"),
        ("Tulips🌷", "Flowers💐"),
        ("Rose🌹", "Flowers💐"),
        ("Sunflower🌻", "Flowers💐"),
        ("Daisy🌼", "Flowers💐"),
        ("Marigold🏵️", "Flowers💐"),
        ("Lily🌸", "Flowers💐"),
        ("Hazelnut🍫", "Chocolates🍫"),
        ("Crackle🍫", "Chocolates🍫"),
        ("Roasted Almonds🍫", "Chocolates🍫"),
        ("Bournville 70% Dark🍫", "Chocolates🍫"),
        ("Ferrero Rocher🍫", "Chocolates🍫"),
        ("Charlotte Tilbury💄", "MakeUp💄"),
        ("YSL💄", "MakeUp💄"),
        ("Huda Beauty💄", "MakeUp💄"),
        ("Fendy Beauty💄", "MakeUp💄"),
        ("MAC💄", "MakeUp💄"),
        ("Dior💄", "MakeUp💄"),
        ("Chanel💄", "MakeUp💄"),
        ("Switzerland🇨🇭", "Country🌎"),
        ("Japan🇯🇵", "Country🌎"),
        ("Golden Retriever🐾", "Dog🐕"),
        ("Rolls Royce🚘", "Car🏎️"),
        ("Porsche🏎️", "Car🏎️"),
        ("Sweet Lime (Saravana Bhavan) 🍋‍🟩", "Drinks🥤"),
        ("Peach iced tea (Bistro 57) 🥤", "Drinks🥤"),
        ("Cold Coffee☕️", "Drinks🥤"),
        ("Butter Chicken🍗", "Food🥘"),
        ("KFC🍗", "Food🥘"),
        ("Rajma Chawal🫘", "Food🥘"),
        ("Chicken Biryani🍗", "Food🥘"),
        ("Shahi Pista (Mother Dairy)🍦", "Ice Cream🍨"),
        ("Hocco🍨", "Ice Cream🍨"),
        ("Sephora💸", "MakeUp Brand💄"),
        ("Chicken Biryani🍗", "Food🥘"),
        ("Chicken Biryani🍗", "Food🥘"),
        ("Chicken Biryani🍗", "Food🥘"),
        ("Navy Blue💙", "Colour🖍️"),
        ("Cherry Red♥️", "Colour🖍️"),
        ("Silver Watch⌚️", "Watch⌚️"),
        ("Penguin🐧", "Stuff Toy🧸"),
        ("Jon Snow🤺", "GOT Character⚔️"),
        ("Dyson🎀", "Hair Dryer"),
        ("Moh Moh ke Dhaage🧵", "Song🎶"),
        ("Momo🥟", "Nickname🥰"),
        ("Sloth Bear🐻", "Nickname🥰"),
        ("Pooju🎀", "Nickname🥰"),
        ("Poojli🎀", "Nickname🥰"),
        ("Princess👸", "Nickname🥰"),
        ("Rainbow🌈", "Nickname🥰"),
        ("Batwoman🦇", "Nickname🥰"),
        ("Catwoman🐈‍⬛", "Nickname🥰"),
        ("Darling🎀", "Nickname🥰"),
        ("Baby❤️", "Nickname🥰"),
        ("Bubu🍼", "Nickname🥰"),
        ("Sweetheart❤️", "Nickname🥰"),
        ("Kuchu Puchu🥰", "Nickname🥰"),
        ("Cupcake🧁", "Nickname🥰"),
        ("Moonpie🌕", "Nickname🥰"),
        ("Moonlight🌙", "Nickname🥰"),
        ("Munchkin😚", "Nickname🥰")
        ]
    for name, category in product_data:
        c.execute('INSERT INTO products (name, category) VALUES (?, ?)', (name, category))

    conn.commit()
    conn.close()

init_db()

@app.route('/api/chat', methods=['POST'])
def chat():
    user_input = request.json['message'].strip().lower()

    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()

    if user_input in ['show all', 'show products', 'list all']:
        c.execute("SELECT name FROM products")
        matches = c.fetchall()
    else:
        # Try exact match first
        c.execute("""
            SELECT name FROM products
            WHERE LOWER(name) = ? OR LOWER(category) = ?
        """, (user_input, user_input))
        matches = c.fetchall()

        # If no exact matches, fall back to partial match
        if not matches:
            c.execute("""
                SELECT name FROM products
                WHERE LOWER(name) LIKE ? OR LOWER(category) LIKE ?
            """, (f"%{user_input}%", f"%{user_input}%"))
            matches = c.fetchall()

    conn.close()

    if matches:
        reply = "Here are some matching products:\n" + "\n".join([row[0] for row in matches])
    else:
        reply = "Sorry, I couldn’t find any matching products."

    return jsonify({'reply': reply})

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
