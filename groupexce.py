import customtkinter as ctk
from tkinter import filedialog, messagebox
import random as rd
import pandas as pd

# Set appearance mode and color theme
ctk.set_appearance_mode("Dark")  # Options: "Light", "Dark", "System"
ctk.set_default_color_theme("blue")

class ModernGroupingApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("ClassGroup Pro - Lecturer Edition")
        self.geometry("1100x600")
        self.students = []

        # --- Grid Layout (1x2) ---
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- SIDEBAR ---
        self.sidebar_frame = ctk.CTkFrame(self, width=300, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        
        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="ClassGroup Pro", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        # Inputs in Sidebar
        self.course_label = ctk.CTkLabel(self.sidebar_frame, text="Course Unit Name:")
        self.course_label.grid(row=1, column=0, padx=20, pady=(10, 0), sticky="w")
        self.course_entry = ctk.CTkEntry(self.sidebar_frame, placeholder_text="e.g. Data Science 101", width=250)
        self.course_entry.grid(row=2, column=0, padx=20, pady=(0, 10))

        self.size_label = ctk.CTkLabel(self.sidebar_frame, text="Students per Group:")
        self.size_label.grid(row=3, column=0, padx=20, pady=(10, 0), sticky="w")
        self.size_entry = ctk.CTkEntry(self.sidebar_frame, width=250)
        self.size_entry.insert(0, "3")
        self.size_entry.grid(row=4, column=0, padx=20, pady=(0, 20))

        # Buttons
        self.upload_btn = ctk.CTkButton(self.sidebar_frame, text="📂 Upload Excel", command=self.upload_excel, fg_color="#3d3d3d", hover_color="#575757")
        self.upload_btn.grid(row=5, column=0, padx=20, pady=10)

        self.generate_btn = ctk.CTkButton(self.sidebar_frame, text="🚀 Generate Groups", command=self.generate, font=ctk.CTkFont(weight="bold"))
        self.generate_btn.grid(row=6, column=0, padx=20, pady=10)

        self.clear_btn = ctk.CTkButton(self.sidebar_frame, text="Reset List", command=self.reset_app, fg_color="transparent", border_width=1)
        self.clear_btn.grid(row=7, column=0, padx=20, pady=(50, 10))

        # --- MAIN CONTENT AREA ---
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)

        # Manual Entry Bar
        self.entry_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.entry_frame.grid(row=0, column=0, pady=(0, 20), sticky="ew")
        
        self.name_entry = ctk.CTkEntry(self.entry_frame, placeholder_text="Enter student name manually...", width=400)
        self.name_entry.pack(side="left", padx=(0, 10))
        self.add_btn = ctk.CTkButton(self.entry_frame, text="Add Student", width=100, command=self.add_student)
        self.add_btn.pack(side="left")

        # Results Display
        self.result_box = ctk.CTkTextbox(self.main_frame, font=("Consolas", 14))
        self.result_box.grid(row=1, column=0, sticky="nsew")

        # Status Bar
        self.status_label = ctk.CTkLabel(self.main_frame, text="Ready: 0 students loaded", font=ctk.CTkFont(size=12))
        self.status_label.grid(row=2, column=0, pady=(10, 0), sticky="w")

    # Logic Methods
    def add_student(self):
        name = self.name_entry.get().strip()
        if name:
            self.students.append(name)
            self.name_entry.delete(0, 'end')
            self.update_status()
        
    def upload_excel(self):
        file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls")])
        if file_path:
            try:
                df = pd.read_excel(file_path)
                names = df.iloc[:, 0].dropna().astype(str).tolist()
                self.students.extend(names)
                self.update_status()
                messagebox.showinfo("Success", f"Imported {len(names)} students.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to read file: {e}")

    def update_status(self):
        self.status_label.configure(text=f"Total Students: {len(self.students)}")

    def reset_app(self):
        self.students = []
        self.result_box.delete("1.0", "end")
        self.update_status()

    def generate(self):
        course = self.course_entry.get().strip()
        try:
            size = int(self.size_entry.get())
        except:
            messagebox.showwarning("Input Error", "Check your group size number.")
            return

        if not self.students:
            messagebox.showwarning("No Students", "Please add students first.")
            return

        shuffled = self.students.copy()
        rd.shuffle(shuffled)
        
        # UI Feedback: Clear and Display
        self.result_box.delete("1.0", "end")
        header = f"{'='*40}\nCOURSE: {course.upper()}\n{'='*40}\n\n"
        self.result_box.insert("end", header)

        for i in range(0, len(shuffled), size):
            group = shuffled[i:i + size]
            group_text = f"🔹 GROUP {(i//size)+1}\n" + "\n".join(f"  • {s}" for s in group) + "\n\n"
            self.result_box.insert("end", group_text)

if __name__ == "__main__":
    app = ModernGroupingApp()
    app.mainloop()