import tkinter as tk
from tkinter import messagebox, ttk
import json
import os

TASKS_FILE = "tasks.json"

# Load tasks
if os.path.exists(TASKS_FILE):
    with open(TASKS_FILE, "r") as f:
        tasks = json.load(f)
else:
    tasks = []

current_index = 0


def save_tasks():
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f, indent=4)


def add_task():
    global current_index
    task = task_entry.get().strip()
    if task:
        tasks.append({"task": task, "done": False})
        save_tasks()
        task_entry.delete(0, tk.END)
        current_index = len(tasks) - 1
        refresh_task_card()
    else:
        messagebox.showwarning("⚠ Input Error", "Please enter a task.")


def delete_task():
    global current_index
    if tasks:
        tasks.pop(current_index)
        save_tasks()
        if current_index >= len(tasks):
            current_index = len(tasks) - 1
        refresh_task_card()
    else:
        messagebox.showwarning("⚠ Selection Error", "No task to delete.")


def mark_done():
    if tasks:
        tasks[current_index]["done"] = True
        save_tasks()
        refresh_task_card()
    else:
        messagebox.showwarning("⚠ Selection Error", "No task to mark.")


def refresh_task_card():
    task_label.config(text="No tasks available", fg="gray")
    status_label.config(text="")
    update_progress()

    if tasks:
        task = tasks[current_index]
        task_label.config(
            text=task["task"],
            fg="#ff5722" if not task["done"] else "#2ecc71"
        )
        status = "✓ Completed" if task["done"] else "✗ Pending"
        status_label.config(
            text=status,
            fg="#2ecc71" if task["done"] else "#e74c3c"
        )


def next_task():
    global current_index
    if tasks:
        current_index = (current_index + 1) % len(tasks)
        refresh_task_card()


def prev_task():
    global current_index
    if tasks:
        current_index = (current_index - 1) % len(tasks)
        refresh_task_card()


def update_progress():
    if tasks:
        done_count = sum(1 for t in tasks if t["done"])
        percent = int((done_count / len(tasks)) * 100)
        progress_var.set(percent)
        progress_label.config(text=f"Progress: {percent}%")
    else:
        progress_var.set(0)
        progress_label.config(text="No tasks")


# ---------------- GUI ----------------
root = tk.Tk()
root.title("🎨 Colorful To-Do Dashboard")
root.geometry("550x450")
root.configure(bg="#f9f9f9")

style = ttk.Style()
style.theme_use("clam")
style.configure("TButton", font=("Arial", 11, "bold"), padding=6)
style.configure("TProgressbar", thickness=15, troughcolor="#eeeeee", background="#4caf50")

# Title
title_label = tk.Label(
    root, text="📋 To-Do Dashboard",
    font=("Arial Rounded MT Bold", 20),
    bg="#f9f9f9", fg="#3f51b5"
)
title_label.pack(pady=10)

# Progress bar
progress_var = tk.IntVar()
progress_bar = ttk.Progressbar(root, orient="horizontal", length=400, variable=progress_var, mode="determinate")
progress_bar.pack(pady=5)

progress_label = tk.Label(root, text="No tasks", font=("Arial", 11), bg="#f9f9f9", fg="#555")
progress_label.pack()

# Entry + Add
entry_frame = tk.Frame(root, bg="#f9f9f9")
entry_frame.pack(pady=10)

task_entry = ttk.Entry(entry_frame, width=40, font=("Arial", 11))
task_entry.pack(side=tk.LEFT, padx=5)

add_btn = ttk.Button(entry_frame, text="➕ Add Task", command=add_task)
add_btn.pack(side=tk.LEFT)

# Card
card_frame = tk.Frame(root, bg="#ffffff", relief="raised", bd=4)
card_frame.pack(pady=20, padx=20, fill="both", expand=True)

task_label = tk.Label(
    card_frame, text="No tasks available",
    font=("Arial", 15, "bold"),
    wraplength=450,
    fg="gray", bg="white", pady=20
)
task_label.pack(pady=15)

status_label = tk.Label(card_frame, text="", font=("Arial", 13, "bold"), bg="white")
status_label.pack()

# Navigation
nav_frame = tk.Frame(root, bg="#f9f9f9")
nav_frame.pack(pady=10)

prev_btn = ttk.Button(nav_frame, text="⬅ Prev", command=prev_task)
prev_btn.pack(side=tk.LEFT, padx=10)

next_btn = ttk.Button(nav_frame, text="Next ➡", command=next_task)
next_btn.pack(side=tk.LEFT, padx=10)

# Action buttons
buttons_frame = tk.Frame(root, bg="#f9f9f9")
buttons_frame.pack(pady=10)

mark_done_btn = ttk.Button(buttons_frame, text="✅ Mark Done", command=mark_done)
mark_done_btn.pack(side=tk.LEFT, padx=5)

delete_btn = ttk.Button(buttons_frame, text="🗑 Delete", command=delete_task)
delete_btn.pack(side=tk.LEFT, padx=5)

refresh_task_card()
root.mainloop()
