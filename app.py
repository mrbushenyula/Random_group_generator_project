import tkinter as tk
from tkinter import messagebox
import random as rd

class LecturerTask:
    def __init__(self, name):
        self.name = name

    def ClassGroups(self, MainList):
        pass

class RandomGroupsIT(LecturerTask):
    def __init__(self, name):
        super().__init__(name)

    def ClassGroups(self, MainList):
        thelist = MainList.copy()
        GroupList = []

        if len(thelist) == 0:
            return "There is no student registered yet"
        elif 1 <= len(thelist) <= 2:
            return "\n".join(thelist)
        else:
            result = "INFORMATION TECHNOLOGY groups\n"
            group = []

            while len(thelist) >= 3:
                for i in range(3):
                    element = rd.choice(thelist)
                    group.append(element)
                    thelist.remove(element)
                GroupList.append(group)
                result += "\nGroup:\n" + "\n".join(group) + "\n"
                group = []

            if len(thelist) > 0:
                result += "\nRemaining students:\n" + "\n".join(thelist)
            return result

class RandomGroupsCS(RandomGroupsIT):
    def ClassGroups(self, MainList):
        result = super().ClassGroups(MainList)
        return result.replace("INFORMATION TECHNOLOGY", "COMPUTER SCIENCE")

class RandomGroupsDS(RandomGroupsIT):
    def ClassGroups(self, MainList):
        result = super().ClassGroups(MainList)
        return result.replace("INFORMATION TECHNOLOGY", "DATA SCIENCE")

# Tkinter-based UI
class GroupingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Grouping")
        self.root.geometry("400x300")

        # Class selection dropdown
        self.class_label = tk.Label(root, text="Select Class:")
        self.class_label.pack()

        self.class_choice = tk.StringVar()
        self.class_dropdown = tk.OptionMenu(root, self.class_choice, "IT", "CS", "DS")
        self.class_dropdown.pack()

        # Entry for student name
        self.name_label = tk.Label(root, text="Student Name:")
        self.name_label.pack()

        self.name_entry = tk.Entry(root)
        self.name_entry.pack()

        # Add student button
        self.add_button = tk.Button(root, text="Add Student", command=self.add_student)
        self.add_button.pack()

        # Group students button
        self.group_button = tk.Button(root, text="Group Students", command=self.group_students)
        self.group_button.pack()

        # Textbox for showing results
        self.result_box = tk.Text(root, height=10, width=40)
        self.result_box.pack()

        self.students = []

    def add_student(self):
        student_name = self.name_entry.get()
        if student_name:
            self.students.append(student_name)
            self.name_entry.delete(0, tk.END)
            messagebox.showinfo("Student Added", f"{student_name} added to the list!")

    def group_students(self):
        class_selected = self.class_choice.get()
        if not class_selected:
            messagebox.showwarning("No Class", "Please select a class.")
            return

        if class_selected == "IT":
            GroupObject = RandomGroupsIT(None)
        elif class_selected == "CS":
            GroupObject = RandomGroupsCS(None)
        elif class_selected == "DS":
            GroupObject = RandomGroupsDS(None)

        result = GroupObject.ClassGroups(self.students)
        self.result_box.delete(1.0, tk.END)
        self.result_box.insert(tk.END, result)


if __name__ == "__main__":
    root = tk.Tk()
    app = GroupingApp(root)
    root.mainloop()
