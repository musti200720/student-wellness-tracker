# recommender.py
# A simple rule-based wellness recommendation engine.
# These are general wellness tips for a college project, not medical advice.

LEVEL_ORDER = {"alert": 0, "warn": 1, "info": 2, "good": 3}
LEVEL_TAG = {"alert": "Priority", "warn": "Improve", "info": "Note", "good": "Great"}


def make_tip(category, icon, level, title, message, steps):
    """Build one suggestion card as a dictionary."""
    return {
        "category": category,
        "icon": icon,
        "level": level,
        "tag": LEVEL_TAG[level],
        "title": title,
        "message": message,
        "steps": steps,
    }


def calculate_score(sleep, water, exercise, mood):
    """Return a wellness score from 0 to 100."""
    # Sleep (max 35)
    if 7 <= sleep <= 9:
        sleep_score = 35
    elif 6 <= sleep < 7 or 9 < sleep <= 10:
        sleep_score = 25
    elif 5 <= sleep < 6:
        sleep_score = 15
    else:
        sleep_score = 5

    # Water (max 25): 8 glasses gives full marks
    water_score = round(min(water / 8, 1) * 25)

    # Exercise (max 25): 30 minutes gives full marks
    exercise_score = round(min(exercise / 30, 1) * 25)

    # Mood (max 15)
    mood_points = {"Happy": 15, "Calm": 15, "Tired": 8, "Stressed": 5}
    mood_score = mood_points.get(mood, 8)

    return sleep_score + water_score + exercise_score + mood_score


def get_rating(score):
    """Turn the score into a label, a CSS class and a short message."""
    if score >= 80:
        return {"label": "Excellent", "css": "excellent",
                "message": "You are taking great care of yourself today. Keep it up!"}
    elif score >= 60:
        return {"label": "Good", "css": "good",
                "message": "A good day overall, with a few small things to improve."}
    elif score >= 40:
        return {"label": "Fair", "css": "fair",
                "message": "Some habits need attention. Small changes today can help."}
    else:
        return {"label": "Needs Attention", "css": "attention",
                "message": "Today was tough on your habits. Follow the steps below to get back on track."}


def get_suggestions(sleep, water, exercise, mood):
    """Return a list of suggestion cards, most important first."""
    tips = []

    # ---------- Sleep ----------
    if sleep < 5:
        tips.append(make_tip(
            "Sleep", "😴", "alert", "Very low sleep",
            f"You slept only {sleep:g} hours. Most adults need 7 to 9 hours.",
            ["Go to bed 1 to 2 hours earlier tonight.",
             "Avoid caffeine in the afternoon and keep your phone away 30 minutes before bed.",
             "If you feel sleepy during the day, take a short nap of about 20 minutes, not longer."]))
    elif sleep < 7:
        tips.append(make_tip(
            "Sleep", "🌙", "warn", "Sleep a little more",
            f"You slept {sleep:g} hours, a bit under the recommended 7 to 9 hours.",
            ["Try going to bed 30 to 60 minutes earlier.",
             "Keep a fixed sleep and wake-up time, even on weekends.",
             "Avoid heavy meals late at night."]))
    elif sleep <= 9:
        tips.append(make_tip(
            "Sleep", "🌟", "good", "Healthy sleep",
            f"{sleep:g} hours of sleep is in the healthy range.",
            ["Keep the same bedtime routine.",
             "Keep your room dark and cool for good quality sleep."]))
    else:
        tips.append(make_tip(
            "Sleep", "⏰", "info", "A lot of sleep",
            f"You slept {sleep:g} hours. Sleeping much more than 9 hours can leave you groggy.",
            ["Set a consistent wake-up alarm.",
             "Get some daylight within an hour of waking up.",
             "If you often sleep this long and still feel tired, consider speaking to a doctor."]))

    # ---------- Water ----------
    if water < 4:
        tips.append(make_tip(
            "Water", "💧", "alert", "Low water intake",
            f"You drank only {water} glasses. Aim for about 8 glasses a day.",
            ["Drink a glass of water right now.",
             "Keep a water bottle in your bag or on your study desk.",
             "Set a reminder to drink every 2 hours."]))
    elif water < 8:
        tips.append(make_tip(
            "Water", "🚰", "warn", "Drink a bit more water",
            f"You drank {water} glasses, which is a good start. Aim for about 8.",
            ["Have a glass of water with each remaining meal.",
             "Carry a bottle so water is always within reach."]))
    else:
        tips.append(make_tip(
            "Water", "🥤", "good", "Well hydrated",
            f"{water} glasses of water. You are meeting your hydration goal.",
            ["Keep sipping water through the day."]))

    # ---------- Exercise ----------
    if exercise == 0:
        tips.append(make_tip(
            "Exercise", "🚶", "warn", "No exercise today",
            "You did not exercise today. Even a little movement helps your body and mind.",
            ["Take a 10-minute walk after your next meal.",
             "Use the stairs instead of the lift.",
             "Do 5 minutes of stretching before bed."]))
    elif exercise < 30:
        tips.append(make_tip(
            "Exercise", "🏃", "warn", "A little more movement",
            f"You exercised for {exercise} minutes. Aim for about 30 minutes a day.",
            ["Add another 10-minute walk or jog.",
             "Try quick exercises such as squats or push-ups.",
             "Stretch for a few minutes to stay flexible."]))
    elif exercise < 60:
        tips.append(make_tip(
            "Exercise", "💪", "good", "Great job staying active",
            f"{exercise} minutes of exercise meets the daily goal.",
            ["Mix cardio with strength exercises during the week.",
             "Do not forget to stretch after exercising."]))
    else:
        tips.append(make_tip(
            "Exercise", "🏅", "good", "Very active day",
            f"{exercise} minutes of exercise is excellent.",
            ["Eat a balanced meal with some protein to help recovery.",
             "Drink extra water after a long workout.",
             "Include a rest day in your week."]))

    # ---------- Mood ----------
    if mood == "Stressed":
        tips.append(make_tip(
            "Mood", "🧘", "warn", "Manage your stress",
            "You said you are feeling stressed today.",
            ["Take 5 slow deep breaths: in for 4 seconds, out for 6 seconds.",
             "Write down what is worrying you, then pick one small thing to do first.",
             "Talk to a friend, family member or your college counsellor, especially if the stress continues for many days."]))
    elif mood == "Tired":
        tips.append(make_tip(
            "Mood", "🔋", "info", "Feeling tired",
            "You said you are feeling tired today.",
            ["Check your water intake, since dehydration can cause tiredness.",
             "Take a short walk in daylight to wake up your body.",
             "Eat a light snack with some protein, such as nuts or fruit with yogurt."]))
    else:
        tips.append(make_tip(
            "Mood", "😊", "good", "Positive mood",
            f"You are feeling {mood.lower()} today. That is great to see.",
            ["Note what made today good so you can repeat it.",
             "Share your positive energy with a friend."]))

    # ---------- Combined rules ----------
    if mood == "Tired" and sleep < 7:
        tips.append(make_tip(
            "Combined", "🛌", "warn", "Your tiredness may be linked to low sleep",
            "Feeling tired after a short night is very common.",
            ["Make an early night your top priority today.",
             "Avoid caffeine after 3 PM so it does not delay your sleep."]))

    if mood == "Stressed" and exercise < 30:
        tips.append(make_tip(
            "Combined", "🌳", "warn", "Movement can ease stress",
            "Light exercise is a proven way to lift your mood.",
            ["Go for a 10-minute walk outdoors.",
             "Try gentle stretching or yoga for a few minutes."]))

    if mood == "Stressed" and sleep < 6:
        tips.append(make_tip(
            "Combined", "📝", "alert", "Stress and low sleep feed each other",
            "Stress makes it harder to sleep, and poor sleep makes stress worse.",
            ["Wind down for 30 minutes before bed without screens.",
             "Write tomorrow's to-do list tonight so your mind can rest."]))

    # Most important first (sort is stable, so equal levels keep their order)
    tips.sort(key=lambda tip: LEVEL_ORDER[tip["level"]])
    return tips