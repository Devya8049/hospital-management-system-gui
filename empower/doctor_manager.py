import tkinter as tk
from tkinter import simpledialog, messagebox, ttk

DOCTORS_FILE = "doctor.txt"

def load_doctors():
    doctors = []
    try:
        with open(DOCTORS_FILE, "r", encoding="utf-8") as f:
            for line in f:
                if not line.strip():
                    continue
                parts = line.strip().split('|')
                if len(parts) >= 4:
                    doctor = {
                        "name": parts[0].strip(),
                        "specialty": parts[1].strip(),
                        "qualification": parts[2].strip(),
                        "contact": parts[3].strip()
                    }
                    doctors.append(doctor)
    except FileNotFoundError:
        pass
    except Exception as e:
        messagebox.showerror("Error", f"Could not load doctor.txt\n{e}")
    return doctors

def save_doctors(doctors):
    try:
        with open(DOCTORS_FILE, "w", encoding="utf-8") as f:
            for d in doctors:
                f.write(f"{d['name']}|{d['specialty']}|{d['qualification']}|{d['contact']}\n")
    except Exception as e:
        messagebox.showerror("Error", f"Could not save doctor.txt\n{e}")

def add_doctor():
    win = tk.Toplevel()
    win.title("Add Doctor")
    win.geometry("250x300")
    win.configure(bg="#e3f2fd")
    tk.Label(win, text="Add Doctor", font=("Segoe UI", 14, "bold"), bg="#e3f2fd", fg="#1976d2").pack(pady=10)
    labels = ["Name (with Dr. prefix):", "Specialty:", "Qualification:", "Contact:"]
    entries = []
    for lab in labels:
        tk.Label(win, text=lab, bg="#e3f2fd", fg="#1976d2", font=("Segoe UI", 10, "bold")).pack()
        e = tk.Entry(win, bg="#fffde7", fg="#222", font=("Segoe UI", 10))
        e.pack()
        entries.append(e)
    def submit():
        name, specialty, qualification, contact = [e.get().strip() for e in entries]
        if not name or not specialty or not qualification or not contact:
            messagebox.showerror("Error", "All fields are required.", parent=win)
            return
        doctors = load_doctors()
        for d in doctors:
            if d["name"].lower() == name.lower():
                messagebox.showerror("Error", "Doctor already exists.", parent=win)
                return
        doctors.append({
            "name": name,
            "specialty": specialty,
            "qualification": qualification,
            "contact": contact
        })
        save_doctors(doctors)
        messagebox.showinfo("Success", "Doctor added successfully.", parent=win)
        win.destroy()
    tk.Button(win, text="Add", command=submit, bg="#43a047", fg="white", activebackground="#66bb6a", font=("Segoe UI", 10, "bold")).pack(pady=10)

def remove_doctor():
    win = tk.Toplevel()
    win.title("Remove Doctor")
    win.geometry("300x180")
    win.configure(bg="#ffe0b2")
    tk.Label(win, text="Remove Doctor", font=("Segoe UI", 14, "bold"), bg="#ffe0b2", fg="#e65100").pack(pady=10)
    tk.Label(win, text="Enter Doctor Name to Remove:", bg="#ffe0b2", fg="#e65100", font=("Segoe UI", 10, "bold")).pack()
    entry = tk.Entry(win, bg="#fffde7", fg="#222", font=("Segoe UI", 10))
    entry.pack()
    def submit():
        name = entry.get().strip()
        if not name:
            return
        doctors = load_doctors()
        new_doctors = [d for d in doctors if d["name"].lower() != name.lower()]
        if len(new_doctors) == len(doctors):
            messagebox.showerror("Error", "Doctor not found.", parent=win)
            return
        save_doctors(new_doctors)
        messagebox.showinfo("Success", "Doctor removed successfully.", parent=win)
        win.destroy()
    tk.Button(win, text="Remove", command=submit, bg="#d84315", fg="white", activebackground="#ff8a65", font=("Segoe UI", 10, "bold")).pack(pady=10)

def update_doctor():
    win = tk.Toplevel()
    win.title("Update Doctor")
    win.geometry("300x150")
    win.configure(bg="#d1c4e9")
    tk.Label(win, text="Update Doctor", font=("Segoe UI", 14, "bold"), bg="#d1c4e9", fg="#512da8").pack(pady=10)
    tk.Label(win, text="Enter Doctor Name to Update:", bg="#d1c4e9", fg="#512da8", font=("Segoe UI", 10, "bold")).pack()
    entry = tk.Entry(win, bg="#fffde7", fg="#222", font=("Segoe UI", 10))
    entry.pack()
    def submit():
        name = entry.get().strip()
        if not name:
            return
        doctors = load_doctors()
        for d in doctors:
            if d["name"].lower() == name.lower():
                specialty = simpledialog.askstring("Update Doctor", f"Enter new Specialty (current: {d['specialty']}):")
                qualification = simpledialog.askstring("Update Doctor", f"Enter new Qualification (current: {d['qualification']}):")
                contact = simpledialog.askstring("Update Doctor", f"Enter new Contact Info (current: {d['contact']}):")
                if specialty:
                    d["specialty"] = specialty.strip()
                if qualification:
                    d["qualification"] = qualification.strip()
                if contact:
                    d["contact"] = contact.strip()
                save_doctors(doctors)
                messagebox.showinfo("Success", "Doctor details updated successfully.", parent=win)
                win.destroy()
                return
        messagebox.showerror("Error", "Doctor not found.", parent=win)
    tk.Button(win, text="Update", command=submit, bg="#8e24aa", fg="white", activebackground="#ba68c8", font=("Segoe UI", 10, "bold")).pack(pady=10)

def view_doctors():
    win = tk.Toplevel()
    win.title("All Doctors")
    win.geometry("700x300")
    win.configure(bg="#b2dfdb")
    tk.Label(win, text="All Doctors", font=("Segoe UI", 14, "bold"), bg="#b2dfdb", fg="#00695c").pack(pady=10)
    doctors = load_doctors()
    if not doctors:
        tk.Label(win, text="No doctor records found.", bg="#b2dfdb", fg="#00695c").pack()
        return
    cols = ["Name", "Specialty", "Qualification", "Contact"]
    tree = ttk.Treeview(win, columns=cols, show="headings")
    for col in cols:
        tree.heading(col, text=col)
        tree.column(col, width=160 if col == "Specialty" else 120)
    for d in doctors:
        tree.insert("", "end", values=(d["name"], d["specialty"], d["qualification"], d["contact"]))
    tree.pack(expand=True, fill="both", padx=10, pady=10)
    tk.Button(win, text="Close", command=win.destroy, bg="#c62828", fg="white", activebackground="#ef5350", font=("Segoe UI", 10, "bold")).pack(pady=5)