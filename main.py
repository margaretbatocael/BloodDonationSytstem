import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3
from PIL import ImageTk, Image

class Application(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title("Blood Donation System")
        self.geometry("1200x480")
        self.resizable(False, False)

        self.receptacle = tk.Frame(self)
        self.receptacle.pack(side="top", fill="both", expand=True)
        self.receptacle.grid_rowconfigure(0, weight=1)
        self.receptacle.grid_columnconfigure(0, weight=1)

        self.frames = {}

        self.display_a_page(First_Page)
        
    def display_a_page(self, controller, *args):
        frame = controller(self.receptacle, self, *args)
        self.frames[controller] = frame
        frame.grid(row=0, column=0, sticky="nsew")
        self.frames[controller].tkraise()

class First_Page(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.configure(background="#FFFFFF")

        global a_positive_count
        global a_negative_count 
        global b_positive_count 
        global b_negative_count 
        global o_positive_count
        global o_negative_count 
        global ab_positive_count 
        global ab_negative_count
        global subtrahend
        
        a_positive_count = 0 
        a_negative_count = 0
        b_positive_count = 0
        b_negative_count = 0
        o_positive_count = 0
        o_negative_count = 0
        ab_positive_count = 0
        ab_negative_count = 0
        subtrahend = 0

        self.logo = Image.open("heart.png")
        self.resizedLogo = self.logo.resize((450, 150), Image.ANTIALIAS)
        self.newLogo = ImageTk.PhotoImage(self.resizedLogo)

        tk.Label(self, image=self.newLogo, background="#FFFFFF").pack(pady=10)

        style = ttk.Style()
        style.theme_use("clam")
        
        style.configure("TLabelframe", bordercolor="#ed1e23", background="#FFFFFF")
        style.configure("TLabelframe.Label", font=("Tw Cen MT", 12, "bold"), background="#FFFFFF")
        style.configure("my.TButton", font=("Tw Cen MT", 12, "bold"), background="#FFFFFF", bordercolor="#ed1e23")
        style.map("my.TButton", foreground=[("!active", "#000000"), ("pressed", "#FFFFFF"), ("active", "#FFFFFF")], \
                  background=[("!active", "#FFFFFF"), ("pressed", "#ed1e23"), ("active", "#ed1e25")])
        
        frame_for_buttons = tk.Frame(self, background="#FFFFFF")
        frame_for_buttons.pack(side="left")

        donor = ttk.Button(frame_for_buttons, text ="Become a Donor", width=18, command=lambda : self.controller.display_a_page(Page_for_Donor), \
                           style="my.TButton")
        donor.grid(row=0, column=1, padx=80)

        request = ttk.Button(frame_for_buttons, text ="Blood Request", width=18, command=lambda : self.controller.display_a_page(Demand_for_Blood), \
                           style="my.TButton")
        request.grid(row=1, column=1, padx=80, pady=25)

        blood_donated = ttk.Button(frame_for_buttons, text ="Blood Donated", width=18, command=lambda : self.controller.display_a_page(Blood_Donated), \
                           style="my.TButton")
        blood_donated.grid(row=2,  column=1, padx=80)

        view_donors = ttk.Button(frame_for_buttons, text ="View Donors", width=18, command=lambda : self.controller.display_a_page(View_Donors), \
                           style="my.TButton")
        view_donors.grid(row=3, column=1, padx=80, pady=25)

        view_pending_requests = ttk.Button(frame_for_buttons, text="View Pending Requests", command=lambda : self.controller.display_a_page(View_Pending_Requests), \
                                           style="my.TButton")
        view_pending_requests.grid(row=4, column=1, padx=60)

        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()

        cursor.execute("SELECT blood_type FROM Blood")
        blood_type_list = [blood_type[0] for blood_type in cursor.fetchall()]

        connection.commit()
        connection.close()
 
        for blood_type in blood_type_list:
            if blood_type == "A+":
                a_positive_count += 1
            elif blood_type == "A-":
                a_negative_count += 1
            elif blood_type == "B+":
                b_positive_count += 1
            elif blood_type == "B-":
                b_negative_count += 1
            elif blood_type == "O+":
                o_positive_count += 1
            elif blood_type == "O-":
                o_negative_count += 1
            elif blood_type == "AB+":
                ab_positive_count += 1
            elif blood_type == "AB-":
                ab_negative_count += 1

        global counts
        counts = {
            "A+" : a_positive_count,
            "A-" : a_negative_count,
            "B+" : b_positive_count,
            "B-" : b_negative_count,
            "O+" : o_positive_count,
            "O-" : o_negative_count,
            "AB+" : ab_positive_count,
            "AB-" : ab_negative_count
        }
        available = ttk.LabelFrame(self, text="Blood Available", style="TLabelframe")
        available.pack(side="left", padx=20)
 
        blood_type = ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"]
        index = 0
        for column in range(4):
            label_one = tk.Label(available, background="#FFFFFF", font=("Tw Cen MT", 12, "bold"), text=blood_type[index])
            label_one.grid(row=0, column=column, padx=20)

            indicator_one = tk.Label(available, background="#FFFFFF", font=("Tw Cen MT", 12), text="Total Bags: {}".format(counts[blood_type[index]]))
            indicator_one.grid(row=1, column=column, padx=20)

            entry = tk.Entry(available)
            entry.configure(state="disabled", disabledbackground="#FFFFFF", highlightbackground="#FFFFFF", relief="flat")
            entry.grid(row=2, column=column)
            
            label_two = tk.Label(available, background="#FFFFFF", font=("Tw Cen MT", 12, "bold"), text=blood_type[index + 1])
            label_two.grid(row=3, column=column, padx=20)

            indicator_two = tk.Label(available, background="#FFFFFF", font=("Tw Cen MT", 12), text="Total Bags: {}".format(counts[blood_type[index + 1]]))
            indicator_two.grid(row=4, column=column, padx=20)
            
            index += 2

class View_Pending_Requests(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(background="#FFFFFF")
        self.controller = controller
        
        self.logo = Image.open("heart.png")
        self.resizedLogo = self.logo.resize((300, 100), Image.ANTIALIAS)
        self.newLogo = ImageTk.PhotoImage(self.resizedLogo)
        tk.Label(self, image=self.newLogo, background="#FFFFFF").pack(pady=20)

        style = ttk.Style()
        style.theme_use("clam")
        
        style.configure("my.TButton", font=("Tw Cen MT", 12, "bold"), background="#FFFFFF", bordercolor="#ed1e23")
        style.map("my.TButton", foreground=[("!active", "#000000"), ("pressed", "#FFFFFF"), ("active", "#FFFFFF")], \
                  background=[("!active", "#FFFFFF"), ("pressed", "#ed1e23"), ("active", "#ed1e23")])
        
        title = tk.Label(self, text="Hospital Requests", background="#FFFFFF", font=("Tw Cen MT", 25, "bold"))
        title.pack()
        
        self.frame = tk.Frame(self, background="#FFFFFF")
        self.frame.pack(pady=10)

        fields = ["Hospital Name", "Address", "Telephone Number", "Physician", "Blood Type", "Date Requested", "Bags", "Actions"]
        for column in range(len(fields)):
            entry = tk.Entry(self.frame, font=("Tw Cen MT", 10, "bold"), relief="flat", justify="center")
            entry.insert(0, fields[column])
            entry.configure(state="disabled", disabledbackground="#ed1e23", disabledforeground="#FFFFFF")
            entry.grid(row=0, column=column)

        inner = tk.Frame(self.frame, background="#FFFFFF")
        inner.grid(row=7, columnspan=7)

        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()

        cursor.execute("SELECT name, address, telephone_number FROM Hospital")
        self.donors = [[data for data in record] for record in cursor.fetchall()]
        
        cursor.execute("SELECT physician, blood_type, date_requested, bags FROM Requests")
        requests = cursor.fetchall()

        cursor.execute("SELECT id_Number FROM Donor")
        id_numbers = [date[0] for date in cursor.fetchall()]
        
        connection.commit()
        connection.close()

        for index in range(len(self.donors)):
            for element in requests[index]:
                self.donors[index].append(element)

        for row in range(len(self.donors)):
            for column in range(7):
                entry = tk.Entry(self.frame, font=("Tw Cen MT", 10), relief="flat", justify="center")
                entry.insert(0, self.donors[row][column])
                entry.configure(state="disabled", disabledbackground="#f2f2f2", disabledforeground="#000000")
                entry.grid(row=row+8, column=column,  ipady=8)

        self.counter = 0
        for row in range(len(self.donors)):
            self.actions = tk.Frame(self.frame, bg="#FFFFFF", relief="flat")
            self.actions.grid(row=row+8, column=7)
            
            accept_button = tk.Button(self.actions, text="Accept", command=(lambda ID=self.counter: self.accept(ID)), font=("Tw Cen MT", 10, "bold"), foreground="#FFFFFF", activeforeground="#FFFFFF", \
                                     bg="#00cc00", activebackground="#00cc00", relief="flat")
            accept_button.pack(side="left", padx=14, pady=3)
            
            reject_button = tk.Button(self.actions, text="Reject", command=(lambda ID=self.counter: self.reject(ID)), \
                                      font=("Tw Cen MT", 10, "bold"), foreground="#FFFFFF", activeforeground="#FFFFFF", \
                                      bg="#ed1e23", activebackground="#ed1e23", relief="flat")
            reject_button.pack(side="left")
            self.counter += 1

        back = ttk.Button(self, text="Back", command=lambda : self.controller.display_a_page(First_Page), style="my.TButton")
        back.pack(pady=15)

    def accept(self, ID):
        print(self.donors)
        subtrahend = int(self.donors[ID][6])
        counts[self.donors[ID][4]] -= int(self.donors[ID][6])
        print(counts[self.donors[ID][4]])

        total = self.donors[ID][6]
        entry = tk.Entry(self.frame, font=("Tw Cen MT", 10), relief="flat", justify="center")
        entry.insert(0, total)
        entry.configure(state="disabled", disabledbackground="#f2f2f2", disabledforeground="#000000")
        entry.grid(row=ID + 8, column=6,  ipady=8)

        self.actions = tk.Frame(self.frame, bg="#FFFFFF", relief="flat")
        self.actions.grid(row=ID+8, column=7)
        
        accepted = tk.Button(self.actions, width=17, text="Accepted", font=("Tw Cen MT", 10, "bold"), relief="flat")
        accepted.configure(background="#00cc00", foreground="#FFFFFF")
        accepted.pack()
        
    def reject(self, ID):
        self.actions = tk.Frame(self.frame, bg="#FFFFFF", relief="flat")
        self.actions.grid(row=ID+8, column=7)
        
        accepted = tk.Button(self.actions, width=17, text="Rejected", font=("Tw Cen MT", 10, "bold"), relief="flat")
        accepted.configure(background="#ed1e23", foreground="#FFFFFF")
        accepted.pack()
    
class View_Donors(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(background="#FFFFFF")
        self.controller = controller
        
        self.logo = Image.open("heart.png")
        self.resizedLogo = self.logo.resize((300, 100), Image.ANTIALIAS)
        self.newLogo = ImageTk.PhotoImage(self.resizedLogo)
        tk.Label(self, image=self.newLogo, background="#FFFFFF").pack(pady=20)

        style = ttk.Style()
        style.theme_use("clam")
        
        style.configure("my.TButton", font=("Tw Cen MT", 12, "bold"), background="#FFFFFF", bordercolor="#ed1e23")
        style.map("my.TButton", foreground=[("!active", "#000000"), ("pressed", "#FFFFFF"), ("active", "#FFFFFF")], \
                  background=[("!active", "#FFFFFF"), ("pressed", "#ed1e23"), ("active", "#ed1e23")])
        
        title = tk.Label(self, text="Donor Information", background="#FFFFFF", font=("Tw Cen MT", 25, "bold"))
        title.pack()
        
        frame = tk.Frame(self, background="#FFFFFF")
        frame.pack(pady=10)

        fields = ["ID Number", "Full name", "Contact Number", "Address", "Blood Type", "Date Donated", "Actions"]
        for column in range(len(fields)):
            entry = tk.Entry(frame, font=("Tw Cen MT", 10, "bold"), relief="flat", justify="center")
            entry.insert(0, fields[column])
            entry.configure(state="disabled", disabledbackground="#ed1e23", disabledforeground="#FFFFFF")
            entry.grid(row=0, column=column)

        inner = tk.Frame(frame, background="#FFFFFF")
        inner.grid(row=7, columnspan=7)

        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM Donor")
        donors = [[data for data in record] for record in cursor.fetchall()]

        cursor.execute("SELECT blood_type FROM Blood")
        blood_type_list = [blood_type[0] for blood_type in cursor.fetchall()]

        cursor.execute("SELECT date FROM Donates")
        dates = [date[0] for date in cursor.fetchall()]

        cursor.execute("SELECT id_Number FROM Donor")
        id_numbers = [date[0] for date in cursor.fetchall()] 

        connection.commit()
        connection.close()

        for index in range(len(donors)):
            donors[index].append(blood_type_list[index])
            donors[index].append(dates[index])

        for row in range(len(donors)):
            for column in range(6):
                entry = tk.Entry(frame, font=("Tw Cen MT", 10), relief="flat", justify="center")
                entry.insert(0, donors[row][column])
                entry.configure(state="disabled", disabledbackground="#f2f2f2", disabledforeground="#000000")
                entry.grid(row=row+8, column=column,  ipady=8)

        counter = 0
        for row in range(len(donors)):
            actions = tk.Frame(frame, bg="#FFFFFF", relief="flat")
            actions.grid(row=row+8, column=6)
            
            update_button = tk.Button(actions, text="Update", command=(lambda ID=id_numbers[counter]: self.update(ID)), font=("Tw Cen MT", 10, "bold"), foreground="#FFFFFF", activeforeground="#FFFFFF", \
                                     bg="#00cc00", activebackground="#00cc00", relief="flat")
            update_button.pack(side="left", padx=14, pady=3)
            
            delete_button = tk.Button(actions, text="Delete", command=(lambda ID=id_numbers[counter]: self.delete(ID)), \
                                      font=("Tw Cen MT", 10, "bold"), foreground="#FFFFFF", activeforeground="#FFFFFF", \
                                      bg="#ed1e23", activebackground="#ed1e23", relief="flat")
            delete_button.pack(side="left")
            counter += 1

        back = ttk.Button(self, text="Back", command=lambda : self.controller.display_a_page(First_Page), style="my.TButton")
        back.pack(pady=15)
        
    def delete(self, ID):
        response = messagebox.askyesno("Information", "Deleted entries are not retrievable. Do you wish to continue?")
        if response:
            connection = sqlite3.connect("database.db")
            cursor = connection.cursor()
            
            cursor.execute("DELETE FROM Donor WHERE id_number=?", (ID,))
            cursor.execute("DELETE FROM Donates WHERE donor_id=?", (ID,))
            cursor.execute("DELETE FROM Blood WHERE id=?", (ID,))
            
            connection.commit()
            connection.close()

            self.controller.display_a_page(First_Page)

    def update(self, ID):
        global ID_NUMBER
        
        ID_NUMBER = ID
        self.controller.display_a_page(Update)
            
class Page_for_Donor(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(background="#FFFFFF")
        self.controller = controller
        
        self.logo = Image.open("heart.png")
        self.resizedLogo = self.logo.resize((300, 100), Image.ANTIALIAS)
        self.newLogo = ImageTk.PhotoImage(self.resizedLogo)
        tk.Label(self, image=self.newLogo, background="#FFFFFF").pack(pady=20)

        style = ttk.Style()
        style.theme_use("clam")
        
        style.configure("my.TButton", font=("Tw Cen MT", 12, "bold"), background="#FFFFFF", bordercolor="#ed1e23")
        style.map("my.TButton", foreground=[("!active", "#000000"), ("pressed", "#FFFFFF"), ("active", "#FFFFFF")], \
                  background=[("!active", "#FFFFFF"), ("pressed", "#ed1e23"), ("active", "#ed1e25")])
        
        title = tk.Label(self, text="Donor Information", background="#FFFFFF", font=("Tw Cen MT", 25, "bold"))
        title.pack()
        
        frame = tk.Frame(self, background="#FFFFFF")
        frame.pack(pady=10)

        id_number = tk.Label(frame, text="ID Number: ", background="#FFFFFF", font=("Tw Cen MT", 12, "bold"))
        id_number.grid(row=0, column=0, sticky="e")

        global ID_number
        ID_number = tk.Entry(frame, width=20, font=("Tw Cen MT", 10), relief="solid")
        ID_number.grid(row=0, column=1)

        full_name = ttk.Label(frame, text="Name: ", background="#FFFFFF", font=("Tw Cen MT", 12, "bold"))
        full_name.grid(row=1, column=0, pady=10, sticky="e")

        self.full_name = tk.Entry(frame, width=20, font=("Tw Cen MT", 10), relief="solid")
        self.full_name.grid(row=1, column=1, pady=10)

        contact_number = ttk.Label(frame, text="Contact Number: ", background="#FFFFFF", font=("Tw Cen MT", 12, "bold"))
        contact_number.grid(row=2, column=0, sticky="e")

        self.contact_number = tk.Entry(frame, width=20, font=("Tw Cen MT", 10), relief="solid")
        self.contact_number.grid(row=2, column=1)

        address = ttk.Label(frame, text="Address: ", background="#FFFFFF", font=("Tw Cen MT", 12, "bold"))
        address.grid(row=3, column=0, pady=10, sticky="e")

        self.address = tk.Entry(frame, width=20, font=("Tw Cen MT", 10), relief="solid")
        self.address.grid(row=3, column=1, pady=10)

        date = ttk.Label(frame, text="Date: ", background="#FFFFFF", font=("Tw Cen MT", 12, "bold"))
        date.grid(row=4, column=0, sticky="e")

        self.date = tk.Entry(frame, width=20, font=("Tw Cen MT", 10), relief="solid")
        self.date.grid(row=4, column=1)

        frame_for_buttons = tk.Frame(frame, background="#FFFFFF")
        frame_for_buttons.grid(row=5, column=0, columnspan=2)

        submit = ttk.Button(frame_for_buttons, text="Submit", command=self.submit, style="my.TButton")
        submit.pack(pady=15)

        back = ttk.Button(frame_for_buttons, text="Back", command=lambda : self.controller.display_a_page(First_Page), style="my.TButton")
        back.pack()
        
    def submit(self):
        if not (ID_number.get() and self.full_name.get() and self.contact_number.get() and self.address.get() and self.date.get()):
            messagebox.showerror("Error", "All fields are required.")
        else:
            connection = sqlite3.connect("database.db")
            cursor = connection.cursor()

            data = (ID_number.get(), self.full_name.get(), self.contact_number.get(), self.address.get())
            cursor.execute("INSERT INTO Donor VALUES (?, ?, ?, ?)", data)
            
            data = (ID_number.get(), self.date.get())
            cursor.execute("INSERT INTO Donates VALUES (?, ?)", data)
            
            messagebox.showinfo("Information", "Information has been added successfully.")
            
            connection.commit()
            connection.close()

            self.controller.display_a_page(First_Page) 

class Update(tk.Frame):
    def __init__(self, parent, controller, *args):
        tk.Frame.__init__(self, parent)
        self.configure(background="#FFFFFF")
        self.controller = controller
        
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM Donor WHERE id_number=?", (ID_NUMBER,))
        record = cursor.fetchall()[0]

        cursor.execute("SELECT date FROM Donates")
        date_today = cursor.fetchall()
        
        connection.commit()
        connection.close()
        
        self.logo = Image.open("heart.png")
        self.resizedLogo = self.logo.resize((300, 100), Image.ANTIALIAS)
        self.newLogo = ImageTk.PhotoImage(self.resizedLogo)
        tk.Label(self, image=self.newLogo, background="#FFFFFF").pack(pady=20)

        style = ttk.Style()
        style.theme_use("clam")
        
        style.configure("my.TButton", font=("Tw Cen MT", 12, "bold"), background="#FFFFFF", bordercolor="#ed1e23")
        style.map("my.TButton", foreground=[("!active", "#000000"), ("pressed", "#FFFFFF"), ("active", "#FFFFFF")], \
                  background=[("!active", "#FFFFFF"), ("pressed", "#ed1e23"), ("active", "#ed1e25")])
        
        title = tk.Label(self, text="Donor Information", background="#FFFFFF", font=("Tw Cen MT", 25, "bold"))
        title.pack()

        frame = tk.Frame(self, background="#FFFFFF")
        frame.pack(pady=10)

        full_name = ttk.Label(frame, text="Name: ", background="#FFFFFF", font=("Tw Cen MT", 12, "bold"))
        full_name.grid(row=0, column=0, pady=10, sticky="e")

        self.new_full_name = tk.Entry(frame, width=20, font=("Tw Cen MT", 10), foreground="#ed1e23", relief="solid")
        self.new_full_name.insert(0, record[1])
        self.new_full_name.grid(row=0, column=1, pady=10)

        contact_number = ttk.Label(frame, text="Contact Number: ", background="#FFFFFF", font=("Tw Cen MT", 12, "bold"))
        contact_number.grid(row=1, column=0, sticky="e")

        self.new_contact_number = tk.Entry(frame, width=20, font=("Tw Cen MT", 10), foreground="#ed1e23", relief="solid")
        self.new_contact_number.insert(0, record[2])
        self.new_contact_number.grid(row=1, column=1)

        address = ttk.Label(frame, text="Address: ", background="#FFFFFF", font=("Tw Cen MT", 12, "bold"))
        address.grid(row=2, column=0, pady=10, sticky="e")

        self.new_address = tk.Entry(frame, width=20, font=("Tw Cen MT", 10), foreground="#ed1e23", relief="solid")
        self.new_address.insert(0, record[3])
        self.new_address.grid(row=2, column=1, pady=10)

        date = ttk.Label(frame, text="Date: ", background="#FFFFFF", font=("Tw Cen MT", 12, "bold"))
        date.grid(row=3, column=0, sticky="e")

        self.new_date = tk.Entry(frame, width=20, font=("Tw Cen MT", 10), foreground="#ed1e23", relief="solid")
        self.new_date.insert(0, date_today[-1][0])
        self.new_date.grid(row=3, column=1)
        
        frame_for_buttons = tk.Frame(frame, background="#FFFFFF")
        frame_for_buttons.grid(row=5, column=0, columnspan=2)

        Update = ttk.Button(frame_for_buttons, text="Update", command=self.update_two, style="my.TButton")
        Update.pack(pady=15)

    def update_two(self):
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        
        data = (self.new_full_name.get(), self.new_contact_number.get(), self.new_address.get(), ID_NUMBER)
        cursor.execute("UPDATE Donor SET name = ?, contact_number = ?, address = ? WHERE id_number = ?", data)
        cursor.execute("UPDATE Donates SET date = ? WHERE donor_id = ?", (self.new_date.get(), ID_NUMBER))

        connection.commit()
        connection.close()
                       
        messagebox.showinfo("Information", "Record updated.")
        self.controller.display_a_page(First_Page)
                       
class Blood_Donated(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(background="#FFFFFF")
        self.controller = controller

        self.logo = Image.open("heart.png")
        self.resizedLogo = self.logo.resize((300, 100), Image.ANTIALIAS)
        self.newLogo = ImageTk.PhotoImage(self.resizedLogo)
        tk.Label(self, image=self.newLogo, background="#FFFFFF").pack(pady=20)

        style = ttk.Style()
        style.theme_use("clam")
        
        style.configure("my.TButton", font=("Tw Cen MT", 12, "bold"), background="#FFFFFF", bordercolor="#ed1e23")
        style.map("my.TButton", foreground=[("!active", "#000000"), ("pressed", "#FFFFFF"), ("active", "#FFFFFF")], \
                  background=[("!active", "#FFFFFF"), ("pressed", "#ed1e23"), ("active", "#ed1e25")])
        
        title = tk.Label(self, text="Blood Type Information", background="#FFFFFF", font=("Tw Cen MT", 25, "bold"))
        title.pack()

        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        
        cursor.execute("SELECT ID_number FROM Donor")

        records = [id[0] for id in cursor.fetchall()]
        
        connection.commit()
        connection.close()

        blood_type_list = ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"]
        self.choice = tk.StringVar()
        self.blood_type = tk.StringVar()

        self.choice.set(records[0])
        self.blood_type.set(blood_type_list[0])
        
        frame = tk.Frame(self, background="#FFFFFF")
        frame.pack(pady=20)

        donor_id_number = ttk.Label(frame, text="Donor ID Number: ", background="#FFFFFF", font=("Tw Cen MT", 12, "bold"))
        donor_id_number.grid(row=0, column=0, sticky="e", pady=20)
        
        option_menu = ttk.Combobox(frame, values=records, textvariable=self.choice, font=("Tw Cen MT", 12), background="#FFFFFF", state="readonly")
        option_menu.grid(row=0, column=1, columnspan=2, pady=20)
        
        blood_type = ttk.Label(frame, text="Blood Type: ", background="#FFFFFF", font=("Tw Cen MT", 12, "bold"))
        blood_type.grid(row=1, column=0, sticky="e")

        option_menu_two = ttk.Combobox(frame, values=blood_type_list, textvariable=self.blood_type, font=("Tw Cen MT", 12), state="readonly")
        option_menu_two.grid(row=1, column=1, columnspan=2)

        frame_for_buttons = tk.Frame(frame, background="#FFFFFF")
        frame_for_buttons.grid(row=2, column=0, columnspan=3)
        
        add = ttk.Button(frame_for_buttons, text="Add", command=self.add, style="my.TButton")
        add.pack(pady=15)

        back = ttk.Button(frame_for_buttons, text="Back", command=lambda : self.controller.display_a_page(First_Page), style="my.TButton")
        back.pack()

    def add(self):
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()

        data = (self.choice.get(), self.blood_type.get())
        cursor.execute("INSERT INTO Blood VALUES (?, ?)", data)

        messagebox.showinfo("Information", "Information has been added successfully.")
        self.controller.display_a_page(First_Page)
        
        connection.commit()
        connection.close()
            
class Demand_for_Blood(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(background="#FFFFFF")
        self.controller = controller

        self.logo = Image.open("heart.png")
        self.resizedLogo = self.logo.resize((300, 100), Image.ANTIALIAS)
        self.newLogo = ImageTk.PhotoImage(self.resizedLogo)
        tk.Label(self, image=self.newLogo, background="#FFFFFF").pack(pady=20)

        style = ttk.Style()
        style.theme_use("clam")
        
        style.configure("my.TButton", font=("Tw Cen MT", 12, "bold"), background="#FFFFFF", bordercolor="#ed1e23")
        style.map("my.TButton", foreground=[("!active", "#000000"), ("pressed", "#FFFFFF"), ("active", "#FFFFFF")], \
                  background=[("!active", "#FFFFFF"), ("pressed", "#ed1e23"), ("active", "#ed1e25")])
        
        title = tk.Label(self, text="Request Form", background="#FFFFFF", font=("Tw Cen MT", 25, "bold"))
        title.pack()
        
        frame = tk.Frame(self, background="#FFFFFF")
        frame.pack(pady=10)

        hospital_name_abbreviation = ttk.Label(frame, text="Hospital Name Abbreviation: ", background="#FFFFFF", font=("Tw Cen MT", 12, "bold"))
        hospital_name_abbreviation.grid(row=0, column=0, sticky="e")

        global HAB
        HAB = tk.Entry(frame, width=20, font=("Tw Cen MT", 10), relief="solid")
        HAB.grid(row=0, column=1)

        hospital_name = ttk.Label(frame, text="Hospital Name: ", background="#FFFFFF", font=("Tw Cen MT", 12, "bold"))
        hospital_name.grid(row=1, column=0, pady=10, sticky="e")

        self.hospital_name = tk.Entry(frame, width=20, font=("Tw Cen MT", 10), relief="solid")
        self.hospital_name.grid(row=1, column=1, pady=10)

        address = ttk.Label(frame, text="Address: ", background="#FFFFFF", font=("Tw Cen MT", 12, "bold"))
        address.grid(row=2, column=0, sticky="e")

        self.address = tk.Entry(frame, width=20, font=("Tw Cen MT", 10), relief="solid")
        self.address.grid(row=2, column=1)

        telephone_number = ttk.Label(frame, text="Telephone Number: ", background="#FFFFFF", font=("Tw Cen MT", 12, "bold"))
        telephone_number.grid(row=3, column=0, pady=(10, 0), sticky="e")

        self.telephone_number = tk.Entry(frame, width=20, font=("Tw Cen MT", 10), relief="solid")
        self.telephone_number.grid(row=3, column=1, pady=(10, 0))

        frame_for_buttons = tk.Frame(frame, background="#FFFFFF")
        frame_for_buttons.grid(row=4, column=0, columnspan=2)

        request = ttk.Button(frame_for_buttons, text="Request", command=self.request, style="my.TButton")
        request.pack(pady=10)

        retreat = ttk.Button(frame_for_buttons, text="Back", command=lambda : self.controller.display_a_page(First_Page), style="my.TButton")
        retreat.pack()

    def request(self):
        if not (HAB.get() and self.hospital_name.get() and self.address.get() and self.telephone_number.get()):
            messagebox.showerror("Error", "All fields are required.")
    
        else:
            connection = sqlite3.connect("database.db")
            cursor = connection.cursor()

            data = (HAB.get(), self.hospital_name.get(), self.address.get(), self.telephone_number.get())
            cursor.execute("INSERT INTO Hospital VALUES (?, ?, ?, ?)", data)
            messagebox.showinfo("Information", "Please click OK to proceed.")
            
            connection.commit()
            connection.close()

            self.controller.display_a_page(Proceed)

class Proceed(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(background="#FFFFFF")
        self.controller = controller

        self.logo = Image.open("heart.png")
        self.resizedLogo = self.logo.resize((300, 100), Image.ANTIALIAS)
        self.newLogo = ImageTk.PhotoImage(self.resizedLogo)
        tk.Label(self, image=self.newLogo, background="#FFFFFF").pack(pady=20)

        style = ttk.Style()
        style.theme_use("clam")
        
        style.configure("my.TButton", font=("Tw Cen MT", 12, "bold"), background="#FFFFFF", bordercolor="#ed1e23")
        style.map("my.TButton", foreground=[("!active", "#000000"), ("pressed", "#FFFFFF"), ("active", "#FFFFFF")], \
                  background=[("!active", "#FFFFFF"), ("pressed", "#ed1e23"), ("active", "#ed1e25")])
        
        title = tk.Label(self, text="Further Information", background="#FFFFFF", font=("Tw Cen MT", 25, "bold"))
        title.pack()
        
        frame = tk.Frame(self, background="#FFFFFF")
        frame.pack(pady=10)

        blood_type = tk.Label(frame, text="Blood Type: ", background="#FFFFFF", font=("Tw Cen MT", 12, "bold"))
        blood_type.grid(row=0, column=0, sticky="e")

        self.blood_type = tk.Entry(frame, width=20, font=("Tw Cen MT", 10), relief="solid")
        self.blood_type.grid(row=0, column=1)

        bags = ttk.Label(frame, text="Bags: ", background="#FFFFFF", font=("Tw Cen MT", 12, "bold"))
        bags.grid(row=1, column=0, pady=10, sticky="e")

        self.bags = tk.Entry(frame, width=20, font=("Tw Cen MT", 10), relief="solid")
        self.bags.grid(row=1, column=1, pady=10)

        request_date = tk.Label(frame, text="Request Date: ", background="#FFFFFF", font=("Tw Cen MT", 12, "bold"))
        request_date.grid(row=2, column=0, sticky="e")

        self.request_date = tk.Entry(frame, width=20, font=("Tw Cen MT", 10), relief="solid")
        self.request_date.grid(row=2, column=1)

        physician = tk.Label(frame, text="Physician: ", background="#FFFFFF", font=("Tw Cen MT", 12, "bold"))
        physician.grid(row=3, column=0, pady=(10, 0), sticky="e")

        self.physician = tk.Entry(frame, width=20, font=("Tw Cen MT", 10), relief="solid")
        self.physician.grid(row=3, column=1, pady=(10, 0))

        frame_for_buttons = tk.Frame(frame, background="#FFFFFF")
        frame_for_buttons.grid(row=4, column=0, columnspan=2)

        request = ttk.Button(frame_for_buttons, text="Proceed", command=self.request, style="my.TButton")
        request.pack(pady=20)

    def request(self):
        pairs = {
            "A+" : a_positive_count,
            "A-" : a_negative_count,
            "B+" : b_positive_count,
            "B-" : b_negative_count,
            "O+" : o_positive_count,
            "O-" : o_negative_count,
            "AB+" : ab_positive_count,
            "AB-" : ab_negative_count
        }
        difference = pairs[self.blood_type.get()] - int(self.bags.get())
        if not (HAB.get() and self.blood_type.get() and self.bags.get() and self.request_date.get() and self.physician.get()):
            messagebox.showerror("Error", "All fields are required.")
        elif difference < 0:
            messagebox.showerror("Error", "There are only {} bags of {} left.".format(pairs[self.blood_type.get()], self.blood_type.get()))
        else:
            connection = sqlite3.connect("database.db")
            cursor = connection.cursor()

            data = (HAB.get(), self.blood_type.get(), self.bags.get(), self.request_date.get(), self.physician.get())
            cursor.execute("INSERT INTO Requests VALUES (?, ?, ?, ?, ?)", data)
            messagebox.showinfo("Information", "Your request is currently being processed.")
            
            connection.commit()
            connection.close()

            self.controller.display_a_page(First_Page)
        
if __name__ == "__main__":    
    application = Application()
    application.mainloop()
