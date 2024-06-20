def calculate_daily_calories(data):
    age = data['age']
    height = data['height']
    weight = data['weight']
    activity = data['activity']
    goal = data['goal']

    bmr = 10 * weight + 6.25 * height - 5 * age + 5  # для мужчин
    if activity == 'низкий':
        daily_calories = bmr * 1.2
    elif activity == 'средний':
        daily_calories = bmr * 1.55
    else:  # высокий уровень активности
        daily_calories = bmr * 1.75

    if goal == 'похудение':
        daily_calories -= 500
    elif goal == 'набор веса':
        daily_calories += 500

    return int(daily_calories)

def calculate_bju(daily_calories):
    proteins = daily_calories * 0.3 / 4
    fats = daily_calories * 0.3 / 9
    carbs = daily_calories * 0.4 / 4
    return {'proteins': int(proteins), 'fats': int(fats), 'carbs': int(carbs)}