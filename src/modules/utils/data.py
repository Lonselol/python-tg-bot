PRODUCT_DATA = {
    'творог': {'calories': 98, 'proteins': 18, 'fats': 1, 'carbs': 3},
    'яблоко': {'calories': 52, 'proteins': 0.3, 'fats': 0.2, 'carbs': 14},
    # Добавьте другие продукты по необходимости
}

def get_product_info(product_name):
    return PRODUCT_DATA.get(product_name.lower())

def calculate_meal_bju(meal_description):
    meal_items = meal_description.split(',')
    total_calories = total_proteins = total_fats = total_carbs = 0

    for item in meal_items:
        product_name, weight = item.strip().split()
        weight = int(weight[:-1])  # убираем "г"
        product_info = get_product_info(product_name)
        if product_info:
            total_calories += product_info['calories'] * weight / 100
            total_proteins += product_info['proteins'] * weight / 100
            total_fats += product_info['fats'] * weight / 100
            total_carbs += product_info['carbs'] * weight / 100

    return {
        'calories': int(total_calories),
        'proteins': int(total_proteins),
        'fats': int(total_fats),
        'carbs': int(total_carbs)
    }