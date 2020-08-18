import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from database import ExpancesDB

class Main(tk.Frame):

    def __init__(self, root):
        super().__init__(root)
        # self.parent = parent
        self.__db = ExpancesDB()
        self.init_main()
        self.view_records()


    #главное окно
    def init_main(self):
        self.add_img = tk.PhotoImage(file="images/add.png")
        self.update_img = tk.PhotoImage(file="images/update.png")
        self.delete_img = tk.PhotoImage(file='images/delete.png')
        self.search_img = tk.PhotoImage(file="images/search.png")
        
        toolbar = tk.Frame(bg = "#d7d8e0", bd = 5)
        toolbar.pack(side="top", fill="x")
        
        addButton = tk.Button(toolbar, text = u"Добавить позицию", command = lambda: self.open_addexpance(), image = self.add_img, 
                                compound = 'top', relief = 'flat', font = ('Verdana', 8), bg = "#d7d8e0")
        addButton.pack(side = 'left')

        apdateButton = tk.Button(toolbar, text = u"Редактировать", command = lambda: self.open_updateexpance(), image = self.update_img, 
                                compound = 'top', relief='flat', font=('Verdana', 8), bg = "#d7d8e0") 
        apdateButton.pack(side = "left")

        deleteButton = tk.Button(toolbar, text=u"Удалить", command=lambda: self.delete_record(), image=self.delete_img,
                                 compound='top', relief='flat', font=('Verdana', 8), bg="#d7d8e0")
        deleteButton.pack(side="left", padx = 15)

        searchButton = tk.Button(toolbar, text=u"Найти", command=lambda: self.open_search(), image=self.search_img,
                                 compound='top', relief='flat', font=('Verdana', 8), bg="#d7d8e0")
        searchButton.pack(side="left", padx=15)

        self.tree = ttk.Treeview(root, columns=('ID', 'description', 'form','total'), height=10, show='headings', selectmode='browse')
        self.tree.column('ID', width=25, anchor='center')
        self.tree.column('description', width=355, anchor='center')
        self.tree.column('form', width=100, anchor='center')
        self.tree.column('total', width=100, anchor='center')

        self.tree.heading('ID', text="№")
        self.tree.heading('description', text="Наименование расхода")
        self.tree.heading('form', text="Тип операции")
        self.tree.heading('total', text="Сумма")
        self.tree.pack()

    def add_records(self, *fields):
        """Функция выполняет валидацию поля на пустое значение, добавляет данные в БД и выводит значения в виджет treeview(см. функцию view_record)"""
        if all(fields): 
            self.__db.insert_data(*fields)
            self.view_records()
        else:
            messagebox.showerror(u'Error', message=u'Заполните поля')
    
    def update_record(self, *fields):
        index = self.tree.set(self.tree.selection()[0], '#1')
        self.__db.update(index,*fields)
        self.view_records()


    def view_records(self):
        """Функция посылает запрос в БД, получает значения полей и выводит значения в виджет treeview"""
        [self.tree.delete(i) for i in self.tree.get_children()]
        for row in self.__db.cursor.execute('''SELECT * FROM homeexpances'''):
            self.tree.insert('', 'end', values=row)

    def set_record_to_vidgets(self, entry_expance, rvbar, entry_expance_sum):
        description=self.tree.set(self.tree.selection()[0], '#2') #собираем значения из полей
        form = self.tree.set(self.tree.selection()[0], '#3')
        cost = self.tree.set(self.tree.selection()[0], '#4')
        #передаем эти значения в виджеты
        entry_expance.set(description)
        rvbar.set(form)
        entry_expance_sum.insert(0, string = cost)

    def delete_record(self):
        element = None
        index = None
        answer = None
        try:
            element = self.tree.selection()[0]
            index = self.tree.set(self.tree.selection()[0], '#1')
        except:
            messagebox.showerror(u'Error', message=u'Выберите поле для удаления')   
        if element:
            answer = messagebox.askyesno(u'Подтверждение удаления', message=u'Вы точно хотите удалить запись?')   
        if answer:
            self.tree.delete(element)
            self.__db.delete(index)

         
    def open_addexpance(self):
        AddExpance()

    def open_updateexpance(self):
        index = None
        try:
            index = self.tree.set(self.tree.selection()[0], '#1')
        except:
            messagebox.showerror(title="Пустое поле",
                                 message="Вы не выбрали запись")
        if index:
            UpdateExpance()

    def open_search(self):
        Search()

    
# дочернее окно
class AddExpance(tk.Toplevel):
    def __init__(self):
        super().__init__(root) 
        self.title(u"Добавить расход/доход")
        self.geometry('400x220+400+300')
        self.resizable(False, False)
        self.rvbar = tk.StringVar()
        self.rvbar.set(u'Доход')
        self.view = app
        expense = tk.Label(self, text=u"Наименование")
        expense_type = tk.Label(self, text=u"Тип расхода")
        expense_sum = tk.Label(self, text=u"Сумма:")
        expense.place(x=50, y=50)
        expense_type.place(x=50, y=80)
        expense_sum.place(x=50, y=110)
        self.entry_expense = ttk.Combobox(self, values=[u'Зарплата', 
                                                   u'Накопления',  
                                                   u'Еда',  
                                                   u'Жилье', 
                                                   u'Развлечения', 
                                                   u'Путешествия', 
                                                   u'Долг', 
                                                   u'Кредит', 
                                                   u'Такси', 
                                                   u'Транспорт', 
                                                   u'Здоровье', 
                                                   u'Разное'], state= "readonly" , width=17)
        entry_expense_type1 = tk.Radiobutton(
            self, text=u'Доход', value=u'Доход', variable=self.rvbar)
        entry_expense_type2 = tk.Radiobutton(self, text=u'Расход', value=u'Расход', variable = self.rvbar)
        self.entry_expense_sum = tk.Entry(self)

        self.entry_expense.place(x = 150, y = 50)
        entry_expense_type1.place(x = 150, y = 80)
        entry_expense_type2.place(x=210, y=80)
        self.entry_expense_sum.place(x=150, y=110)

        self.button_accept = tk.Button(self, text=u"Добавить", command= lambda: self.view.add_records(self.entry_expense.get(),
                                                                                                      self.rvbar.get(),
                                                                                                      self.entry_expense_sum.get()))
        self.button_accept.place(x = 100, y = 150)
        self.button_cancel = tk.Button(self, text = u"Отменить", command = self.destroy)
        self.button_cancel.place(x = 200,  y = 150)
        
        self.grab_set()
        self.focus_set()
        # self.wait_window()


class UpdateExpance(AddExpance):
    def __init__(self):
        super().__init__()
        self.title(u"Редактировать запись")
        self.button_accept.destroy()
        self.view.set_record_to_vidgets(self.entry_expense, self.rvbar, self.entry_expense_sum)
        button_update = tk.Button(self, text=u"Изменить", command=lambda: self.view.update_record(self.entry_expense.get(),
                                                                                                   self.rvbar.get(),
                                                                                                   self.entry_expense_sum.get()))
        button_update.place(x=100, y=150)


class Search(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.title(u"Поиск")
        self.geometry('400x220+400+300')
        self.resizable(False, False)
        search_field_name = tk.Label(self, text=u"Что ищем?")
        search_field_name.place (x = 175, y = 50)
        search_field = tk.Entry(self)
        search_field.place(x= 150, y=70)


if __name__ == "__main__":
    root = tk.Tk()
    app = Main(root)
    root.title(u"Мои финансы")
    root.geometry("650x450+300+200")
    root.resizable(False, False)
    root.mainloop()


