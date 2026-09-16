import json
import os
import tkinter as tk
from tkinter import messagebox

DATA_FILE = "tasks.json"


class TodoApp:

  def __init__(self, root):
    self.root = root
    self.root.title("Tkinter To-Do List")
    self.root.geometry("400x450")

    # Title Label
    self.title_label = tk.Label(
        root, text="My Tasks", font=("Arial", 16, "bold")
    )
    self.title_label.pack(pady=10)

    # Input Frame
    self.input_frame = tk.Frame(root)
    self.input_frame.pack(pady=5)

    self.task_entry = tk.Entry(self.input_frame, width=25, font=("Arial", 12))
    self.task_entry.pack(side=tk.LEFT, padx=5)
    self.task_entry.bind("<Return>", lambda event: self.add_task())

    self.add_button = tk.Button(
        self.input_frame,
        text="Add your task",
        command=self.add_task,
        bg="#033280",
        fg="white",
    )
    self.add_button.pack(side=tk.LEFT)

    # Task Listbox + Scrollbar
    self.list_frame = tk.Frame(root)
    self.list_frame.pack(pady=10)

    self.scrollbar = tk.Scrollbar(self.list_frame)
    self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    self.task_listbox = tk.Listbox(
        self.list_frame,
        width=35,
        height=12,
        font=("Arial", 11),
        yscrollcommand=self.scrollbar.set,
        selectmode=tk.SINGLE,
    )
    self.task_listbox.pack(side=tk.LEFT)
    self.scrollbar.config(command=self.task_listbox.yview)

    # Delete Button
    self.delete_button = tk.Button(
        root,
        text="Delete Selected",
        command=self.delete_task,
        bg="#b4bfd1",
        fg="white",
    )
    self.delete_button.pack(pady=5)

    # Load tasks on startup
    self.load_tasks()

  def add_task(self):
    task = self.task_entry.get().strip()
    if task:
      self.task_listbox.insert(tk.END, task)
      self.task_entry.delete(0, tk.END)
      self.save_tasks()
    else:
      messagebox.showwarning("oops!", "it cannot be empty")

  def delete_task(self):
    try:
      selected_index = self.task_listbox.curselection()[0]
      self.task_listbox.delete(selected_index)
      self.save_tasks()
    except IndexError:
      messagebox.showwarning("Warning", "Please select a task to delete.")

  def save_tasks(self):
    tasks = self.task_listbox.get(0, tk.END)
    with open(DATA_FILE, "w") as f:
      json.dump(list(tasks), f, indent=4)

  def load_tasks(self):
    if os.path.exists(DATA_FILE):
      try:
        with open(DATA_FILE, "r") as f:
          tasks = json.load(f)
          for task in tasks:
            self.task_listbox.insert(tk.END, task)
      except json.JSONDecodeError:
        pass


if __name__ == "__main__":
  root = tk.Tk()
  app = TodoApp(root)
  root.mainloop()
