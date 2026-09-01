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
    """Drivers, Race Results, aur Friend Requests tables create karta hai."""
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

    # 3. Friend Requests & Friendships Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS friend_requests (
            id SERIAL PRIMARY KEY,
            sender_id INT NOT NULL REFERENCES drivers (id) ON DELETE CASCADE,
            receiver_id INT NOT NULL REFERENCES drivers (id) ON DELETE CASCADE,
            status VARCHAR(20) DEFAULT 'pending', -- 'pending', 'accepted', 'rejected'
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(sender_id, receiver_id)
        );
    ''')
    
    conn.commit()
    cursor.close()
    conn.close()
    print("Database tables initialized successfully in PostgreSQL!")

# --- Validation Helper Functions ---

def is_username_taken(username):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT 1 FROM drivers WHERE LOWER(username) = LOWER(%s);', (username,))
    exists = cursor.fetchone() is not None
    cursor.close()
    conn.close()
    return exists

def is_phone_registered(phone):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT 1 FROM drivers WHERE phone = %s;', (phone,))
    exists = cursor.fetchone() is not None
    cursor.close()
    conn.close()
    return exists

# --- Auth Functions ---

def add_user(phone, username, password, player_id):
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
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT username, player_id, level, total_score, coins 
        FROM drivers 
        WHERE id = %s;
    ''', (user_id,))
    user = cursor.fetchone()
    
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

# --- Friend System Functions ---

def search_driver_by_player_id(player_id, current_user_id):
    """Player ID se kisi bhi user ki profile aur relation fetch karta hai."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, username, player_id, total_score, coins 
        FROM drivers 
        WHERE player_id = %s;
    ''', (player_id,))
    target = cursor.fetchone()
    
    if not target:
        cursor.close()
        conn.close()
        return None, "Driver not found"
        
    target_id = target['id']
    total_score = target['total_score'] or 0
    level = (total_score // 1000) + 1
    current_xp = total_score % 1000
    
    # Check total races & wins
    cursor.execute("SELECT COUNT(*), COUNT(CASE WHEN position = 1 THEN 1 END) FROM race_results WHERE user_id = %s", (target_id,))
    races_count, wins_count = cursor.fetchone()
    
    # Relation status check (self, pending, accepted, none)
    relation = "none"
    if target_id == current_user_id:
        relation = "self"
    else:
        cursor.execute('''
            SELECT status, sender_id FROM friend_requests 
            WHERE (sender_id = %s AND receiver_id = %s) OR (sender_id = %s AND receiver_id = %s);
        ''', (current_user_id, target_id, target_id, current_user_id))
        req = cursor.fetchone()
        if req:
            if req['status'] == 'accepted':
                relation = 'friends'
            elif req['sender_id'] == current_user_id:
                relation = 'request_sent'
            else:
                relation = 'request_received'
                
    cursor.close()
    conn.close()
    
    return {
        "id": target['id'],
        "username": target['username'],
        "player_id": target['player_id'],
        "level": level,
        "total_score": total_score,
        "current_xp": current_xp,
        "races_played": races_count or 0,
        "races_won": wins_count or 0,
        "relation": relation
    }, None

def send_friend_request(sender_id, receiver_player_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id FROM drivers WHERE player_id = %s;", (receiver_player_id,))
        receiver = cursor.fetchone()
        if not receiver:
            return False, "Driver not found"
            
        receiver_id = receiver['id']
        if sender_id == receiver_id:
            return False, "You cannot send request to yourself"
            
        cursor.execute('''
            INSERT INTO friend_requests (sender_id, receiver_id, status)
            VALUES (%s, %s, 'pending')
            ON CONFLICT (sender_id, receiver_id) DO UPDATE SET status = 'pending';
        ''', (sender_id, receiver_id))
        conn.commit()
        return True, "Friend request sent successfully!"
    except Exception as e:
        return False, str(e)
    finally:
        cursor.close()
        conn.close()

def get_incoming_friend_requests(user_id):
    """Aapko aayi hui pending friend requests fetch karta hai."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT fr.id as request_id, d.username, d.player_id, d.total_score, fr.created_at
        FROM friend_requests fr
        JOIN drivers d ON fr.sender_id = d.id
        WHERE fr.receiver_id = %s AND fr.status = 'pending'
        ORDER BY fr.id DESC;
    ''', (user_id,))
    rows = cursor.fetchall()
    
    requests = []
    for r in rows:
        total_score = r['total_score'] or 0
        level = (total_score // 1000) + 1
        requests.append({
            "request_id": r['request_id'],
            "username": r['username'],
            "player_id": r['player_id'],
            "level": level,
            "created_at": r['created_at'].strftime("%d %b, %H:%M") if r['created_at'] else ""
        })
    cursor.close()
    conn.close()
    return requests

def respond_to_friend_request(request_id, user_id, action):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        if action == 'accept':
            cursor.execute("UPDATE friend_requests SET status = 'accepted' WHERE id = %s AND receiver_id = %s;", (request_id, user_id))
        else:
            cursor.execute("DELETE FROM friend_requests WHERE id = %s AND receiver_id = %s;", (request_id, user_id))
        conn.commit()
        return True
    except Exception as e:
        return False
    finally:
        cursor.close()
        conn.close()

def get_friends_list(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT d.username, d.player_id, d.total_score
        FROM friend_requests fr
        JOIN drivers d ON (d.id = CASE WHEN fr.sender_id = %s THEN fr.receiver_id ELSE fr.sender_id END)
        WHERE (fr.sender_id = %s OR fr.receiver_id = %s) AND fr.status = 'accepted'
        ORDER BY d.total_score DESC;
    ''', (user_id, user_id, user_id))
    rows = cursor.fetchall()
    friends = []
    for r in rows:
        total_score = r['total_score'] or 0
        friends.append({
            "username": r['username'],
            "player_id": r['player_id'],
            "level": (total_score // 1000) + 1,
            "total_score": total_score
        })
    cursor.close()
    conn.close()
    return friends

if __name__ == '__main__':
    init_db()