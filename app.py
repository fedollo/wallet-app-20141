from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import requests
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
# Configurazione CORS per accettare richieste da qualsiasi origine
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Configurazione del database
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///wallet.db')
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modello User
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    btc_amount = db.Column(db.Float, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

# Creazione delle tabelle
with app.app_context():
    db.create_all()
    
    # Inserimento degli utenti iniziali se il database è vuoto
    if not User.query.first():
        alessandro = User(username='Alessandro', btc_amount=0.001, is_admin=False)
        andrea = User(username='Andrea', btc_amount=0.001, is_admin=False)
        admin = User(username='Admin', btc_amount=0.0045, is_admin=True)
        
        db.session.add(alessandro)
        db.session.add(andrea)
        db.session.add(admin)
        db.session.commit()

def get_btc_price():
    """Ottiene il prezzo attuale del Bitcoin in USD"""
    try:
        response = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd')
        return response.json()['bitcoin']['usd']
    except:
        return None

@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Bitcoin Wallet API", "status": "running"})

@app.route('/api/users', methods=['GET'])
def get_users():
    users = User.query.all()
    btc_price = get_btc_price()
    
    users_data = []
    for user in users:
        user_data = {
            'username': user.username,
            'btc_amount': user.btc_amount,
            'usd_value': user.btc_amount * btc_price if btc_price else 0,
            'is_admin': user.is_admin
        }
        users_data.append(user_data)
    
    return jsonify(users_data)

@app.route('/api/wallet-info', methods=['GET'])
def get_wallet_info():
    btc_price = get_btc_price()
    total_btc = sum(user.btc_amount for user in User.query.all())
    
    return jsonify({
        'total_btc': total_btc,
        'btc_price': btc_price,
        'total_usd_value': total_btc * btc_price if btc_price else 0
    })

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8000))
    app.run(host='0.0.0.0', port=port) 