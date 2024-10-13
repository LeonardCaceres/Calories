import tkinter as tk
from tkinter import messagebox, ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# --- Калькулятор ИМТ ---

def CalculateMBI():
    """Рассчитывает ИМТ и выводит результат в диалоговом окне."""
    try:
        kg = float(weight_ent.get())
        m = float(height_ent.get()) / 100
        bmi = kg / m**2
        bmi = round(bmi, 1)
        print(bmi)
        if bmi <= 18.5:
            messagebox.showinfo('bmi-pythonguides', f'ИМТ = {bmi} соответствует недостаточному весу Тора')
        elif (bmi > 18.5) and (bmi <= 24.9):
            messagebox.showinfo('bmi-pythonguides', f'ИМТ = {bmi} соответствует нормальному весу Тора')
        elif (bmi > 24.9) and (bmi < 29.9):
            messagebox.showinfo('bmi-pythonguides', f'ИМТ = {bmi} соответствует избыточному весу Тора')
        else:
            messagebox.showinfo('bmi-pythonguides', f'ИМТ = {bmi} соответствует ожирению Тора')
    except ValueError:
        messagebox.showerror('Ошибка', 'Введите корректные данные.')

# --- Калькулятор калорий ---

class FoodItem:
    """Представляет собой информацию о блюде."""
    def __init__(self, name, calories, protein, fats, carbs):
        self.name = name
        self.calories = calories
        self.protein = protein
        self.fats = fats
        self.carbs = carbs

    def __str__(self):
        return f"{self.name} (Калории: {self.calories}, Белки: {self.protein}, Жиры: {self.fats}, Углеводы: {self.carbs})"

class CalorieTracker:
    """Класс для отслеживания потребления калорий."""
    def __init__(self):
        self.food_items = []
        self.consumed_calories = []
        self.dates = []
        self.daily_calorie_goal = 0  # Добавлен атрибут для хранения дневной нормы калорий

    def add_food(self):
        """Добавляет новое блюдо в список."""
        name = food_name_ent.get()
        try:
            calories = float(calories_ent.get())
            protein = float(protein_ent.get())
            fats = float(fats_ent.get())
            carbs = float(carbs_ent.get())
        except ValueError:
            messagebox.showerror('Ошибка', 'Введите корректные числовые данные.')
            return

        self.food_items.append(FoodItem(name, calories, protein, fats, carbs))
        food_name_ent.delete(0, tk.END)
        calories_ent.delete(0, tk.END)
        protein_ent.delete(0, tk.END)
        fats_ent.delete(0, tk.END)
        carbs_ent.delete(0, tk.END)
        self.update_food_list()
    def find_food(self):
        """Ищет блюдо по названию."""
        name = search_ent.get()
        for item in self.food_items:
            if item.name == name:
                food_name_ent.insert(0, item.name)
                calories_ent.insert(0, item.calories)
                protein_ent.insert(0, item.protein)
                fats_ent.insert(0, item.fats)
                carbs_ent.insert(0, item.carbs)
                return
        messagebox.showinfo('Информация', 'Блюдо не найдено.')

    def edit_food(self):
        """Редактирует выбранное блюдо."""
        try:
            index = food_listbox.curselection()[0]
            item = self.food_items[index]
            item.name = food_name_ent.get()
            item.calories = float(calories_ent.get())
            item.protein = float(protein_ent.get())
            item.fats = float(fats_ent.get())
            item.carbs = float(carbs_ent.get())
            self.update_food_list()
        except IndexError:
            messagebox.showinfo('Информация', 'Выберите блюдо для редактирования.')

    def delete_food(self):
        """Удаляет выбранное блюдо."""
        try:
            index = food_listbox.curselection()[0]
            del self.food_items[index]
            self.update_food_list()
        except IndexError:
            messagebox.showinfo('Информация', 'Выберите блюдо для удаления.')

    def update_food_list(self):
        """Обновляет список блюд."""
        food_listbox.delete(0, tk.END)
        for item in self.food_items:
            food_listbox.insert(tk.END, item)

    def add_consumed_calories(self):
        """Добавляет потребленные калории."""
        try:
            calories = float(consumed_calories_ent.get())
            date = date_ent.get()
            self.consumed_calories.append(calories)
            self.dates.append(date)
            consumed_calories_ent.delete(0, tk.END)
            date_ent.delete(0, tk.END)
            self.update_calorie_chart()
        except ValueError:
            messagebox.showerror('Ошибка', 'Введите корректные данные.')

    def set_daily_calorie_goal(self):
        """Устанавливает дневную норму калорий."""
        try:
            self.daily_calorie_goal = float(daily_calorie_goal_ent.get())
            daily_calorie_goal_ent.delete(0, tk.END)
        except ValueError:
            messagebox.showerror('Ошибка', 'Введите корректные числовые данные.')

    def update_calorie_chart(self):
        """Обновляет график потребления калорий."""
        global chart
        try:
            fig, ax = plt.subplots()
            ax.plot(self.dates, self.consumed_calories)
            ax.set_xlabel('Дата')
            ax.set_ylabel('Потребленные калории')
            ax.set_title('Динамика потребления калорий')

            # Добавляем линию дневной нормы калорий на график
            if self.daily_calorie_goal > 0:
                ax.axhline(y=self.daily_calorie_goal, color='r', linestyle='--', label='Дневная норма Тора')
                ax.legend()

            canvas = FigureCanvasTkAgg(fig, master=calorie_chart_frame)
            canvas_widget = canvas.get_tk_widget()
            canvas_widget.pack(fill=tk.BOTH, expand=True)

            if chart is not None:
                chart.destroy()

            chart = canvas_widget
        except IndexError:
            messagebox.showinfo('Информация', 'Недостаточно данных для построения графика.')

    def add_meal_to_consumed_calories(self):
        """Добавляет блюдо в список потребленных калорий."""
        try:
            selected_index = food_listbox.curselection()[0]
            selected_food = self.food_items[selected_index]
            grams = float(grams_ent.get())  # Получаем количество грамм блюда
            # Рассчитываем количество калорий в выбранном количестве грамм
            calories_per_gram = selected_food.calories / 100
            consumed_calories = calories_per_gram * grams

            date = date_ent.get()
            self.consumed_calories.append(consumed_calories)
            self.dates.append(date)
            grams_ent.delete(0, tk.END)
            date_ent.delete(0, tk.END)
            self.update_calorie_chart()
        except IndexError:
            messagebox.showinfo('Информация', 'Выберите блюдо из списка.')
        except ValueError:
            messagebox.showerror('Ошибка', 'Введите корректные числовые данные.')


# --- Главное окно приложения ---

window = tk.Tk()
window.title("Приложение для подсчета калорий для Тора")
window.geometry('800x600')

# --- Фрейм для калькулятора ИМТ ---
bmi_frame = tk.Frame(window, padx=10, pady=10)
bmi_frame.pack(pady=10)

# --- Калькулятор ИМТ ---

height_lb = tk.Label(bmi_frame, text="Введите свой рост (в см)")
height_lb.grid(row=0, column=0)

weight_lb = tk.Label(bmi_frame, text="Введите свой вес (в кг)")
weight_lb.grid(row=1, column=0)

height_ent = tk.Entry(bmi_frame)
height_ent.grid(row=0, column=1)

weight_ent = tk.Entry(bmi_frame)
weight_ent.grid(row=1, column=1)

calculate_bmi_button = tk.Button(bmi_frame, text="Рассчитать ИМТ", command=CalculateMBI)
calculate_bmi_button.grid(row=2, column=1, pady=5)

# --- Фрейм для отслеживания потребления калорий ---

calorie_tracker = CalorieTracker()

main_frame = tk.Frame(window, padx=10, pady=10)
main_frame.pack(pady=10)

# --- Фрейм для добавления блюд ---
food_frame = tk.Frame(main_frame)
food_frame.pack(side=tk.LEFT, padx=10)

food_name_lb = tk.Label(food_frame, text="Название блюда:")
food_name_lb.grid(row=0, column=0)

calories_lb = tk.Label(food_frame, text="Калории (на 100г):")
calories_lb.grid(row=1, column=0)

protein_lb = tk.Label(food_frame, text="Белки (на 100г):")
protein_lb.grid(row=2, column=0)

fats_lb = tk.Label(food_frame, text="Жиры (на 100г):")
fats_lb.grid(row=3, column=0)

carbs_lb = tk.Label(food_frame, text="Углеводы (на 100г):")
carbs_lb.grid(row=4, column=0)

food_name_ent = tk.Entry(food_frame)
food_name_ent.grid(row=0, column=1)

calories_ent = tk.Entry(food_frame)
calories_ent.grid(row=1, column=1)

protein_ent = tk.Entry(food_frame)
protein_ent.grid(row=2, column=1)

fats_ent = tk.Entry(food_frame)
fats_ent.grid(row=3, column=1)

carbs_ent = tk.Entry(food_frame)
carbs_ent.grid(row=4, column=1)

add_food_button = tk.Button(food_frame, text="Добавить блюдо", command=calorie_tracker.add_food)
add_food_button.grid(row=5, column=1, pady=5)

# --- Фрейм для поиска и редактирования блюд ---

search_frame = tk.Frame(main_frame)
search_frame.pack(side=tk.LEFT, padx=10)

search_lb = tk.Label(search_frame, text="Поиск блюда:")
search_lb.grid(row=0, column=0)

search_ent = tk.Entry(search_frame)
search_ent.grid(row=0, column=1)

find_food_button = tk.Button(search_frame, text="Найти", command=calorie_tracker.find_food)
find_food_button.grid(row=1, column=0, pady=5)

edit_food_button = tk.Button(search_frame, text="Редактировать", command=calorie_tracker.edit_food)
edit_food_button.grid(row=1, column=1, pady=5)

delete_food_button = tk.Button(search_frame, text="Удалить", command=calorie_tracker.delete_food)
delete_food_button.grid(row=2, column=0, columnspan=2, pady=5)

# --- Фрейм для списка блюд ---

food_listbox_frame = tk.Frame(main_frame)
food_listbox_frame.pack(side=tk.LEFT, padx=10)

food_listbox = tk.Listbox(food_listbox_frame, width=30, height=10)
food_listbox.pack(side=tk.LEFT)

scrollbar =tk.Scrollbar(food_listbox_frame, orient=tk.VERTICAL)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

food_listbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=food_listbox.yview)

# --- Фрейм для добавления блюда в потребленные калории ---

meal_frame = tk.Frame(window, padx=10, pady=10)
meal_frame.pack(pady=10)

grams_lb = tk.Label(meal_frame, text="Граммы:")
grams_lb.grid(row=0, column=0)

grams_ent = tk.Entry(meal_frame)
grams_ent.grid(row=0, column=1)

add_meal_button = tk.Button(meal_frame, text="Добавить блюдо в калории", command=calorie_tracker.add_meal_to_consumed_calories)
add_meal_button.grid(row=1, column=1, pady=5)

# --- Фрейм для ввода дневной нормы калорий ---

calorie_goal_frame = tk.Frame(window, padx=10, pady=10)
calorie_goal_frame.pack(pady=10)

daily_calorie_goal_lb = tk.Label(calorie_goal_frame, text="Дневная норма калорий:")
daily_calorie_goal_lb.grid(row=0, column=0)

daily_calorie_goal_ent = tk.Entry(calorie_goal_frame)
daily_calorie_goal_ent.grid(row=0, column=1)

set_calorie_goal_button = tk.Button(calorie_goal_frame, text="Установить норму", command=calorie_tracker.set_daily_calorie_goal)
set_calorie_goal_button.grid(row=1, column=1, pady=5)

# --- Фрейм для отслеживания потребления калорий ---

consumed_calories_frame = tk.Frame(window, padx=10, pady=10)
consumed_calories_frame.pack(pady=10)

consumed_calories_lb = tk.Label(consumed_calories_frame, text="Потребленные калории:")
consumed_calories_lb.grid(row=0, column=0)

date_lb = tk.Label(consumed_calories_frame, text="Дата:")
date_lb.grid(row=1, column=0)

consumed_calories_ent = tk.Entry(consumed_calories_frame)
consumed_calories_ent.grid(row=0, column=1)

date_ent = tk.Entry(consumed_calories_frame)
date_ent.grid(row=1, column=1)

add_consumed_calories_button = tk.Button(consumed_calories_frame, text="Добавить", command=calorie_tracker.add_consumed_calories)
add_consumed_calories_button.grid(row=2, column=1, pady=5)

# --- Фрейм для графика ---

calorie_chart_frame = tk.Frame(window, padx=10, pady=10)
calorie_chart_frame.pack(pady=10)

chart = None

calorie_tracker.update_food_list()

window.mainloop()