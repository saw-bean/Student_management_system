from tkinter import ttk
from tkinter import *
import tkinter
import sqlite3


class database:
    # connection dir property----------------------------------------------------
    db_name = 'database.db'

    def __init__(self, window):

        # Initializations ----------------------------------------------  
        self.wind = window
        self.wind.title('Database')
        


        # Creating a Frame Container ------------------------------------------------  
        frame = LabelFrame(self.wind, text = 'Fill your information')
        frame.grid(row = 0, column = 0, columnspan = 3, pady = 20)

        # Name Input------------------------------------------------------
        Label(frame, text = 'Name: ').grid(row = 1, column = 0)
        self.name = Text(frame, width=20,height=3)
        self.name.config(font=("consolas", 12), undo=True, wrap='word')
        self.name.focus()
        self.name.grid(row = 1, column = 1)

        self.scrollb = Scrollbar(frame, command=self.name.yview)
        self.scrollb.grid(row=1, column=1, sticky='ns', columnspan=3)
        self.name['yscrollcommand'] = self.scrollb.set
        #Grade input--------------------------------------------------
        Label(frame, text = 'Grade: ').grid(row = 2, column = 0)
        self.Grade = Text(frame, width=20,height=3)
        self.Grade.config(font=("consolas", 12), undo=True, wrap='word')
        self.Grade.focus()
        self.Grade.grid(row = 2, column = 1)
        #scrollbar----------------------------------------------------
        self.scrollb = Scrollbar(frame, command=self.Grade.yview)
        self.scrollb.grid(row=2, column=1, sticky='ns', columnspan=3)
        self.Grade['yscrollcommand'] = self.scrollb.set
        #Gender input-------------------------------------------------------------
        Label(frame, text = 'Gender: ').grid(row = 3, column = 0)
        self.Gender = Text(frame,width=20,height=3)
        self.Gender.config(font=("consolas", 12), undo=True, wrap='word')
        self.Gender.focus()
        self.Gender.grid(row = 3, column = 1)
        #scrollbar---------------------------------------------------------------
        self.scrollb = Scrollbar(frame, command=self.Gender.yview)
        self.scrollb.grid(row=3, column=1, sticky='ns', columnspan=3)
        self.Gender['yscrollcommand'] = self.scrollb.set

        self.tree = ttk.Treeview(frame,columns=("Name", "Grade"))
        self.tree.heading("#0", text="Name", anchor= CENTER)
        self.tree.heading("#1", text="Grade", anchor= CENTER)
        self.tree.heading("#2", text="Gender", anchor= CENTER)        
        self.tree.grid(row = 4, column = 0, columnspan = 5, ipady=10)

        self.scrollb = Scrollbar(frame, command=self.tree.yview)
        self.scrollb.grid(row=4, column=5, sticky='ns', rowspan=1)
        self.tree['yscrollcommand'] = self.scrollb.set

        # Button Add database --------------------------------------------------
        ttk.Button(frame, text = 'Insert', command = self.add_database).grid(row = 5, column = 1, sticky = W + E)
        ttk.Button(frame, text = 'DELETE', command = self.delete_database).grid(row = 5, column = 2, sticky = W + E)
        ttk.Button(frame, text = 'EDIT', command = self.edit_database).grid(row = 5, column = 3, sticky = W + E)

        # Output Messages ------------------------------------------------------
        self.message = Label(text = '', fg = 'red')
        self.message.grid(row = 7, column = 0, columnspan = 3, sticky = W + E)


        # Filling the Rows-------------------------------------------------------
        
        self.get_database()

    # Function to Execute Database Querys----------------------------------------------

    def run_query(self, query, parameters = ()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS database (id INTEGER PRIMARY KEY , name TEXT, Grade TEXT, Gender TEXT)")
            result = cursor.execute(query, parameters)
            conn.commit()
        return result

    def get_database(self):
        # cleaning Table ----------------------------------------------------------------
 
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element) 

        query = 'SELECT * FROM database ORDER BY name DESC'
        db_rows = self.run_query(query)


        for row in db_rows:

            self.tree.insert('', 0, text = row[1], values = (row[2],row[3]))

    # vvalidation
    def validation(self):
        return (self.name.get(1.0, END)),(self.Grade.get(1.0, END), (self.Gender.get(1.0, END)))

    def add_database(self):
        if self.validation():
            query = 'INSERT INTO database VALUES(NULL, ?, ?, ?)'
            parameters =  (self.name.get(1.0, END), self.Grade.get(1.0, END), self.Gender.get(1.0, END))
            self.run_query(query, parameters)
            self.message['text'] = 'database {} added Successfully'.format(self.name.get(1.0, END))
            self.name.delete(1.0, END)
            self.Grade.delete(1.0, END)
            self.Gender.delete(1.0, END)
        else:
            self.message['text'] = 'Name and Data is Required'
        self.get_database()

    def delete_database(self):
        self.message['text'] = ''
        try:
           self.tree.item(self.tree.selection())['text'][0]
        except IndexError as e:
            self.message['text'] = 'Please select a Record'
            return
        self.message['text'] = ''
        name = self.tree.item(self.tree.selection())['text']
        query = 'DELETE FROM database WHERE name = ?'
        self.run_query(query, (name, ))
        self.message['text'] = 'Record {} deleted Successfully'.format(name)
        self.get_database()

    def edit_database(self):
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['values'][0]
        except IndexError as e:
            self.message['text'] = 'Please, select Record'
            return
        name = self.tree.item(self.tree.selection())['text']
        Grade = self.tree.item(self.tree.selection())['values'][0]
        Gender = self.tree.item(self.tree.selection())['values'][1]

        self.edit_wind = Toplevel()
        self.edit_wind.title = 'Edit Civilization'
        frame2 = LabelFrame(self.edit_wind, text = 'Edit your information')
        frame2.grid(row = 0, column = 0, columnspan = 3, pady = 20)

        self.nomelab = Label(frame2, text = 'Name: ').grid(row = 1, column = 0)


        message2 = Text(frame2, height=5, width=50)
        message2.config(font=("consolas", 12), undo=True, wrap='word')
        message2.insert(END, name)
        message2.grid(row = 2, column = 0, columnspan = 2, sticky = W + E)

        self.descriptlab = Label(frame2, text = 'Grade: ').grid(row = 3, column = 0)

        message3 = Text(frame2, height=5, width=34)
        message3.config(font=("consolas", 12), undo=True, wrap='word')
        message3.insert(END, Grade)
        message3.grid(row = 4, column = 0, columnspan = 2, sticky = W + E)

        self.Genderlab = Label(frame2, text = 'Gender: ').grid(row = 5, column = 0)

        message4 = Text(frame2, height=5, width=34)
        message4.config(font=("consolas", 12), undo=True, wrap='word')
        message4.insert(END, Gender)
        message4.grid(row = 6, column = 0, columnspan = 2, sticky = W + E)

        ttk.Button(
            frame2, text = 'Update', 
            command = lambda: self.update_castro(name, message2, message3, message4)
        ).grid(row = 7, column = 3, sticky = W + E)

    def update_castro(self, old_name, message2, message3, message4):
        message2 = message2.get(1.0, END)
        message3 = message3.get(1.0, END)
        message4 = message4.get(1.0, END)

        query = 'UPDATE database set name = ?, Grade = ?, Gender = ? WHERE name = ?'
        self.run_query(query, (message2, message3, message4, old_name ))

        self.get_database()
        self.edit_wind.destroy()

if __name__ == '__main__':
    window = Tk()

    application = database(window)
    window.mainloop()
