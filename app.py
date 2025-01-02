from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import requests
from datetime import datetime
import os
from dotenv import load_dotenv
import logging
import sys

# Configurazione logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

load_dotenv()

app = Flask(__name__)
# Configurazione CORS per accettare richieste da qualsiasi origine
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Configurazione del database
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///wallet.db')
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

logger.info(f"Connecting to database: {DATABASE_URL}")

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modello User
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    btc_amount = db.Column(db.Float, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

def init_db():
    """Inizializza il database e crea gli utenti iniziali"""
    try:
        logger.info("Creating database tables...")
        db.create_all()
        
        # Inserimento degli utenti iniziali se il database è vuoto
        if not User.query.first():
            logger.info("Initializing database with default users...")
            alessandro = User(username='Alessandro', btc_amount=0.001, is_admin=False)
            andrea = User(username='Andrea', btc_amount=0.001, is_admin=False)
            admin = User(username='Admin', btc_amount=0.0045, is_admin=True)
            
            db.session.add(alessandro)
            db.session.add(andrea)
            db.session.add(admin)
            db.session.commit()
            logger.info("Default users created successfully")
        else:
            logger.info("Database already contains users")
    except Exception as e:
        logger.error(f"Error initializing database: {str(e)}")
        raise

def get_btc_price():
    """Ottiene il prezzo attuale del Bitcoin in USD"""
    try:
        response = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd')
        price = response.json()['bitcoin']['usd']
        logger.info(f"Current BTC price: ${price}")
        return price
    except Exception as e:
        logger.error(f"Error fetching BTC price: {str(e)}")
        return None

@app.route('/', methods=['GET'])
def home():
    try:
        db_status = "connected" if db.session.is_active else "disconnected"
    except:
        db_status = "error"
    
    return jsonify({
        "message": "Bitcoin Wallet API", 
        "status": "running",
        "database_status": db_status,
        "endpoints": {
            "users": "/api/users",
            "wallet_info": "/api/wallet-info"
        }
    })

@app.route('/api/users', methods=['GET'])
def get_users():
    try:
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
        
        logger.info(f"Retrieved {len(users_data)} users")
        return jsonify(users_data)
    except Exception as e:
        logger.error(f"Error getting users: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/wallet-info', methods=['GET'])
def get_wallet_info():
    try:
        btc_price = get_btc_price()
        total_btc = sum(user.btc_amount for user in User.query.all())
        total_usd = total_btc * btc_price if btc_price else 0
        
        logger.info(f"Wallet info - Total BTC: {total_btc}, Price: ${btc_price}, Total USD: ${total_usd}")
        return jsonify({
            'total_btc': total_btc,
            'btc_price': btc_price,
            'total_usd_value': total_usd
        })
    except Exception as e:
        logger.error(f"Error getting wallet info: {str(e)}")
        return jsonify({"error": str(e)}), 500

# Inizializzazione del database
with app.app_context():
    try:
        init_db()
    except Exception as e:
        logger.error(f"Failed to initialize database: {str(e)}")

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8000))
    logger.info(f"Starting server on port {port}")
    app.run(host='0.0.0.0', port=port) 