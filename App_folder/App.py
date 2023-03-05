import customtkinter as tk
import random
from math import pow
import numpy as np


tk.set_appearance_mode("System")  # задаём оформление приложения
tk.set_default_color_theme("green")  # задаём тему приложению


class Application(tk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("390x150") # Задаём размер окна

        # Блок Label, задаём текст в начальном окне
        self.title('Sim_model')
        self.lbl1 = tk.CTkLabel(master=self, text='Введите размер буфера(L)')
        self.lbl1.grid(row=0, column=0, columnspan=2)
        self.lbl2 = tk.CTkLabel(master=self, text='Введите нач. ГСЧ')
        self.lbl2.grid(row=1, column=0, columnspan=2)

        # Блок Entry, поля для ввода значений L и ГСЧ
        self.entry1 = tk.CTkEntry(master=self, width=90)
        self.entry1.grid(row=0, column=2, columnspan=1, padx=(0, 10), pady=(0, 5))
        self.entry2 = tk.CTkEntry(master=self, width=90)
        self.entry2.grid(row=1, column=2, columnspan=1, padx=(0, 10))

        # Блок Button, делаем кнопку, которая будет запускать алгоритм
        self.btn1 = tk.CTkButton(master=self, text="Запустить модель", width=100, command=self.example, text_color='gold')
        self.btn1.grid(row=0, column=4, columnspan=1)

    def text_get(self): # Получаем текст из поля ввода
        return (int(self.entry1.get()), int(self.entry2.get()))


    def example(self): # Функция, которая вызывается при нажатии на кнопку
        new_win = tk.CTk() # Создаём новое окно
        s = Simulation_model(int(self.entry1.get()), int(self.entry2.get())) # Вызываем класс Simulation_model
        L, gsch = self.text_get()

        # Задаём в новом окне текст на вывод
        lbl = tk.CTkLabel(master=new_win,  text=f"Размер буфера = {L}", font = ("Candara", 14))
        lbl2 = tk.CTkLabel(master=new_win, text=f"Начальное значение ГСЧ = {gsch}", font = ("Candara", 14))
        lbl3 = tk.CTkLabel(master=new_win, text=f"Коэффициент потерь = {s.Simulate()}", font = ("Candara", 14))
        lbl4 = tk.CTkLabel(master=new_win, text=f"Макс. число входных заявок = {s.max_requests}", font = ("Candara", 14))
        lbl5 = tk.CTkLabel(master=new_win, text=f"Средняя длина очереди: {round(s.Avg_queue(), 3)}", font = ("Candara", 14))
        lbl6 = tk.CTkLabel(master=new_win, text='-----------------------------------------')
        lbl7 = tk.CTkLabel(master=new_win, text='Типовые характеристики модели, рассчитанные вручную', font = ("Candara", 14))
        lbl8 = tk.CTkLabel(master=new_win, text=f"Коэффициент потерь = {round(s.P(L), 3)}", font = ("Candara", 14))
        lbl9 = tk.CTkLabel(master=new_win, text=f"Средняя длина очереди = {round(s.queue(L), 3)}", font = ("Candara", 14))
        lbl.grid(row=0, column=0)
        lbl2.grid(row=1, column=0)
        lbl3.grid(row=2, column=0)
        lbl4.grid(row=3, column=0)
        lbl5.grid(row=4, column=0)
        lbl6.grid(row=5, column=0)
        lbl7.grid(row=6, column=0)
        lbl8.grid(row=7, column=0)
        lbl9.grid(row=8, column=0)
        new_win.mainloop()

class Simulation_model: # Класс с реализацией алгоритма
    def __init__(self, L, seed):
        self.L = L  # Емкость буфера
        self.GSCH = seed  # Начальное значение ГСЧ
        self.enter = 9  # Среднее время между появлениями заявок на входе
        self.service = 17  # Cреднее время обслуживания/передачи
        self.requests = 0  # Количество поступивших на вход заявок
        self.max_requests = 250  # Заданное максимальное число входных заявок
        self.lost = 0  # Количество потерянных заявок
        self.n = 0  # Количество заявок в модели
        random.seed(seed)  # Инициализируем имитацию случайного выбора
        self.lst_of_queue = [0] * (self.max_requests + 1)  # Список будет представлять длину очереди

    def P(self, L): # Получаем типовую характеристику коэф. потери заявки
        p = round(self.service/self.enter, 1)
        return (1-p)/(1-pow(p, L+2))*pow(p, L+1)

    def queue(self, L): # Получаем типовую характеристику средней длины очереди
        p = round(self.service/self.enter, 1)
        return (pow(p, 2)/(1-pow(p, L+2))) * (1-pow(p, L)*(1 + L - L*p))/(1-p)

    def Random_number(self, val):  # Генерируем случайное значение
        return -(np.log(random.random()) / (1 / val))

    def Avg_queue(self):  # Непосредственно в методе находим длину очереди
        s = 0
        for i in self.lst_of_queue:
            s += i

        return s / len(self.lst_of_queue)

    def Simulate(self):  # Здесь мы имитируем работу передатчика
        enter_time = self.Random_number(self.enter)
        exit_time = enter_time + self.Random_number(self.service)
        self.n += 1
        self.requests += 1
        enter_time += self.Random_number(self.enter)
        while self.requests != self.max_requests:
            if enter_time < exit_time:
                if (self.n == self.L + 1):
                    self.lost += 1
                else:
                    self.n += 1
                self.requests += 1
                enter_time += self.Random_number(self.enter)
            else:
                self.n -= 1
                if (self.n == 0):
                    exit_time = enter_time + self.Random_number(self.service)
                    self.n += 1
                    self.requests += 1
                    enter_time += self.Random_number(self.enter)

                else:
                    exit_time += self.Random_number(self.service)
            self.lst_of_queue[self.requests] = self.n - 1 if self.n - 1 >= 0 else 0

        return self.lost / self.max_requests  # Возвращаем коэффициент потерь