import tkinter as tk
from tkinter import messagebox, filedialog
import random as rd
import pandas as pd

class GroupGenerator:
    """Handles the logic for shuffling and grouping students."""
    def __init__(self, course_name):
        self.course_name = course_name.upper()

    def create_groups(self, student_list, group_size):
        if not student_list:
            return "No students found in the list."
        
        if group_size <= 0:
            return "Group size must be a positive number."

        # Create a copy and shuffle to ensure randomness
        shuffled_list = student_list.copy()
        rd.shuffle(shuffled_list)

        result = f"--- {self.course_name} GROUPS ---\n"
        
        # Slice the list into groups of the specified size
        for i in range(0, len(shuffled_list), group_size):
            group = shuffled_list[i : i + group_size]
            group_num = (i // group_size) + 1
            
            if len(group) == group_size:
                result += f"\nGroup {group_num}:\n" + "\n".join(f"- {s}" for s in group) + "\n"
            else:
                result += f"\nRemaining Students (Incomplete Group):\n" + "\n".join(f"- {s}" for s in group) + "\n"
        
        return result

class GroupingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Lecturer's Grouping Tool")
        self.root.geometry("500x650")
        
        self.students = []

        # --- Course Unit Input ---
        tk.Label(root, text="Course Unit Name:", font=('Arial', 10, 'bold')).pack(pady=(10, 0))
        self.course_entry = tk.Entry(root, width=40)
        self.course_entry.insert(0, "e.g., Data Structures")
        self.course_entry.pack(pady=5)

        # --- Group Size Input ---
        tk.Label(root, text="Number of Students per Group:", font=('Arial', 10, 'bold')).pack(pady=(10, 0))
        self.size_entry = tk.Entry(root, width=10)
        self.size_entry.insert(0, "3")
        self.size_entry.pack(pady=5)

        # --- Student Input Section ---
        tk.Frame(root, height=2, bd=1, relief=tk.SUNKEN).pack(fill=tk.X, padx=20, pady=15)
        
        tk.Label(root, text="Add Student Manually:").pack()
        self.name_entry = tk.Entry(root, width=40)
        self.name_entry.pack(pady=5)

        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=5)
        tk.Button(btn_frame, text="Add Individual", command=self.add_student).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Upload Excel List", command=self.upload_excel, bg="#D1E8FF").grid(row=0, column=1, padx=5)

        # --- Action Button ---
        tk.Button(root, text="GENERATE GROUPS", command=self.generate, 
                  bg="#28a745", fg="white", font=('Arial', 11, 'bold'), height=2, width=20).pack(pady=20)

        # --- Results Output ---
        self.result_box = tk.Text(root, height=15, width=55)
        self.result_box.pack(padx=20, pady=10)

    def add_student(self):
        name = self.name_entry.get().strip()
        if name:
            self.students.append(name)
            self.name_entry.delete(0, tk.END)
            self.update_count()
        else:
            messagebox.showwarning("Warning", "Please enter a student name.")

    def upload_excel(self):
        file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls")])
        if file_path:
            try:
                df = pd.read_excel(file_path)
                # Reads the very first column for names
                names = df.iloc[:, 0].dropna().astype(str).tolist()
                self.students.extend(names)
                self.update_count()
                messagebox.showinfo("Success", f"Imported {len(names)} students successfully.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to read file: {e}")

    def update_count(self):
        # Optional: update UI to show how many students are loaded
        count = len(self.students)
        self.root.title(f"Grouping Tool - {count} Students Loaded")

    def generate(self):
        course = self.course_entry.get().strip()
        try:
            size = int(self.size_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number for group size.")
            return

        if not course or course == "e.g., Data Structures":
            messagebox.showwarning("Warning", "Please enter a Course Unit name.")
            return

        grouper = GroupGenerator(course)
        final_text = grouper.create_groups(self.students, size)
        
        self.result_box.delete(1.0, tk.END)
        self.result_box.insert(tk.END, final_text)

if __name__ == "__main__":
    root = tk.Tk()
    app = GroupingApp(root)
    root.mainloop()