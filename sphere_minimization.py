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
    dx = abs(bounds[0][1] - bounds[0][0])
    dy = abs(bounds[1][1] - bounds[1][0])
    step = max(dx, dy) / iterations

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

        # Перевірка умови зупинки: зміна значення менша за epsilon або нове значення більше за поточне
        if next_value > current_value:
            # print("next_value > current_value")
            break
        if abs(next_value - current_value) < epsilon:
            # print("abs(next_value - current_value) < epsilon")
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
    dx = abs(bounds[0][1] - bounds[0][0])
    dy = abs(bounds[1][1] - bounds[1][0])
    step = max(dx, dy) / iterations

    # Визначаємо розмірність простору пошуку
    dimension = len(bounds)
    # Ініціалізуємо першу точку випадково в межах bounds
    current_point = [random.uniform(*bounds[i]) for i in range(dimension)]
    current_value = func(current_point)

    for _ in range(iterations):
        # Генеруємо випадкового кандидата в межах bounds
        new_point = get_random_neighbor(current_point, step)
        new_value = func(new_point)
        deviation = new_value - current_value

        # Перевірка умови переходу до нової точки
        if new_value < current_value:
            current_point, current_value = new_point, new_value

        # Перевірка умови зупинки: зміна значення менша за epsilon
        if abs(deviation) < epsilon:
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
    pass


if __name__ == "__main__":
    # Межі для функції
    bounds = [(-5, 5), (-5, 5)]

    # Виконання алгоритмів
    print("Hill Climbing:")
    hc_solution, hc_value = hill_climbing(sphere_function, bounds)
    print("Розв'язок:", hc_solution, "Значення:", hc_value)

    print("\nRandom Local Search:")
    rls_solution, rls_value = random_local_search(sphere_function, bounds)
    print("Розв'язок:", rls_solution, "Значення:", rls_value)

    print("\nSimulated Annealing:")
    # sa_solution, sa_value = simulated_annealing(sphere_function, bounds)
    # print("Розв'язок:", sa_solution, "Значення:", sa_value)
