import customtkinter as ctk
from tkinter import filedialog, messagebox
import random as rd
import pandas as pd
import datetime 

# --- Appearance Setup ---
ctk.set_appearance_mode("System")  
ctk.set_default_color_theme("blue")

class ModernGroupingApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Basic Window Setup
        self.title("ClassGroup Pro - Lecturer Edition")
        self.geometry("1100x650")
        self.students = []

        # --- Main Grid Layout (1x2) ---
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # ==============================
        # === SIDEBAR (Left Panel) ===
        # ==============================
        self.sidebar_frame = ctk.CTkFrame(self, width=300, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(8, weight=1)
        
        # Logo / Title
        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="ClassGroup Pro", font=ctk.CTkFont(size=22, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(30, 20))

        # --- Inputs ---
        self.course_label = ctk.CTkLabel(self.sidebar_frame, text="Course Unit Name:", anchor="w")
        self.course_label.grid(row=1, column=0, padx=25, pady=(10, 0), sticky="ew")
        self.course_entry = ctk.CTkEntry(self.sidebar_frame, placeholder_text="e.g. Advanced Database Systems")
        self.course_entry.grid(row=2, column=0, padx=20, pady=(5, 15), sticky="ew")

        self.size_label = ctk.CTkLabel(self.sidebar_frame, text="Students per Group:", anchor="w")
        self.size_label.grid(row=3, column=0, padx=25, pady=(10, 0), sticky="ew")
        self.size_entry = ctk.CTkEntry(self.sidebar_frame)
        self.size_entry.insert(0, "4")
        self.size_entry.grid(row=4, column=0, padx=20, pady=(5, 25), sticky="ew")

        # --- Action Buttons ---
        #upload button
        self.upload_btn = ctk.CTkButton(self.sidebar_frame, text="📂 Upload Excel List", command=self.upload_excel, fg_color="#3d3d3d", hover_color="#575757", height=40)
        self.upload_btn.grid(row=5, column=0, padx=20, pady=10, sticky="ew")

        #Generate group button
        self.generate_btn = ctk.CTkButton(self.sidebar_frame, text="⚡ Generate Groups", command=self.generate, font=ctk.CTkFont(weight="bold"), height=45)
        self.generate_btn.grid(row=6, column=0, padx=20, pady=(10, 20), sticky="ew")
        
        # Download button (Initially Disabled)
        self.download_btn = ctk.CTkButton(self.sidebar_frame, text="💾 Download Results", command=self.download_results, state="disabled", fg_color="#2d8a4e", hover_color="#246e3e", height=40)
        self.download_btn.grid(row=7, column=0, padx=20, pady=(0, 20), sticky="ew")

        # Reset button
        self.clear_btn = ctk.CTkButton(self.sidebar_frame, text="Reset Application", command=self.reset_app, fg_color="transparent", border_width=1, text_color=("#555555", "#aaaaaa"))
        self.clear_btn.grid(row=9, column=0, padx=20, pady=20, sticky="ew")

        #apearence
        self.appearance_mode_label = ctk.CTkLabel(self.sidebar_frame, text="Appearance:", anchor="w")
        self.appearance_mode_label.grid(row=9, column=0, padx=25, pady=(100, 0), sticky="ew")
        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(self.sidebar_frame, 
                                                            values=["Dark", "Light", "System"],
                                                            command=self.change_appearance_mode)
        self.appearance_mode_optionemenu.grid(row=10, column=0, padx=20, pady=(5, 20), sticky="ew")


        # ===================================
        # === MAIN AREA (Right Panel) ===
        # ===================================
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.grid(row=0, column=1, padx=30, pady=30, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)

        #Manual Entry
        self.entry_frame = ctk.CTkFrame(self.main_frame)
        self.entry_frame.grid(row=0, column=0, pady=(0, 20), sticky="ew")
        
        self.name_entry = ctk.CTkEntry(self.entry_frame, placeholder_text="Type student name to add manually...", height=40, font=ctk.CTkFont(size=14))
        self.name_entry.pack(side="left", padx=10, pady=10, expand=True, fill="x")
        
        self.add_btn = ctk.CTkButton(self.entry_frame, text="Add Name", width=120, height=40, command=self.add_student)
        self.add_btn.pack(side="right", padx=10, pady=10)
        self.name_entry.bind("<Return>", lambda event: self.add_student()) # Enable 'Enter' key to add

        # 2. Results Area (Textbox)
        # Using Consolas font ensures alignment, corner_radius=10 makes it look modern
        self.result_box = ctk.CTkTextbox(self.main_frame, font=("Consolas", 15), corner_radius=10)
        self.result_box.grid(row=1, column=0, sticky="nsew")
        self.result_box.insert("1.0", "\n  Ready to generate groups.\n  Add students or upload an Excel file to begin.\n please Make sure you download your group list this is a beta version no database attached to it thank you 😉")
        self.result_box.configure(state="disabled") # Make read-only initially

        # 3. Status Bar
        self.status_label = ctk.CTkLabel(self.main_frame, text="Status: 0 students loaded", font=ctk.CTkFont(size=12), anchor="w", text_color="gray")
        self.status_label.grid(row=2, column=0, pady=(10, 0), sticky="ew")


    # =========================
    # === LOGIC METHODS ===
    # =========================
    
    def update_status(self):
        count = len(self.students)
        self.status_label.configure(text=f"Status: {count} students ready for grouping.")
        # Change color slightly if students are loaded
        color = "gray" if count == 0 else ctk.ThemeManager.theme["CTkLabel"]["text_color"]
        self.status_label.configure(text_color=color)

    def change_appearance_mode(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)

    def add_student(self):
        name = self.name_entry.get().strip()
        if name:
            self.students.append(name)
            self.name_entry.delete(0, 'end')
            self.update_status()
            # Temporarily enable textbox to show added message
            self.result_box.configure(state="normal")
            self.result_box.insert("end", f"\n  [+] Added: {name}")
            self.result_box.see("end") # Scroll to bottom
            self.result_box.configure(state="disabled")

        
    def upload_excel(self):
        file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls")])
        if file_path:
            try:
                df = pd.read_excel(file_path)
                #Assumes names are in the first column
                names = df.iloc[:, 0].dropna().astype(str).tolist()
                
                # Clean up names (remove extra spaces)
                clean_names = [n.strip() for n in names if n.strip()]
                
                self.students.extend(clean_names)
                self.update_status()
                messagebox.showinfo("Upload Successful", f"Successfully imported {len(clean_names)} students.")
            except Exception as e:
                messagebox.showerror("Import Error", f"Could not read the Excel file.\nError: {e}")

    def reset_app(self):
        confirm = messagebox.askyesno("Reset", "Are you sure you want to clear all data?")
        if confirm:
            self.students = []
            self.result_box.configure(state="normal")
            self.result_box.delete("1.0", "end")
            self.result_box.insert("1.0", "\n  Application reset successfully.")
            self.result_box.configure(state="disabled")
            self.update_status()
            # Disable download button on reset
            self.download_btn.configure(state="disabled")

    def generate(self):
        # Input Validation
        course = self.course_entry.get().strip()
        if not course: course = "General Course"

        try:
            size = int(self.size_entry.get())
            if size < 1: raise ValueError
        except ValueError:
            messagebox.showwarning("Input Error", "Please enter a valid positive number for group size.")
            return

        if not self.students:
            messagebox.showwarning("Wait", "No students found. Please add students or upload an Excel list first.")
            return

        # The core logic: Shuffle and Slice
        shuffled_list = self.students.copy()
        rd.shuffle(shuffled_list)
        
        # Prepare Output text
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        final_output = f"{'='*50}\nCOURSE UNIT: {course.upper()}\nGENERATED ON: {timestamp}\nTOTAL STUDENTS: {len(shuffled_list)} | TARGET SIZE: {size}\n{'='*50}\n\n"

        group_count = 0
        for i in range(0, len(shuffled_list), size):
            group_count += 1
            group = shuffled_list[i : i + size]
            
            # Determine header based on group size
            if len(group) == size:
                 header = f" GROUP {group_count}"
            else:
                 header = f" REMAINING STUDENTS (Group {group_count})"

            final_output += f"{header}\n"
            final_output += "\n".join(f"   • {student}" for student in group) + "\n\n"
            
        # Update UI text box
        self.result_box.configure(state="normal")
        self.result_box.delete("1.0", "end")
        self.result_box.insert("1.0", final_output)
        self.result_box.configure(state="disabled") # Set back to read-only

        # UX Improvement: Enable download button now that results exist
        self.download_btn.configure(state="normal")
        messagebox.showinfo("Done", f"Successfully created {group_count} groups.")


    # --- DOWNLOAD FUNCTION ---
    def download_results(self):
        # Get current date for default filename
        date_str = datetime.date.today().strftime("%Y-%m-%d")
        course_name = self.course_entry.get().strip().replace(" ", "_")
        if not course_name: course_name = "Groups"
        
        default_name = f"{course_name}_{date_str}_Groups"

        # Open standard "Save As" dialog
        file = filedialog.asksaveasfile(
            mode='w',
            defaultextension=".txt",
            initialfile=default_name,
            filetypes=[("Text File", "*.txt"), ("All Files", "*.*")],
            title="Save Groups As...",
            
        )

        if file:
             # Get text from the result box (from start "1.0" to the end "end-1c" to avoid extra newline)
            content_to_save = self.result_box.get("1.0", "end-1c")
            try:
                file.write(content_to_save)
                file.close()
                messagebox.showinfo("Saved", f"File saved successfully successfully!")
            except Exception as e:
                 messagebox.showerror("Error", f"Could not save file:\n{e}")


if __name__ == "__main__":
    # Added a slightly better scaling for high-DPI displays (like Macs or newer Windows laptops)
    ctk.set_widget_scaling(1.1) 
    app = ModernGroupingApp()
    app.mainloop()