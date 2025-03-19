from datetime import datetime, timedelta

# Базовый класс для всех товаров
class Product:
    def __init__(self, name, price, quantity):
        self.name = name
        self.price = price
        self.quantity = quantity

    def is_available(self, amount):
        """Проверка наличия товара на складе в нужном количестве"""
        return self.quantity >= amount

# Класс для продуктов питания с информацией о БЖУ и калориях
class FoodProduct(Product):
    def __init__(self, name, price, quantity, proteins, fats, carbs, calories):
        super().__init__(name, price, quantity)
        self.proteins = proteins  # Белки на 100г
        self.fats = fats          # Жиры на 100г
        self.carbs = carbs        # Углеводы на 100г
        self.calories = calories  # Калории на 100г

# Класс для скоропортящихся товаров
class PerishableProduct(Product):
    def __init__(self, name, price, quantity, production_date, shelf_life_days):
        super().__init__(name, price, quantity)
        self.production_date = datetime.strptime(production_date, "%Y-%m-%d")
        self.shelf_life_days = shelf_life_days

    def is_expired(self):
        """Проверка, истек ли срок годности"""
        return datetime.now() > self.production_date + timedelta(days=self.shelf_life_days)

    def will_expire_soon(self):
        """Проверка, истекает ли срок годности менее чем через 24 часа"""
        return datetime.now() + timedelta(days=1) > self.production_date + timedelta(days=self.shelf_life_days)

# Класс для витаминов
class VitaminProduct(Product):
    def __init__(self, name, price, quantity, requires_prescription):
        super().__init__(name, price, quantity)
        self.requires_prescription = requires_prescription  # Требуется ли рецепт

# Класс для товаров, являющихся одновременно продуктами питания и скоропортящимися
class FoodPerishableProduct(FoodProduct, PerishableProduct):
    def __init__(self, name, price, quantity, proteins, fats, carbs, calories, production_date, shelf_life_days):
        FoodProduct.__init__(self, name, price, quantity, proteins, fats, carbs, calories)
        PerishableProduct.__init__(self, name, price, quantity, production_date, shelf_life_days)

# Класс для управления корзиной пользователя
class Cart:
    def __init__(self, user_norms):
        self.items = []  # Список товаров в корзине: (продукт, количество)
        self.user_norms = user_norms  # Нормы БЖУ и калорий: {'proteins': max_p, 'fats': max_f, 'carbs': max_c, 'calories': max_cal}

    def add_item(self, product, amount):
        """Добавление товара в корзину с учетом ограничений"""
        if not product.is_available(amount):
            print(f"Товар {product.name} отсутствует на складе в нужном количестве.")
            return
        if isinstance(product, VitaminProduct) and product.requires_prescription:
            print(f"Товар {product.name} требует рецепта и не может быть продан без него.")
            return
        if isinstance(product, PerishableProduct) and product.will_expire_soon():
            print(f"Товар {product.name} испортится менее чем через 24 часа и не может быть продан.")
            return
        self.items.append((product, amount))

    def calculate_total_cost(self):
        """Расчет общей стоимости товаров в корзине"""
        return sum(product.price * amount for product, amount in self.items)

    def check_nutrition(self):
        """Проверка соответствия нормам БЖУ и калорий"""
        total_proteins = sum(product.proteins * amount / 100 for product, amount in self.items if isinstance(product, FoodProduct))
        total_fats = sum(product.fats * amount / 100 for product, amount in self.items if isinstance(product, FoodProduct))
        total_carbs = sum(product.carbs * amount / 100 for product, amount in self.items if isinstance(product, FoodProduct))
        total_calories = sum(product.calories * amount / 100 for product, amount in self.items if isinstance(product, FoodProduct))

        if total_proteins > self.user_norms['proteins']:
            print("Превышена норма белков.")
        if total_fats > self.user_norms['fats']:
            print("Превышена норма жиров.")
        if total_carbs > self.user_norms['carbs']:
            print("Превышена норма углеводов.")
        if total_calories > self.user_norms['calories']:
            print("Превышена норма калорий.")

# Класс для управления складом
class Warehouse:
    def __init__(self):
        self.products = []  # Список всех товаров на складе

    def add_product(self, product):
        """Добавление товара на склад"""
        self.products.append(product)

    def get_products_to_order(self, min_quantity):
        """Формирование списка товаров для закупки"""
        return [product for product in self.products if product.quantity < min_quantity]

    def get_products_to_dispose(self):
        """Формирование списка товаров для утилизации"""
        return [product for product in self.products if isinstance(product, PerishableProduct) and product.is_expired()]

# Пример использования модуля
if __name__ == "__main__":
    # Создание товаров
    apple = FoodProduct("Яблоко", 100, 50, 0.3, 0.2, 11.2, 47)
    milk = FoodPerishableProduct("Молоко", 80, 20, 3.2, 3.5, 4.7, 60, "2023-10-01", 7)
    vitamins = VitaminProduct("Витамин C", 500, 10, True)

    # Создание склада и добавление товаров
    warehouse = Warehouse()
    warehouse.add_product(apple)
    warehouse.add_product(milk)
    warehouse.add_product(vitamins)

    # Создание корзины с нормами БЖУ и калорий
    user_norms = {'proteins': 50, 'fats': 70, 'carbs': 200, 'calories': 2000}
    cart = Cart(user_norms)

    # Добавление товаров в корзину
    cart.add_item(apple, 200)  # 200г яблок
    cart.add_item(milk, 100)   # 100г молока
    cart.add_item(vitamins, 1) # 1 упаковка витаминов (но требуется рецепт)

    # Проверка норм БЖУ и калорий
    cart.check_nutrition()

    # Расчет стоимости
    print(f"Суммарная стоимость: {cart.calculate_total_cost()}")

    # Управление складом
    print("Товары для закупки:", [p.name for p in warehouse.get_products_to_order(30)])
    print("Товары для утилизации:", [p.name for p in warehouse.get_products_to_dispose()])