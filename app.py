from flask import Flask, render_template, request
import google.generativeai as genai
from config import GEMINI_API_KEY

app = Flask(__name__)

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/analyze', methods=['POST'])
def analyze():

    event_name = request.form['event_name']
    attendees = int(request.form['attendees'])
    duration = int(request.form['duration'])
    venue = request.form['venue']
    food_stalls = int(request.form['food_stalls'])

    # Sustainability Calculations

    food = int(attendees * 0.9)

    water = attendees * 3

    plastic = round(attendees * 0.04, 2)

    electricity = round(attendees * duration * 0.15, 2)

    # Sustainability Score

    score = 100

    if plastic > 30:
        score -= 20

    if food_stalls > 10:
        score -= 10

    if attendees > 1000:
        score -= 10

    # AI Recommendations

    prompt = f"""
You are a sustainability expert.

Analyze the following event and provide 5 practical sustainability recommendations.

Event Name: {event_name}
Number of Attendees: {attendees}
Duration: {duration} hours
Venue Type: {venue}
Food Stalls: {food_stalls}

Estimated Food Requirement: {food} meals
Estimated Water Usage: {water} liters
Estimated Plastic Waste: {plastic} kg
Estimated Electricity Usage: {electricity} kWh

Give recommendations in bullet points.
Keep them short and practical.
"""

    try:
        response = model.generate_content(prompt)
        recommendations = response.text

    except Exception as e:
        recommendations = f"AI recommendations unavailable: {str(e)}"

    return render_template(
        "result.html",
        event_name=event_name,
        attendees=attendees,
        duration=duration,
        venue=venue,
        food_stalls=food_stalls,
        food=food,
        water=water,
        plastic=plastic,
        electricity=electricity,
        score=score,
        recommendations=recommendations
    )


if __name__ == '__main__':
    app.run(debug=True)