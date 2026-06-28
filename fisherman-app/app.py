import random
import re
from flask import Flask, jsonify, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "super_secret_marine_command_center_key_xyz"

# User Database
USER_DATABASE = {
    "captain": "password123"
}


def generate_global_fleet():
    fleet = []

    fishing_boat_names = [
        "St. Peter", "St. Andrew", "St. Francis", "St. Thomas",
        "St. John", "St. Xavier", "St. Sebastian", "St. Antony",
        "St. Jude", "St. Joseph", "St. Raphael", "St. Gabriel",
        "St. Christopher", "St. Paul", "St. Mary", "St. Anne"
    ]

    ship_names = [
        "Ocean Carrier", "Pacific Dawn", "Atlantic Titan",
        "Nordic Swift", "Delta Patrol", "Global Mariner",
        "Sea Ranger", "Ocean Voyager"
    ]

    ship_types = [
        "Container Ship",
        "Oil Tanker",
        "Bulk Carrier",
        "LNG Carrier",
        "Coast Guard Escort"
    ]

    maritime_nations = [
        {"country": "India", "flag": "🇮🇳", "ports": ["Chennai Port", "Kochi Harbour", "Vizag Port", "Mumbai Port"]},
        {"country": "Panama", "flag": "🇵🇦", "ports": ["Port of Balboa", "Port of Cristobal", "Manzanillo"]},
        {"country": "Singapore", "flag": "🇸🇬", "ports": ["Tuas Port", "Keppel Terminal", "Jurong Port"]},
        {"country": "United States", "flag": "🇺🇸", "ports": ["Port of Los Angeles", "Port of Houston", "Port of Miami"]},
        {"country": "Japan", "flag": "🇯🇵", "ports": ["Port of Tokyo", "Port of Yokohama", "Port of Kobe"]},
        {"country": "United Kingdom", "flag": "🇬🇧", "ports": ["Port of Southampton", "Felixstowe", "Port of Liverpool"]},
        {"country": "Greece", "flag": "🇬🇷", "ports": ["Port of Piraeus", "Thessaloniki", "Patras"]}
    ]

    shipping_lanes = [
        {"name": "Indian Ocean Route", "lat_range": (5, 14), "lon_range": (80, 100)},
        {"name": "Arabian Sea Corridor", "lat_range": (10, 22), "lon_range": (60, 75)},
        {"name": "Mediterranean Sea Lane", "lat_range": (32, 40), "lon_range": (-5, 30)},
        {"name": "North Atlantic Route", "lat_range": (40, 55), "lon_range": (-50, -10)},
        {"name": "Trans-Pacific Route", "lat_range": (20, 45), "lon_range": (140, 175)},
        {"name": "Malacca Strait Corridor", "lat_range": (1, 6), "lon_range": (95, 105)}
    ]

    random.seed(101)

    for i in range(85):

        lane = random.choice(shipping_lanes)
        nation = random.choice(maritime_nations)
        port = random.choice(nation["ports"])

        lat = round(random.uniform(lane["lat_range"][0], lane["lat_range"][1]), 4)
        lon = round(random.uniform(lane["lon_range"][0], lane["lon_range"][1]), 4)

        speed = round(random.uniform(12.0, 25.5), 1)
        heading = random.randint(0, 359)

        # More fishing boats than ships
        if i < 55:
            vessel_type = random.choice([
                "Gillnet Boat",
                "Trawler Boat"
            ])
            name = f"{random.choice(fishing_boat_names)}-{200 + i}"

        else:
            vessel_type = random.choice(ship_types)
            name = f"{random.choice(ship_names)}-{200 + i}"

        fleet.append({
            "name": name,
            "type": vessel_type,
            "country": nation["country"],
            "flag": nation["flag"],
            "homePort": port,
            "lat": lat,
            "lon": lon,
            "speedKnots": speed,
            "heading": heading
        })

    return fleet


GLOBAL_FLEET = generate_global_fleet()


@app.route('/')
def home():
    if 'logged_in' in session:
        return render_template('index.html')
    return redirect(url_for('login'))



@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    success = None

    if request.method == 'POST':
        action = request.form.get('action')
        username = request.form.get('username', '').strip().lower()
        password = request.form.get('password', '')

        if not username or not password:
            error = "Fields cannot be left empty."
            return render_template('login.html', error=error)

        if action == "signup":

            password_pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&]).{8,}$'

            if username in USER_DATABASE:
                error = f"The username '{username}' is already registered!"

            elif not re.match(password_pattern, password):
                error = ("Password must contain at least 8 characters, "
                         "one uppercase letter, one lowercase letter, "
                         "one number, and one special character.")

            else:
                USER_DATABASE[username] = password
                success = "Account created successfully! Please sign in below."

        elif action == "login":
            if username in USER_DATABASE and USER_DATABASE[username] == password:
                session['logged_in'] = True
                session['username'] = username
                return redirect(url_for('home'))
            else:
                error = "Access Denied. Incorrect username or password."

    return render_template('login.html', error=error, success=success)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    return redirect(url_for('login'))


@app.route('/api/fleet', methods=['GET'])
def get_fleet():
    if 'logged_in' not in session:
        return jsonify({"error": "Unauthorized"}), 401

    return jsonify(GLOBAL_FLEET)


if __name__ == '__main__':
    app.run(port=5000, debug=True)