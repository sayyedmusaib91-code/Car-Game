import psycopg2
from psycopg2.extras import DictCursor

# PostgreSQL Local Configuration
DB_HOST = "localhost"
DB_NAME = "carclash_db"
DB_USER = "postgres"
DB_PASS = "admin123"
DB_PORT = "5432"

def get_db_connection():
    """PostgreSQL Database connection return karta hai."""
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        port=DB_PORT,
        cursor_factory=DictCursor
    )
    return conn

def init_db():
    """Drivers/Users aur Race Results tables create karta hai."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 1. Drivers Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS drivers (
            id SERIAL PRIMARY KEY,
            phone VARCHAR(20) UNIQUE NOT NULL,
            username VARCHAR(50) UNIQUE NOT NULL,
            password TEXT NOT NULL,
            player_id VARCHAR(50) UNIQUE NOT NULL,
            level INT DEFAULT 1,
            total_score INT DEFAULT 0,
            coins INT DEFAULT 1000,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    ''')

    # 2. Race Results Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS race_results (
            id SERIAL PRIMARY KEY,
            user_id INT NOT NULL REFERENCES drivers (id) ON DELETE CASCADE,
            position INT,
            score INT NOT NULL,
            coins_earned INT DEFAULT 0,
            race_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    ''')
    
    conn.commit()
    cursor.close()
    conn.close()
    print("Database tables initialized successfully in PostgreSQL!")

# --- Validation Helper Functions ---

def is_username_taken(username):
    """Check karta hai ki username pehle se exist karta hai ya nahi."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT 1 FROM drivers WHERE LOWER(username) = LOWER(%s);', (username,))
    exists = cursor.fetchone() is not None
    cursor.close()
    conn.close()
    return exists

def is_phone_registered(phone):
    """Check karta hai ki phone number pehle se registered hai ya nahi."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT 1 FROM drivers WHERE phone = %s;', (phone,))
    exists = cursor.fetchone() is not None
    cursor.close()
    conn.close()
    return exists

# --- Auth Functions ---

def add_user(phone, username, password, player_id):
    """app.py ke /register route ke liye naya driver add karta hai."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO drivers (phone, username, password, player_id)
            VALUES (%s, %s, %s, %s);
        ''', (phone, username, password, player_id))
        conn.commit()
        return True
    except Exception as e:
        print("Database Insert Error:", e)
        return False
    finally:
        cursor.close()
        conn.close()

def check_user(username_or_phone, password):
    """app.py ke /login route ke liye user verify karta hai."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, username, password, player_id, level, total_score, coins 
        FROM drivers 
        WHERE (username = %s OR phone = %s) AND password = %s;
    ''', (username_or_phone, username_or_phone, password))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user

# --- Profile & Game Data Functions ---

def get_profile_data(user_id):
    """Driver profile aur race history fetch karta hai."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Driver data fetch
    cursor.execute('''
        SELECT username, player_id, level, total_score, coins 
        FROM drivers 
        WHERE id = %s;
    ''', (user_id,))
    user = cursor.fetchone()
    
    # Race results fetch
    cursor.execute('''
        SELECT position, score, race_date 
        FROM race_results 
        WHERE user_id = %s 
        ORDER BY id DESC;
    ''', (user_id,))
    races = cursor.fetchall()
    
    cursor.close()
    conn.close()
    return user, races

def save_race_result(user_id, position, score, coins_earned=0):
    """Unity race complete hone par score aur position save karta hai."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO race_results (user_id, position, score, coins_earned)
            VALUES (%s, %s, %s, %s);
        ''', (user_id, position, score, coins_earned))
        
        cursor.execute('''
            UPDATE drivers 
            SET total_score = total_score + %s,
                coins = coins + %s 
            WHERE id = %s;
        ''', (score, coins_earned, user_id))
        
        conn.commit()
        return True
    except Exception as e:
        print("Error saving race result:", e)
        return False
    finally:
        cursor.close()
        conn.close()

def get_leaderboard(limit=10):
    """Top high score drivers fetch karta hai."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT username, total_score, level, coins 
        FROM drivers 
        ORDER BY total_score DESC 
        LIMIT %s;
    ''', (limit,))
    leaderboard = [dict(row) for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return leaderboard

if __name__ == '__main__':
    init_db()