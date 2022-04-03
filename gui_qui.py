from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from db import Database
import myfunction
import os, psutil

mydb = Database("quality.db")
root = Tk()
root.
root.title("Automated Questionnaire")
root.geometry("1920x1080+0+0")
root.config(bg="WHITE")
root.state("iconic")

emr = IntVar()
age_group = StringVar()
gender = StringVar()
ward = StringVar()
cubicle = IntVar()

# Entries Frame
entries_frame = Frame(root, bg="WHITE")
entries_frame.pack(side=TOP, fill=X)
title = Label(entries_frame, text="Automated Questionnaire", font=("Calibri", 18, "bold"), bg="white", fg="blue")
title.grid(row=0, columnspan=2, padx=10, pady=20, sticky="w")

lblEMR = Label(entries_frame, text="EMR NO", font=("Calibri", 16), bg="white", fg="blue")
lblEMR.grid(row=1, column=0, padx=10, pady=10, sticky="w")
txtEMR = Entry(entries_frame, textvariable=emr, font=("Calibri", 16), width=29)
txtEMR.grid(row=1, column=1, padx=10, pady=10, sticky="w")

lblAge = Label(entries_frame, text="Age Group", font=("Calibri", 16), bg="white", fg="blue")
lblAge.grid(row=1, column=2, padx=10, pady=10, sticky="w")
comboage = ttk.Combobox(entries_frame, font=("Calibri", 16), width=28,
                        textvariable= age_group, state="readonly")
comboage['values'] = ("0-35yrs", "36-49yrs", "50yrs and above")
comboage.grid(row=1, column=3, padx=10, sticky="w")

lblward = Label(entries_frame, text="Ward", font=("Calibri", 16), bg="white", fg="blue")
lblward.grid(row=2, column=0, padx=10, pady=10, sticky="w")
comboward = ttk.Combobox(entries_frame, font=("Calibri", 16), width=28,
                         textvariable= ward, state="readonly")
comboward['values'] = ("VIP", "General", "Blue", "Grey", "Silver", "Maternity", "Pediatric")
comboward.grid(row=2, column=1, padx=10, sticky="w")

lblGender = Label(entries_frame, text="Gender", font=("Calibri", 16), bg="white", fg="blue")
lblGender.grid(row=2, column=2, padx=10, pady=10, sticky="w")
comboGender = ttk.Combobox(entries_frame, font=("Calibri", 16), width=28,
                           textvariable=gender, state="readonly")
comboGender['values'] = ("Male", "Female")
comboGender.grid(row=2, column=3, padx=10, sticky="w")

lblCubicle = Label(entries_frame, text="Cubicle No", font=("Calibri", 16), bg="white", fg="blue")
lblCubicle.grid(row=3, column=0, padx=10, pady=10, sticky="w")
txtCubicle = Entry(entries_frame, textvariable=cubicle, font=("Calibri", 16), width=29)
txtCubicle.grid(row=3, column=1, padx=10, sticky="w")


def getData(event):
    selected_row = tv.focus()
    data = tv.item(selected_row)
    global row
    row = data["values"]
    #print(row)
    emr.set(row[1])
    age_group.set(row[2])
    ward.set(row[3])
    gender.set(row[4])
    cubicle.set(row[5])

def dispalyAll():
    tv.delete(*tv.get_children())
    for row in mydb.fetch():
        tv.insert("", END, values=row)

def add_record():
    if txtEMR.get() == "" or comboage.get() == "" or comboward.get() == "" or \
            comboGender.get() == "" or txtCubicle.get() == "":
        messagebox.showerror("Error in Input", "Please Fill All the Details")
        return
    mydb.insert(txtEMR.get(), comboage.get(), comboward.get(),comboGender.get(), txtCubicle.get())
    messagebox.showinfo("Success", "Record Inserted")
    clearAll()
    dispalyAll()

def update_record():
    if txtEMR.get() == "" or comboage.get() == "" or comboward.get() == "" or comboGender.get() == "" or \
            txtCubicle.get() == "":
        messagebox.showerror("Error in Input", "Please Fill All the Details")
        return
    mydb.update(row[0], txtEMR.get(), comboage.get(), comboward.get(), comboGender.get(), txtCubicle.get())
    messagebox.showinfo("Success", "Record Update")
    clearAll()
    dispalyAll()


def delete_record():
    mydb.remove(row[0])
    clearAll()
    dispalyAll()


def clearAll():
    emr.set("")
    age_group.set("")
    gender.set("")
    ward.set("")
    cubicle.set("")

def pdf_print():
    if txtEMR.get() == "" or comboage.get() == "" or comboward.get() == "" or comboGender.get() == "" or \
            txtCubicle.get() == "":
        messagebox.showerror("Error in Input", "Please Fill All the Details")
        return

    a = mydb.fetch([0])
    dcode = myfunction.day + a.ward + a.cubicle
    c1 = myfunction.custom_question(dcode)
    c = os.startfile(c1, "print")
    for p in psutil.process_iter(): #Close Acrobat after printing the PDF
        if 'AcroRd' in str(p):
            p.kill()
        messagebox.showinfo("Success", "Record Update")
    return(c)

btn_frame = Frame(entries_frame, bg="light blue")
btn_frame.grid(row=6, column=0, columnspan=4, padx=10, pady=10, sticky="w")
btnAdd = Button(btn_frame, command=add_record, text="Add Details", width=15, font=("Calibri", 16, "bold"), fg="blue",
                bg="white", bd=0).grid(row=0, column=0)
btnEdit = Button(btn_frame, command=update_record, text="Update Details", width=15, font=("Calibri", 16, "bold"),
                 fg="blue", bg="white",
                 bd=0).grid(row=0, column=1, padx=10)
btnDelete = Button(btn_frame, command=delete_record, text="Delete Details", width=15, font=("Calibri", 16, "bold"),
                   fg="blue", bg="white",
                   bd=0).grid(row=0, column=2, padx=10)
btnClear = Button(btn_frame, command=clearAll, text="Clear Details", width=15, font=("Calibri", 16, "bold"), fg="blue",
                  bg="white",
                  bd=0).grid(row=0, column=3, padx=10)

btnPrint = Button(btn_frame, command= lambda: pdf_print, text="Print", width=15, font=("Calibri", 16, "bold"), fg="blue",
                  bg="white",
                  bd=0).grid(row=0, column=4, padx=10)

# Table Frame
tree_frame = Frame(root, bg="white")
tree_frame.place(x=0, y=320, width=1360, height=1320)
style = ttk.Style()
style.configure("mystyle.Treeview", font=('Calibri', 18),
                rowheight=50)  # Modify the font of the body
style.configure("mystyle.Treeview.Heading", font=('Calibri', 18))  # Modify the font of the headings
tv = ttk.Treeview(tree_frame, columns=(1, 2, 3, 4, 5, 6), style="mystyle.Treeview")
tv.heading("1", text="ID")
tv.column("1", width=2)
tv.heading("2", text="EMR")
tv.heading("3", text="Age Group")
tv.column("3", width=2)
tv.heading("4", text="Ward")
tv.column("4", width=2)
tv.heading("5", text="Gender")
tv.column("5", width=2)
tv.heading("6", text="Cubicle")
tv.column("6", width=2)
tv['show'] = 'headings'
tv.bind("<ButtonRelease-1>", getData)
tv.pack(fill=X)

dispalyAll()
root.mainloop()