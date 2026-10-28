import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# Connect to database
conn = sqlite3.connect("students.db")
cursor = conn.cursor()

# Create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    department TEXT NOT NULL,
    age INTEGER NOT NULL
)
""")
conn.commit()


# Insert student record
def add_student():
    name = name_entry.get().strip()
    department = dept_entry.get().strip()
    age = age_entry.get().strip()

    if not name or not department or not age:
        messagebox.showerror("Error", "Please fill all fields")
        return

    try:
        age_value = int(age)
        if age_value <= 0:
            raise ValueError

        cursor.execute(
            "INSERT INTO students (name, department, age) VALUES (?, ?, ?)",
            (name, department, age_value)
        )
        conn.commit()

        messagebox.showinfo("Success", "Student added successfully")
        clear_fields()
        view_students()

    except ValueError:
        messagebox.showerror("Error", "Enter a valid positive age")


# Display student records
def view_students():
    for item in tree.get_children():
        tree.delete(item)

    cursor.execute("SELECT * FROM students ORDER BY id")

    for row in cursor.fetchall():
        tree.insert("", tk.END, values=row)


# Select a student
def select_student(event):
    selected = tree.selection()

    if selected:
        values = tree.item(selected[0], "values")

        clear_fields()
        name_entry.insert(0, values[1])
        dept_entry.insert(0, values[2])
        age_entry.insert(0, values[3])


# Update student record
def update_student():
    selected = tree.selection()

    if not selected:
        messagebox.showerror("Error", "Select a student first")
        return

    name = name_entry.get().strip()
    department = dept_entry.get().strip()
    age = age_entry.get().strip()

    if not name or not department or not age:
        messagebox.showerror("Error", "Please fill all fields")
        return

    try:
        age_value = int(age)
        if age_value <= 0:
            raise ValueError

        student_id = tree.item(selected[0], "values")[0]

        cursor.execute(
            """UPDATE students
               SET name=?, department=?, age=?
               WHERE id=?""",
            (name, department, age_value, student_id)
        )
        conn.commit()

        messagebox.showinfo("Success", "Student updated successfully")
        clear_fields()
        view_students()

    except ValueError:
        messagebox.showerror("Error", "Enter a valid positive age")


# Delete student record
def delete_student():
    selected = tree.selection()

    if not selected:
        messagebox.showerror("Error", "Select a student first")
        return

    student_id = tree.item(selected[0], "values")[0]

    if messagebox.askyesno("Confirm", "Delete this student?"):
        cursor.execute("DELETE FROM students WHERE id=?", (student_id,))
        conn.commit()

        messagebox.showinfo("Success", "Student deleted successfully")
        clear_fields()
        view_students()


# Clear input fields
def clear_fields():
    name_entry.delete(0, tk.END)
    dept_entry.delete(0, tk.END)
    age_entry.delete(0, tk.END)


# Create GUI window
root = tk.Tk()
root.title("Student Database Management System")
root.geometry("750x500")

title = tk.Label(
    root,
    text="STUDENT DATABASE MANAGEMENT",
    font=("Arial", 18, "bold")
)
title.pack(pady=10)

# Input form
form = tk.Frame(root)
form.pack(pady=10)

tk.Label(form, text="Name:").grid(row=0, column=0, padx=5, pady=5)
name_entry = tk.Entry(form, width=25)
name_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(form, text="Department:").grid(row=1, column=0, padx=5, pady=5)
dept_entry = tk.Entry(form, width=25)
dept_entry.grid(row=1, column=1, padx=5, pady=5)

tk.Label(form, text="Age:").grid(row=2, column=0, padx=5, pady=5)
age_entry = tk.Entry(form, width=25)
age_entry.grid(row=2, column=1, padx=5, pady=5)

# Buttons
buttons = tk.Frame(root)
buttons.pack(pady=10)

tk.Button(buttons, text="Add Student", width=14,
          command=add_student).grid(row=0, column=0, padx=5)

tk.Button(buttons, text="View Students", width=14,
          command=view_students).grid(row=0, column=1, padx=5)

tk.Button(buttons, text="Update Student", width=14,
          command=update_student).grid(row=0, column=2, padx=5)

tk.Button(buttons, text="Delete Student", width=14,
          command=delete_student).grid(row=0, column=3, padx=5)

tk.Button(buttons, text="Clear Fields", width=14,
          command=clear_fields).grid(row=0, column=4, padx=5)

# Table to display records
columns = ("ID", "Name", "Department", "Age")

tree = ttk.Treeview(root, columns=columns, show="headings")

for column in columns:
    tree.heading(column, text=column)
    tree.column(column, width=150)

tree.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
tree.bind("<<TreeviewSelect>>", select_student)

# Display existing records
view_students()

# Start GUI
root.mainloop()

# Close database connection when the application exits
conn.close()