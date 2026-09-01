from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
import database
import random
import re
from database import save_race_result
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.secret_key = "racer_secret_key"

database.init_db()

def generate_player_id():
    return str(random.randint(1000000000, 9999999999))

def is_valid_mobile(phone):
    return bool(re.match(r'^[6-9]\d{9}$', phone))

def is_strong_password(password):
    if len(password) < 6:
        return False, "Password must be at least 6 characters long!"
    if not re.search(r'[0-9]', password):
        return False, "Password must contain at least one number (0-9)!"
    if not re.search(r'[a-zA-Z]', password):
        return False, "Password must contain at least one letter!"
    return True, "Strong password"

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/intro')
def intro():
    return render_template('intro.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json() if request.is_json else request.form
        user_in = data.get('username')
        pass_in = data.get('password')

        if not user_in or not pass_in:
            if request.is_json:
                return jsonify({"success": False, "message": "Username and password are required!"}), 400
            flash("Please enter both username and password.")
            return redirect(url_for('login'))

        user = database.check_user(user_in, pass_in)
        if user:
            session['user_id'] = user[0]
            session['username'] = user[1]
            session['player_id'] = user[3]
            
            if request.is_json:
                return jsonify({"success": True, "message": "Login successful!"})
            return redirect(url_for('loading'))
        else:
            if request.is_json:
                return jsonify({"success": False, "message": "Invalid username/number or password!"}), 401
            flash("Invalid Login! Please check your credentials.")
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json() if request.is_json else request.form

    phone = data.get('phone', '').strip()
    username = data.get('username', '').strip()
    password = data.get('password', '')
    confirm_password = data.get('confirm_password', '')

    if not phone or not username or not password or not confirm_password:
        return jsonify({"success": False, "message": "All fields are required!"}), 400

    if not is_valid_mobile(phone):
        return jsonify({"success": False, "message": "Invalid mobile number! Enter a valid 10-digit number."}), 400

    if database.is_phone_registered(phone):
        return jsonify({"success": False, "message": "This mobile number is already registered!"}), 400

    if len(username) < 3:
        return jsonify({"success": False, "message": "Username must be at least 3 characters!"}), 400

    if database.is_username_taken(username):
        return jsonify({"success": False, "message": "Username already taken! Choose a unique driver alias."}), 400

    if password != confirm_password:
        return jsonify({"success": False, "message": "Passwords do not match!"}), 400

    is_strong, pass_msg = is_strong_password(password)
    if not is_strong:
        return jsonify({"success": False, "message": pass_msg}), 400

    player_id = generate_player_id()
    if database.add_user(phone, username, password, player_id):
        return jsonify({"success": True, "message": "Driver account created successfully! Please Login."})
    else:
        return jsonify({"success": False, "message": "Server error creating driver account."}), 500

@app.route('/loading')
def loading():
    return render_template('loading.html')

@app.route('/login_guest')
def login_guest():
    session.clear()
    session['username'] = 'Guest'
    session['user_id'] = -1
    session['player_id'] = 'GUEST'
    return redirect(url_for('loading'))

@app.route('/main_menu')
def main_menu():
    user_id = session.get('user_id')
    if user_id is None:
        return redirect(url_for('login'))

    username = session.get('username', 'Guest')
    player_id = session.get('player_id', '0000000000')

    if user_id == -1:
        return render_template(
            'main_menu.html',
            username="Guest",
            player_id="GUEST",
            level=1,
            total_score=0,
            current_xp=0,
            max_xp=1000
        )

    user, _ = database.get_profile_data(user_id)
    if user:
        total_score = user[3] or 0
        level = (total_score // 1000) + 1
        current_xp = total_score % 1000
        max_xp = 1000
        return render_template(
            'main_menu.html',
            username=user[0],
            player_id=user[1],
            level=level,
            total_score=total_score,
            current_xp=current_xp,
            max_xp=max_xp
        )

    return render_template('main_menu.html', username=username, player_id=player_id, level=1, total_score=0, current_xp=0, max_xp=1000)

@app.route('/get_player_stats')
def get_player_stats():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"success": False}), 401

    if user_id == -1:
        return jsonify({
            "success": True,
            "username": "Guest",
            "level": 1,
            "total_score": 0,
            "current_xp": 0,
            "max_xp": 1000
        })

    user, _ = database.get_profile_data(user_id)
    if not user:
        return jsonify({"success": False}), 404

    total_score = user[3] or 0
    level = (total_score // 1000) + 1
    current_xp = total_score % 1000

    return jsonify({
        "success": True,
        "username": user[0],
        "player_id": user[1],
        "level": level,
        "total_score": total_score,
        "current_xp": current_xp,
        "max_xp": 1000
    })

# --- Friend System Routes ---

@app.route('/search_driver')
def search_driver():
    user_id = session.get('user_id')
    if not user_id or user_id == -1:
        return jsonify({"success": False, "message": "Please login to search drivers."}), 401
        
    pid = request.args.get('player_id', '').strip()
    if not pid:
        return jsonify({"success": False, "message": "Enter a valid Player ID."}), 400
        
    driver_data, err = database.search_driver_by_player_id(pid, user_id)
    if err:
        return jsonify({"success": False, "message": err}), 404
        
    return jsonify({"success": True, "driver": driver_data})

@app.route('/send_friend_request', methods=['POST'])
def send_request():
    user_id = session.get('user_id')
    if not user_id or user_id == -1:
        return jsonify({"success": False, "message": "Please login first."}), 401
        
    data = request.get_json() or {}
    receiver_pid = data.get('player_id')
    
    success, msg = database.send_friend_request(user_id, receiver_pid)
    return jsonify({"success": success, "message": msg})

@app.route('/get_mail_requests')
def get_mail_requests():
    user_id = session.get('user_id')
    if not user_id or user_id == -1:
        return jsonify({"success": False, "requests": []})
        
    requests = database.get_incoming_friend_requests(user_id)
    return jsonify({"success": True, "requests": requests, "count": len(requests)})

@app.route('/respond_request', methods=['POST'])
def respond_request():
    user_id = session.get('user_id')
    if not user_id or user_id == -1:
        return jsonify({"success": False}), 401
        
    data = request.get_json() or {}
    req_id = data.get('request_id')
    action = data.get('action') # 'accept' ya 'reject'
    
    success = database.respond_to_friend_request(req_id, user_id, action)
    return jsonify({"success": success})

@app.route('/get_friends')
def get_friends():
    user_id = session.get('user_id')
    if not user_id or user_id == -1:
        return jsonify({"success": False, "friends": []})
        
    friends = database.get_friends_list(user_id)
    return jsonify({"success": True, "friends": friends})

@app.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out.")
    return redirect(url_for('login'))

@app.route('/save_race_result', methods=['POST'])
def save_race():
    data = request.get_json()
    user_id = session.get('user_id')

    if not user_id:
        return jsonify({"error": "Not logged in"}), 401

    position = data.get("position")
    score = data.get("score")

    save_race_result(user_id, position, score)
    return jsonify({"status": "success"})

@app.route('/profile')
def profile():
    user_id = session.get('user_id')
    if user_id is None:
        return redirect(url_for('login'))

    if user_id == -1:
        return render_template(
            "profile.html",
            username="Guest",
            player_id="GUEST",
            level=1,
            total_score=0,
            current_xp=0,
            max_xp=1000,
            races=[],
            level_up=False
        )

    user, races = database.get_profile_data(user_id)
    total_score = user[3] or 0
    level = (total_score // 1000) + 1
    current_xp = total_score % 1000
    max_xp = 1000

    old_level = session.get('last_level', 1)
    level_up = level > old_level
    session['last_level'] = level

    return render_template(
        "profile.html",
        username=user[0],
        player_id=user[1],
        level=level,
        total_score=total_score,
        current_xp=current_xp,
        max_xp=max_xp,
        races=races,
        level_up=level_up
    )

@app.route('/privacy_policy')
def privacy_policy():
    return render_template('privacy_policy.html')

@app.route('/shop')
def shop():
    return render_template('shop.html')

if __name__ == '__main__':
    app.run(debug=True)