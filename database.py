import sqlite3

DATABASE_NAME = 'database.db'

def get_db_connection():
    """Database connection return karta hai."""
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Drivers/Users aur Race Results tables create karta hai."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 1. Drivers Table (Phone & Username UNIQUE)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS drivers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            phone TEXT UNIQUE NOT NULL,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            player_id TEXT UNIQUE NOT NULL,
            level INTEGER DEFAULT 1,
            total_score INTEGER DEFAULT 0,
            coins INTEGER DEFAULT 1000,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # 2. Race Results Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS race_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            position INTEGER,
            score INTEGER NOT NULL,
            coins_earned INTEGER DEFAULT 0,
            race_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES drivers (id)
        )
    ''')
    
    conn.commit()
    conn.close()
    print("Database tables initialized successfully!")

# --- Validation Helper Functions ---

def is_username_taken(username):
    """Check karta hai ki username pehle se exist karta hai ya nahi."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT 1 FROM drivers WHERE LOWER(username) = LOWER(?)', (username,))
    exists = cursor.fetchone() is not None
    conn.close()
    return exists

def is_phone_registered(phone):
    """Check karta hai ki phone number pehle se registered hai ya nahi."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT 1 FROM drivers WHERE phone = ?', (phone,))
    exists = cursor.fetchone() is not None
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
            VALUES (?, ?, ?, ?)
        ''', (phone, username, password, player_id))
        conn.commit()
        return True
    except Exception:
        return False
    finally:
        conn.close()

def check_user(username_or_phone, password):
    """app.py ke /login route ke liye user verify karta hai."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, username, password, player_id, level, total_score, coins 
        FROM drivers 
        WHERE (username = ? OR phone = ?) AND password = ?
    ''', (username_or_phone, username_or_phone, password))
    user = cursor.fetchone()
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
        WHERE id = ?
    ''', (user_id,))
    user = cursor.fetchone()
    
    # Race results fetch
    cursor.execute('''
        SELECT position, score, race_date 
        FROM race_results 
        WHERE user_id = ? 
        ORDER BY id DESC
    ''', (user_id,))
    races = cursor.fetchall()
    
    conn.close()
    return user, races

def save_race_result(user_id, position, score, coins_earned=0):
    """Unity race complete hone par score aur position save karta hai."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO race_results (user_id, position, score, coins_earned)
            VALUES (?, ?, ?, ?)
        ''', (user_id, position, score, coins_earned))
        
        cursor.execute('''
            UPDATE drivers 
            SET total_score = total_score + ?,
                coins = coins + ?
            WHERE id = ?
        ''', (score, coins_earned, user_id))
        
        conn.commit()
        return True
    except Exception as e:
        print("Error saving race result:", e)
        return False
    finally:
        conn.close()

def get_leaderboard(limit=10):
    """Top high score drivers fetch karta hai."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT username, total_score, level, coins 
        FROM drivers 
        ORDER BY total_score DESC 
        LIMIT ?
    ''', (limit,))
    leaderboard = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return leaderboard

if __name__ == '__main__':
    init_db()