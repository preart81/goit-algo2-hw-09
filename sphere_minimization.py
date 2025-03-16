import random
import math

from pprint import pprint


# Визначення функції Сфери
def sphere_function(x):
    return sum(xi**2 for xi in x)


# Hill Climbing
def hill_climbing(func, bounds, iterations=1000, epsilon=1e-6):
    """
    Hill Climbing - алгоритм пошуку глобального мінімуму функції.

    Args:
        func (function): Функція для пошуку мінімуму.
        bounds (list): Межі для пошуку мінімуму.
        iterations (int, optional): Кількість ітерацій. По замовчуванню - 1000.
        epsilon (float, optional): Похибка для зупинки алгоритму. По замовчуванню - 1e-6.

    Returns:
        tuple: Розв'язок та його значення.
    """

    def get_neighbors(point, step=0.5):
        """Функція для визначення сусідів поточної точки

        Args:
            point (tuple): Поточна точка
            step (float): Крок пошуку

        Returns:
            list: Список сусідніх точок
        """
        x, y = point
        return [(x + step, y), (x - step, y), (x, y + step), (x, y - step)]

    # Визначаємо крок пошуку
    step = get_step_size(bounds, iterations)

    dimension = len(bounds)
    current_point = [random.uniform(*bounds[i]) for i in range(dimension)]

    current_value = func(current_point)

    for _ in range(iterations):
        # Створення сусідніх точок
        neighbor_points = get_neighbors(current_point, step)

        # Обробка сусідніх точок
        next_point, next_value = None, float("inf")
        for neighbor_point in neighbor_points:
            neighbor_value = func(neighbor_point)
            if neighbor_value < next_value:
                next_point, next_value = neighbor_point, neighbor_value

        # Перевірка умови зупинки: нове значення більше за поточне - пройшли оптимум
        if next_value > current_value:
            # print("next_value > current_value")
            break
        # Перевірка умови зупинки: зміна значення менша за epsilon або нове значення більше за поточне
        if abs(next_value - current_value) < epsilon:
            # print("abs(next_value - current_value) < epsilon")
            current_point, current_value = next_point, next_value
            break
        # Перевірка умови зупинки: зміна точки менша за epsilon
        if delta_point(current_point, next_point) < epsilon:
            # print("delta_point(current_point, next_point) < epsilon")
            current_point, current_value = next_point, next_value
            break

        current_point, current_value = next_point, next_value

    # Повертаємо розв'язок та його значення
    return current_point, current_value


# Random Local Search
def random_local_search(func, bounds, iterations=1000, epsilon=1e-6):
    """
    Random Local Search - алгоритм пошуку локального мінімуму функції.

    Args:
        func (function): Функція для пошуку локального мінімуму.
        bounds (list): Межі для пошуку локального мінімуму.
        iterations (int, optional): Кількість ітерацій. По замовчуванню - 1000.
        epsilon (float, optional): Похибка для зупинки алгоритму. По замовчуванню - 1e-6.

    Returns:
        tuple: Розв'язок та його значення.
    """

    def get_random_neighbor(current, step=0.5):
        """Функція для визначення випадкового сусіда"""
        x, y = current
        new_x = x + random.uniform(-step, step)
        new_y = y + random.uniform(-step, step)
        return (new_x, new_y)

    # Визначаємо крок пошуку
    step = get_step_size(bounds, iterations)

    # Визначаємо розмірність простору пошуку
    dimension = len(bounds)
    # Ініціалізуємо першу точку випадково в межах bounds
    current_point = [random.uniform(*bounds[i]) for i in range(dimension)]
    current_value = func(current_point)

    for _ in range(iterations):
        # Генеруємо випадкового кандидата в межах bounds
        new_point = get_random_neighbor(current_point, step=0.5)
        new_value = func(new_point)
        delta_value = new_value - current_value

        # Перевірка умови переходу до нової точки
        if new_value < current_value:
            current_point, current_value = new_point, new_value

        # Перевірка умови зупинки: зміна значення менша за epsilon
        if abs(delta_value) < epsilon:
            # print("abs(deviation) < epsilon")
            break

    # Повертаємо розв'язок та його значення
    return current_point, current_value


# Simulated Annealing
def simulated_annealing(func, bounds, iterations=1000, temp=1000, cooling_rate=0.95, epsilon=1e-6):
    """
    Simulated Annealing - алгоритм відпалу.

    Args:
        func (function): Функція для пошуку мінімуму.
        bounds (list): Межі для пошуку мінімуму.
        iterations (int, optional): Кількість ітерацій. По замовчуванню - 1000.
        temp (float, optional): Температура. По замовчуванню - 1000.
        cooling_rate (float, optional): Коефіцієнт зміни температури. По замовчуванню - 0.95.
        epsilon (float, optional): Похибка для зупинки алгоритму. По замовчуванню - 1e-6.

    Returns:
        tuple: Розв'язок та його значення.
    """

    def generate_neighbor(old_point, step=1):
        """Функція для генерації сусіда"""
        x, y = old_point
        new_x = x + random.uniform(-step, step)
        new_y = y + random.uniform(-step, step)
        return (new_x, new_y)

    # Визначаємо розмірність простору пошуку
    dimension = len(bounds)
    # Ініціалізуємо першу точку випадково в межах bounds
    current_point = [random.uniform(*bounds[i]) for i in range(dimension)]
    current_value = func(current_point)

    while temp >= epsilon:
        new_point = generate_neighbor(current_point)
        new_value = func(new_point)
        delta_value = new_value - current_value

        # Перевірка умови зупинки: відстань між точками менша за epsilon
        if delta_point(current_point, new_point) < epsilon:
            # print("Перевірка умови зупинки: відстань між точками менша за epsilon")
            break

        if delta_value < 0 or random.random() < math.exp(-delta_value / temp):
            current_point, current_value = new_point, new_value

        temp *= cooling_rate
    return current_point, current_value


def get_step_size(bounds, iterations=1000):
    """Функція для визначення кроку пошуку"""
    max_delta = max(abs(b[1] - b[0]) for b in bounds)
    step = max_delta / iterations
    return step


def delta_point(point1, point2):
    """Функція для обчислення відстані між двома точками"""
    return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)


if __name__ == "__main__":
    # Межі для функції
    bounds = [(-5, 5), (-5, 5)]

    # Виконання алгоритмів
    print("Hill Climbing:")
    hc_solution, hc_value = hill_climbing(sphere_function, bounds)
    print("Розв'язок:", hc_solution, "Значення:", f"{hc_value:.8f}")

    print("\nRandom Local Search:")
    rls_solution, rls_value = random_local_search(sphere_function, bounds)
    print("Розв'язок:", rls_solution, "Значення:", f"{rls_value:.8f}")

    print("\nSimulated Annealing:")
    sa_solution, sa_value = simulated_annealing(sphere_function, bounds)
    print("Розв'язок:", sa_solution, "Значення:", f"{sa_value:.8f}")
