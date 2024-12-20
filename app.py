import math
from flask import Flask, request, jsonify, render_template, redirect, url_for, flash
from datetime import datetime
from skyfield.api import load
from geopy.geocoders import Nominatim
import random
from werkzeug.security import generate_password_hash, check_password_hash
import ephem
app = Flask(__name__)
app.secret_key = '1234567890123456'  # Needed for flashing messages

# Hardcoded user credentials (for demo purposes)
hardcoded_username = "user1"
hardcoded_password = "password123"

# Dummy horoscope data for demonstration
daily_horoscopes = {
    "aries": "Today is a great day to take initiative and pursue your goals.",
    "taurus": "Patience will be your ally today. Good things come to those who wait.",
    "gemini": "Your communication skills will shine. Connect with loved ones.",
    "cancer": "Focus on self-care and nurture your emotions.",
    "leo": "Show your leadership skills and embrace opportunities for growth.",
    "virgo": "Organize your tasks and pay attention to details for success.",
    "libra": "Seek balance in relationships and embrace harmony.",
    "scorpio": "Transformation is on the horizon. Embrace change fearlessly.",
    "sagittarius": "Your adventurous spirit will lead you to exciting opportunities.",
    "capricorn": "Hard work and persistence will pay off. Stay focused.",
    "aquarius": "Innovation and creativity will guide you today.",
    "pisces": "Trust your intuition and explore your artistic side."
}
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


def generate_square_birth_chart(planets):
    # Create the figure and axis
    fig, ax = plt.subplots(figsize=(6, 6))
    
    # Draw the outer square (12 x 12)
    outer_square = Rectangle((0, 0), 12, 12, fill=None, edgecolor="black", linewidth=2)
    ax.add_patch(outer_square)

    # Define the house coordinates for a square chart layout
    house_coords = [
        (0, 9), (3, 9), (6, 9), (9, 9),
        (0, 6), (3, 6), (6, 6), (9, 6),
        (0, 3), (3, 3), (6, 3), (9, 3),
        (0, 0), (3, 0), (6, 0), (9, 0)
    ]

    # Add house rectangles
    for i, (x, y) in enumerate(house_coords, start=1):
        ax.add_patch(Rectangle((x, y), 3, 3, fill=False, edgecolor="gray", linewidth=1))
        ax.text(x + 1.5, y + 1.5, f"House {i}", ha="center", va="center", fontsize=8, color="blue")

    # Place planets in their respective houses
    for planet, data in planets.items():
        house_num = data['house']
        x, y = house_coords[house_num - 1]  # Get the coordinates for the house
        ax.text(x + 1.5, y + 1.5, planet, ha="center", va="center", fontsize=10, color="red")

    # Set the plot limits and hide axis
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 12)
    ax.axis("off")

    # Save the chart image
    plt.savefig('static/square_birth_chart.png')
    plt.close(fig)


@app.route('/birth_chart', methods=['GET'])
def birth_chart():
    # Example planets input (replace with actual calculations later)
    planets = {
        'Sun': {'house': 1},
        'Moon': {'house': 5},
        'Venus': {'house': 3},
        'Mars': {'house': 10},
        'Jupiter': {'house': 8},
        'Saturn': {'house': 7}
    }
    generate_square_birth_chart(planets)  # Generate the chart
    return render_template('birth_chart.html')  # Render the template


import plotly.graph_objects as go
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend

# Example data for the chart
houses = [
    "1st House", "2nd House", "3rd House", "4th House",
    "5th House", "6th House", "7th House", "8th House",
    "9th House", "10th House", "11th House", "12th House"
]

# Coordinates for the square chart
coordinates = [
    (0, 1), (1, 1), (1, 0), (0, 0),
    (0, -1), (-1, -1), (-1, 0), (-1, 1),
    (1, 2), (2, 1), (2, 0), (1, -2)
]

# Planets and positions
planets = ["Sun", "Moon", "Venus", "Mars"]
positions = [(0.5, 0.5), (1.5, 1), (0, -0.5), (-1.5, -0.5)]

# Create figure
fig = go.Figure()

# Add houses
for i, (x, y) in enumerate(coordinates):
    fig.add_trace(go.Scatter(
        x=[x], y=[y],
        mode='markers+text',
        text=houses[i],
        textposition="bottom center",
        marker=dict(size=15, color='lightblue'),
    ))

# Add planets
for i, (x, y) in enumerate(positions):
    fig.add_trace(go.Scatter(
        x=[x], y=[y],
        mode='markers+text',
        text=planets[i],
        textposition="top center",
        marker=dict(size=20, color='orange'),
    ))

# Update layout for aesthetics
fig.update_layout(
    title="Birth Chart",
    xaxis=dict(showgrid=False, zeroline=False, visible=False),
    yaxis=dict(showgrid=False, zeroline=False, visible=False),
    plot_bgcolor='white',
    height=600,
    width=600
)

# Show the chart
fig.show()

# Define the zodiac signs and their degree spans (30 degrees each)
zodiac_signs = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
]

# Define the planets and their positions in degrees
planet_positions = {
    "Sun": 249.83,     # Example positions
    "Moon": 273.55,
    "Venus": 297.56,
    "Mars": 129.15,
    "Jupiter": 75.85,
    "Saturn": 345.09
}

# Create a function to draw the birth chart and save as an image
def draw_birth_chart(planet_positions, file_path):
    # Create the figure
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw={'projection': 'polar'})
    
    # Draw the circles for each house (12 houses)
    ax.set_theta_offset(np.pi / 2)  # Set the 0 degree at the top
    ax.set_theta_direction(-1)  # Make the degrees go clockwise
    
    # Draw the 12 sections for the zodiac signs
    for i, sign in enumerate(zodiac_signs):
        ax.plot([i * np.pi / 6, (i + 1) * np.pi / 6], [0, 1], color='black', lw=2)
        ax.text(i * np.pi / 6 + np.pi / 12, 1.05, sign, horizontalalignment='center', fontsize=12)
    
    # Plot the planets in their respective houses (degrees)
    for planet, degrees in planet_positions.items():
        # Normalize the degrees to radians
        angle = np.radians(degrees % 360)
        ax.plot(angle, 1, 'o', markersize=8, label=planet)
        ax.text(angle, 1.05, f'{planet} ({degrees}°)', horizontalalignment='center', fontsize=10)
    
    # Add the legend for planets
    ax.legend(loc='upper left', bbox_to_anchor=(1.1, 1.1), fontsize=10)
    
    # Save the chart as a PNG file
    plt.savefig(file_path, bbox_inches='tight')
    plt.close()

# Example: Save the birth chart image
file_path = 'static/birth_chart.png'
draw_birth_chart(planet_positions, file_path)




@app.route('/daily_horoscope', methods=['GET', 'POST'])
def daily_horoscope():
    horoscope = None

    if request.method == 'POST':
        zodiac_sign = request.form.get('zodiac_sign')

        if zodiac_sign:
            # Fetch horoscope from the inbuilt data based on the zodiac sign
            if zodiac_sign in daily_horoscopes:
                horoscope = daily_horoscopes[zodiac_sign]
            else:
                flash("Sorry, we don't have horoscope data for the selected sign.", 'error')
        else:
            flash("Please select a zodiac sign.", 'error')

    return render_template('daily_horoscope.html', horoscope=horoscope)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        flash('Registration is not saved. Please login with predefined credentials.', 'info')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username == hardcoded_username and password == hardcoded_password:
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password!', 'error')
    return render_template('login.html')

# Home page
@app.route('/')
def home():
    return render_template('index.html')


@app.route('/logout')
def logout():
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))


# Tarot Deck with Card Names and Meanings
tarot_deck = [
    {"name": "The Fool", "meaning": "New beginnings, innocence, adventure, and spontaneity.", "image": "/static/images/tarot/the_fool.jpg"},
    {"name": "The Magician", "meaning": "Manifestation, resourcefulness, and inspired action.", "image": "/static/images/tarot/the_magician.jpg"},
    {"name": "The High Priestess", "meaning": "Intuition, subconscious mind, and mystery.", "image": "/static/images/tarot/the_high_priestess.jpg"},
    {"name": "The Empress", "meaning": "Nurturing, abundance, femininity, and nature.", "image": "/static/images/tarot/the_empress.jpg"},
    {"name": "The Emperor", "meaning": "Authority, structure, control, and fatherhood.", "image": "/static/images/tarot/the_emperor.jpg"},
    {"name": "The Lovers", "meaning": "Love, harmony, relationships, and choices.", "image": "/static/images/tarot/the_lovers.jpg"},
    {"name": "The Chariot", "meaning": "Determination, willpower, and success.", "image": "/static/images/tarot/the_chariot.jpg"},
    {"name": "The Hermit", "meaning": "Soul-searching, introspection, and inner guidance.", "image": "/static/images/tarot/the_hermit.jpg"},
    {"name": "Wheel of Fortune", "meaning": "Luck, karma, destiny, and cycles of change.", "image": "/static/images/tarot/wheel_of_fortune.jpg"},
    {"name": "Death", "meaning": "Endings, transitions, and transformation.", "image": "/static/images/tarot/death.jpg"},
]
@app.route('/tarot', methods=['GET', 'POST'])
def tarot():
    cards = []  # Initialize cards variable to avoid errors
    error_message = None  # Initialize error message variable

    if request.method == 'POST':
        reading_type = request.form.get('reading_type')
        if reading_type == 'daily':
            selected_card = random.choice(tarot_deck)
            cards = [selected_card]  # Single card for daily reading
        elif reading_type == 'past_present_future':
            if len(tarot_deck) >= 3:
                selected_cards = random.sample(tarot_deck, 3)  # Pick 3 cards
                cards = selected_cards
            else:
                error_message = "Not enough cards for this reading."
        elif reading_type == 'yes_no':
            selected_card = random.choice(tarot_deck)
            cards = [selected_card]

    # For GET request, render all cards in the deck
    return render_template('tarot.html', cards=cards, error_message=error_message, reading_type=request.form.get('reading_type'))

@app.route('/tarot/<card_name>', methods=['GET'])
def tarot_card(card_name):
    # Find the card with the name provided
    card = next((card for card in tarot_deck if card['name'].lower() == card_name.lower()), None)
    if card:
        return render_template('tarot_card_detail.html', card=card)
    else:
        return redirect(url_for('tarot'))



from datetime import datetime

# Function to determine Sun sign based on birth date
def get_sun_sign(birth_date):
    try:
        # Parse birth date from string (YYYY-MM-DD format)
        birth_date = datetime.strptime(birth_date, '%Y-%m-%d')

        # Define the sun sign date ranges
        sun_sign_dates = {
            "Aries": (3, 21, 4, 19),
            "Taurus": (4, 20, 5, 20),
            "Gemini": (5, 21, 6, 20),
            "Cancer": (6, 21, 7, 22),
            "Leo": (7, 23, 8, 22),
            "Virgo": (8, 23, 9, 22),
            "Libra": (9, 23, 10, 22),
            "Scorpio": (10, 23, 11, 21),
            "Sagittarius": (11, 22, 12, 21),
            "Capricorn": (12, 22, 1, 19),
            "Aquarius": (1, 20, 2, 18),
            "Pisces": (2, 19, 3, 20)
        }

        # Find the sun sign by checking the month and day
        for sign, (start_month, start_day, end_month, end_day) in sun_sign_dates.items():
            if (birth_date.month == start_month and birth_date.day >= start_day) or \
               (birth_date.month == end_month and birth_date.day <= end_day):
                return sign
        return "Unknown"  # Default in case no match
    except Exception as e:
        print(f"Error in get_sun_sign: {e}")
        return None

# Function to parse datetime (same as before)
def parse_datetime(birth_date, birth_time):
    if len(birth_time.split(":")) == 2:
        birth_time += ":00"
    return datetime.strptime(f'{birth_date} {birth_time}', "%Y-%m-%d %H:%M:%S")

# Function to calculate planetary positions using PyEphem
def get_planet_positions(birth_date, birth_time, location):
    try:
        # Get latitude and longitude for the location
        geolocator = Nominatim(user_agent="astroApp")
        location_data = geolocator.geocode(location, timeout=10)
        if not location_data:
            raise ValueError("Location not found.")
        latitude = location_data.latitude
        longitude = location_data.longitude

        # Parse the birth date and time
        birth_datetime = parse_datetime(birth_date, birth_time)
        birth_date = ephem.Date(birth_datetime)

        # Set up observer location
        observer = ephem.Observer()
        observer.lat = str(latitude)
        observer.lon = str(longitude)
        observer.date = birth_date

        # Get the planetary positions
        planets = {
            "sun": ephem.Sun(observer),
            "moon": ephem.Moon(observer),
            "venus": ephem.Venus(observer),
            "mars": ephem.Mars(observer),
            "jupiter": ephem.Jupiter(observer),
            "saturn": ephem.Saturn(observer),
        }

        # Get the longitude positions of the planets
        planet_positions = {}
        for planet_name, planet in planets.items():
            planet_positions[planet_name] = math.degrees(planet.ra) % 360  # Convert to degrees

        return planet_positions

    except Exception as e:
        print(f"Error in get_planet_positions: {e}")
        return {"error": f"An error occurred: {str(e)}"}

# Define a function to calculate house placements (example, simplified)
def get_house_placements(birth_date, birth_time, location):
    try:
        # Dummy implementation: replace with actual house calculation logic
        # Here, we are simulating house placements. Replace this with your actual calculation.
        house_placements = {
            "1st House": 15.5,
            "2nd House": 45.2,
            "3rd House": 78.9,
            "4th House": 105.6
        }
        return house_placements
    except Exception as e:
        return {"error": str(e)}



def get_planetary_aspects(planet_positions):
    pass  # Same as before
@app.route('/horoscope', methods=['GET', 'POST'])
def horoscope():
    if request.method == 'POST':
        name = request.form.get('name')
        birth_date = request.form.get('birth_date')
        birth_time = request.form.get('birth_time')
        location = request.form.get('location')

        # Validate inputs
        if not name or not birth_date or not birth_time or not location:
            flash("Please fill in all fields!", "error")
            return redirect(url_for('horoscope'))
        
        try:
            # Get Sun Sign
            sun_sign = get_sun_sign(birth_date)
            
            # Get Planetary positions
            planets_positions = get_planet_positions(birth_date, birth_time, location)
            
            # Get House Placements
            house_placements = get_house_placements(birth_date, birth_time, location)

            # Basic prediction based on Sun Sign
            sun_sign_prediction = {
                "Aries": "You're feeling adventurous today, Aries! It's a great day to take risks and step out of your comfort zone.",
                "Taurus": "Focus on your finances today, Taurus. Small investments or saving plans could yield big rewards.",
                "Gemini": "Communication is key today, Gemini. You might find yourself having important conversations with loved ones.",
                "Cancer": "Today is a good day for self-care, Cancer. Take time to relax and recharge.",
                "Leo": "You're in the spotlight today, Leo! Your leadership skills will shine in group settings.",
                "Virgo": "Pay attention to the details today, Virgo. Precision will be your ally in solving problems.",
                "Libra": "Balance is the key today, Libra. Seek harmony in your relationships and surroundings.",
                "Scorpio": "You're feeling ambitious today, Scorpio. Take charge of your goals and work towards your success.",
                "Sagittarius": "Adventure is calling, Sagittarius! Today is a great day for exploring new ideas and places.",
                "Capricorn": "Focus on your career today, Capricorn. Hard work will pay off in the long run.",
                "Aquarius": "You're feeling creative today, Aquarius. Express yourself through art or new projects.",
                "Pisces": "Emotions may run high today, Pisces. Trust your intuition and allow yourself to connect with others."
            }

            prediction = f"Hello {name}, your horoscope for {birth_date} at {birth_time} in {location} is: " \
                         f"Your Sun sign is {sun_sign}. {sun_sign_prediction.get(sun_sign, 'Your Sun sign holds the key to your energy today.')} " \
                         f"Here are your planetary positions: " \
                         f"Sun at {planets_positions['sun']}°, Moon at {planets_positions['moon']}°, " \
                         f"Venus at {planets_positions['venus']}°, and Mars at {planets_positions['mars']}°."

            # Add personalized predictions based on planetary positions
            if planets_positions['venus'] > 90:
                prediction += " Venus' position suggests a positive influence on your relationships today. It's a good time for love and socializing."
            if planets_positions['mars'] > 90:
                prediction += " Mars indicates strong energy today, perfect for tackling challenges and staying active."
            if planets_positions['moon'] < 45:
                prediction += " The Moon's position suggests an emotional day, be mindful of your feelings and reactions."
            
            # Pass house_placements to the template
            return render_template('horoscope.html', prediction=prediction, planets_positions=planets_positions, 
                                   sun_sign=sun_sign, house_placements=house_placements)
        except Exception as e:
            flash(f"An error occurred: {str(e)}", "error")
            return redirect(url_for('horoscope'))
    
    return render_template('horoscope.html', house_placements={})



# Calculate Life Path Number (simplified example)
def calculate_life_path(birth_date):
    date_parts = list(map(int, birth_date.split('-')))
    life_path_number = sum(date_parts) % 9
    return life_path_number if life_path_number != 0 else 9

# Calculate Expression Number (based on name, simplified)
def calculate_expression_number(name):
    # Using the Pythagorean system for name numerology
    alphabet_to_number = {'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8, 'I': 9,
                          'J': 1, 'K': 2, 'L': 3, 'M': 4, 'N': 5, 'O': 6, 'P': 7, 'Q': 8, 'R': 9,
                          'S': 1, 'T': 2, 'U': 3, 'V': 4, 'W': 5, 'X': 6, 'Y': 7, 'Z': 8}
    name = name.upper().replace(" ", "")
    name_number = sum([alphabet_to_number[letter] for letter in name])
    while name_number > 9:
        name_number = sum([int(digit) for digit in str(name_number)])
    return name_number

# Calculate Soul Urge Number (based on vowels in name)
def calculate_soul_urge_number(name):
    vowels = 'AEIOU'
    alphabet_to_number = {'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8, 'I': 9,
                          'J': 1, 'K': 2, 'L': 3, 'M': 4, 'N': 5, 'O': 6, 'P': 7, 'Q': 8, 'R': 9,
                          'S': 1, 'T': 2, 'U': 3, 'V': 4, 'W': 5, 'X': 6, 'Y': 7, 'Z': 8}
    soul_urge_number = sum([alphabet_to_number[letter] for letter in name.upper() if letter in vowels])
    while soul_urge_number > 9:
        soul_urge_number = sum([int(digit) for digit in str(soul_urge_number)])
    return soul_urge_number

# Calculate Personality Number (based on consonants in name)
def calculate_personality_number(name):
    consonants = 'BCDFGHJKLMNPQRSTVWXYZ'
    alphabet_to_number = {'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8, 'I': 9,
                          'J': 1, 'K': 2, 'L': 3, 'M': 4, 'N': 5, 'O': 6, 'P': 7, 'Q': 8, 'R': 9,
                          'S': 1, 'T': 2, 'U': 3, 'V': 4, 'W': 5, 'X': 6, 'Y': 7, 'Z': 8}
    personality_number = sum([alphabet_to_number[letter] for letter in name.upper() if letter in consonants])
    while personality_number > 9:
        personality_number = sum([int(digit) for digit in str(personality_number)])
    return personality_number

# Calculate Maturity Number (combination of Life Path and Expression Numbers)
def calculate_maturity_number(life_path, expression_number):
    maturity_number = life_path + expression_number
    while maturity_number > 9:
        maturity_number = sum([int(digit) for digit in str(maturity_number)])
    return maturity_number

# Example numerology descriptions
numerology_descriptions = {
    1: {
        "life_path": "As a Life Path 1, you are an independent, pioneering spirit. You are driven by your own goals and have a strong desire to be the best at what you do. You are a natural leader and innovator, always striving to carve your own path in life. Challenges often fuel you, and you do well when working alone or leading a team toward a new vision. However, the challenge for you is learning to balance your independence with collaboration.",
        "expression": "Your Expression number is also a sign of leadership. You are confident, self-sufficient, and love to be in charge. You possess a strong sense of individuality and can inspire others to follow your lead. However, you must be careful not to become overly dominant or self-centered.",
        "soul_urge": "As your Soul urge number 1, you are deep down, you are motivated by a desire to succeed and prove yourself. You crave recognition and respect and seek to be acknowledged for your achievements. You have a strong inner drive to achieve greatness, which can sometimes lead to feelings of frustration if things don’t go according to your plan.",
        "personality": "As Personality Number 1: Others see you as a go-getter, someone who is capable of making decisions and taking action. You are decisive, energetic, and ambitious, and you often make a strong impression in any room.",
        "maturity": "As Maturity Number 1: As you mature, your leadership abilities will become more refined, and you will understand the importance of working with others and sharing the spotlight. Your growth involves learning to be more empathetic and balanced."
    },
    2: {
        "life_path": "Life Path Number 2 is all about harmony, cooperation, and balance. You are a diplomatic, gentle soul who seeks peace and avoids conflict at all costs. You thrive in relationships and have a natural ability to empathize with others. Your life’s purpose is to bring people together and foster harmony. You are a natural mediator and can bring out the best in others.",
        "expression": "Your Expression number reveals your nurturing side. You are kind, considerate, and have a great capacity for caring for others. Your ability to listen and understand others makes you a valuable friend, partner, and coworker.",
        "soul_urge": "As your soul urge number 2, you will Deep down, you want peaceful and loving relationships. You crave emotional closeness and are motivated by a desire to help and support others. Your soul urges you to create harmony in the world, and you often seek out situations where you can be of service.",
        "personality": "Personality Number 2: People see you as gentle, patient, and empathetic. You are the one who often smooths over conflicts and provides a calming influence. You are approachable, trustworthy, and reliable, and people turn to you when they need emotional support.",
        "maturity": "Maturity Number 2: Over time, you will learn to assert yourself more and become less dependent on others for emotional validation. Your growth involves standing up for yourself while still maintaining your natural compassion."
    },
    3: {
        "life_path": "Life Path Number 3 is all about self-expression and creativity. You are a natural performer, artist, or communicator. Your ability to express yourself through words, art, or other mediums is one of your greatest strengths. You are optimistic, joyful, and social, always bringing a sense of fun to the world around you.",
        "expression": "Your Expression number 3 enhances your ability to connect with others. You are charming, outgoing, and have a magnetic personality. You can captivate an audience with your words or your creative abilities.",
        "soul_urge": "As your soul urge number 3, You are motivated by a desire to be seen, heard, and appreciated. Your soul craves attention and recognition for your creative talents. You want to inspire and uplift others, and you thrive when you are surrounded by a supportive, enthusiastic audience.",
        "personality": "Personality Number 3: Others see you as fun-loving, witty, and full of energy. You are often the life of the party, and people are drawn to your infectious enthusiasm. You are emotionally expressive and can light up any room with your charm.",
        "maturity": "Maturity Number 3: As you mature, you will learn to refine your creativity and channel it into more focused endeavors. You will also recognize the importance of inner growth and emotional balance, not just external recognition."
    },
    4: {
        "life_path": "Life Path Number 4 is grounded, practical, and detail-oriented. You are a hard worker who thrives in structured environments and loves creating lasting foundations. You are driven by a need for security and stability, both for yourself and for others. You are dependable and meticulous in everything you do.",
        "expression": "Your Expression number 4 speaks to your pragmatic nature. You are disciplined, responsible, and can be counted on to get things done. Your ability to plan and organize is exceptional, and you enjoy working toward long-term goals.",
        "soul_urge": "As your soul urge number 4, Deep down, you are motivated by a desire for stability and security. You want to create a solid foundation for your future, and your soul craves the comfort that comes from hard work and achievement.",
        "personality": "Personality Number 4: Others see you as reliable, hardworking, and grounded. You are serious, but not without a sense of humor. People turn to you for advice because they know you will provide sound, practical solutions.",
        "maturity": "Maturity Number 4: As you mature, you will learn to let go of some of your rigid expectations and embrace more flexibility. You will also discover the importance of personal growth and spiritual development alongside your material pursuits."
    },
    5: {
        "life_path": "Life Path Number 5 is all about freedom, change, and exploration. You are an adventurous spirit who thrives on new experiences and is always seeking excitement and variety. You are adaptable, curious, and open-minded, and you can easily see things from different perspectives. You can get restless if life becomes too predictable.",
        "expression": "Your Expression number 5 reveals your love for change and excitement. You are spontaneous, dynamic, and enthusiastic, with a natural ability to adapt to different situations. You are a risk-taker who isn’t afraid to step outside of your comfort zone.",
        "soul_urge": "As your soul urge number 5, Deep down, you are motivated by a desire for personal freedom. You seek independence and the ability to make your own choices without being constrained by rules or expectations.",
        "personality": "Personality Number 5: Others see you as exciting, energetic, and full of life. You are the person who brings excitement to any situation, and people love to be around you for your adventurous and carefree spirit.",
        "maturity": "Maturity Number 5: As you mature, you will learn to focus your energy on projects and goals that require long-term commitment. You will understand the importance of stability, but without sacrificing your love for freedom and variety."
    },
    6: {
        "life_path": "Life Path Number 6 is all about care, love, and responsibility. You are a compassionate soul who is always ready to help others. Your life’s purpose is to provide support and stability to those around you, whether through family, community, or career. You are deeply empathetic and have a strong desire to create harmony in your surroundings.",
        "expression": "Your Expression number 6 reveals your nurturing abilities. You are loving, caring, and responsible, with a deep understanding of the needs of others. You often take on a parental role, even if you are not a parent, and you are happiest when you are taking care of others.",
        "soul_urge": "As your soul urge number 6, Deep down, you are motivated by a desire to create a loving, harmonious environment. You want to bring peace and comfort to others, and your soul is happiest when you are making a positive difference in the lives of those you care about.",
        "personality": "Personality Number 6: Others see you as kind, compassionate, and selfless. You are often the one who steps in to offer help or comfort when needed, and people turn to you for emotional support and guidance.",
        "maturity": "Maturity Number 6: As you mature, you will learn to balance your care for others with care for yourself. You will also discover the importance of creating boundaries to avoid burnout from taking on too much responsibility."
    },
    7: {
        "life_path": "Life Path Number 7 represents introspection, wisdom, and spirituality. People with this Life Path are often deep thinkers, analytical, and drawn to uncovering the mysteries of life. They are highly intuitive, intellectual, and are often on a quest for knowledge, truth, and spiritual understanding. They may prefer solitude and are naturally introspective, often looking within to find the answers to life’s questions. While they may come across as reserved or distant, they have a rich inner world that guides them.",
        "expression": "With an Expression Number of 7, you express yourself through deep thought, wisdom, and analysis. You are likely drawn to fields such as science, philosophy, or research, where you can explore complex ideas and seek the truth. You may also find fulfillment in spiritual or metaphysical pursuits, as you seek to understand the deeper aspects of life.",
        "soul_urge": "The Soul Urge number 7 is to seek truth, wisdom, and spiritual growth. You are deeply fulfilled when you are on a journey of self-discovery and when you can uncover deeper insights about the world and yourself. You feel at peace when you can explore and contemplate the mysteries of life.",
        "personality": "Personality Number 7: Your personality is introspective, intellectual, and reserved. You are seen as a deep thinker who enjoys spending time alone to reflect and explore your thoughts. While you may be quiet or private, those who know you well appreciate your wisdom and insight.",
        "maturity": "Maturity Number 7: As you mature, you may find that sharing your wisdom with others brings you greater fulfillment. You’ll learn to balance your introspective nature with engaging more actively in the world, helping others find clarity and purpose through your knowledge and experiences."
    },
    8: {
        "life_path": "Life Path Number 8 represents ambition, material success, and personal power. People with this Life Path are goal-oriented, determined, and often achieve great success in their professional lives. They are natural leaders with strong managerial abilities and a desire for financial independence. While they can be highly driven and authoritative, they must also learn to balance their ambitions with compassion and avoid becoming overly focused on material success at the expense of personal relationships.",
        "expression": "With an Expression Number of 8, you express yourself with power, authority, and a desire for success. You are likely to excel in business, management, or finance, where your ability to make strategic decisions and take charge is highly valued. You have a natural gift for leadership and tend to rise to the top of your field.",
        "soul_urge": "The Soul Urge number 8 is to achieve success, power, and financial independence. You are driven by the desire to build something lasting and substantial, whether it’s a career, wealth, or a legacy. You feel fulfilled when you are in control of your own destiny and can make a significant impact in the world.",
        "personality": "Personality Number 8: Your personality is confident, assertive, and ambitious. People view you as a strong, capable individual who knows what they want and is willing to work hard to achieve it. You are determined, practical, and often take charge in situations, making you a natural leader.",
        "maturity": "Maturity Number 8: As you mature, you may find that true success comes not just from financial achievement, but from creating meaningful relationships and contributing to others' growth. You will learn the value of balancing power with empathy, understanding that both personal and professional success rely on the strength of your relationships with others."
    },
    9: {
        "life_path": "Life Path Number 9 represents compassion, humanitarianism, and idealism. People with this Life Path are deeply concerned with the well-being of others and are driven by a desire to make the world a better place. They are highly empathetic, intuitive, and have a natural ability to understand the emotions and needs of others. They are often involved in charitable or humanitarian causes and are always looking for ways to help those in need. However, they may struggle with letting go of emotional attachments and the weight of the world’s problems.",
        "expression": "With an Expression Number of 9, you express yourself with compassion, generosity, and idealism. You are likely drawn to fields that involve helping others, such as social work, teaching, or healthcare. You feel fulfilled when you can contribute to the greater good and make a positive difference in the world.",
        "soul_urge": "The Soul Urge number 9 is to serve humanity and bring healing to the world. You are deeply fulfilled when you are helping others, whether through charitable work, artistic expression, or spiritual guidance. You feel at peace when you are able to use your talents and resources to make a positive impact.",
        "personality": "Personality Number 9: Your personality is compassionate, idealistic, and selfless. People are drawn to your caring nature and your desire to help others. You may be seen as someone who is deeply emotional, sensitive, and understanding, often putting the needs of others above your own.",
        "maturity": "Maturity Number 9: As you mature, you may learn to focus your idealism and compassion in a way that also allows you to take care of yourself. You will discover the importance of balancing your desire to help others with taking time for self-care and emotional healing. Understanding that you can’t save everyone will bring you greater peace and fulfillment."
    },

    # Continue adding descriptions for other numbers here...
}

@app.route('/numerology', methods=['GET', 'POST'])
def numerology():
    if request.method == 'POST':
        name = request.form['name']
        birth_date = request.form['birth_date']

        # Calculate each numerology number
        life_path = calculate_life_path(birth_date)
        expression_number = calculate_expression_number(name)
        soul_urge_number = calculate_soul_urge_number(name)
        personality_number = calculate_personality_number(name)
        maturity_number = calculate_maturity_number(life_path, expression_number)

        # Get the descriptions
        life_path_desc = numerology_descriptions.get(life_path, {}).get("life_path", "No description available")
        expression_desc = numerology_descriptions.get(expression_number, {}).get("expression", "No description available")
        soul_urge_desc = numerology_descriptions.get(soul_urge_number, {}).get("soul_urge", "No description available")
        personality_desc = numerology_descriptions.get(personality_number, {}).get("personality", "No description available")
        maturity_desc = numerology_descriptions.get(maturity_number, {}).get("maturity", "No description available")

        # Send the numbers and their meanings to the template
        return render_template('numerology_result.html', 
                               life_path=life_path, 
                               expression_number=expression_number, 
                               soul_urge_number=soul_urge_number,
                               personality_number=personality_number, 
                               maturity_number=maturity_number,
                               name=name, birth_date=birth_date,
                               life_path_desc=life_path_desc, 
                               expression_desc=expression_desc, 
                               soul_urge_desc=soul_urge_desc, 
                               personality_desc=personality_desc,
                               maturity_desc=maturity_desc)

    # Render the form for user input on GET
    return render_template('numerology.html')

@app.route('/compatibility')
def compatibility():
    return render_template('compatibility.html')
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        
        # Here you would typically send the email or save the message to a database
        flash('Thank you for your message, we will get back to you soon!')
        return redirect(url_for('home'))
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000, use_reloader=False)

