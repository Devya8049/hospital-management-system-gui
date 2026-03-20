import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import datetime

from doctor_manager import add_doctor, remove_doctor, update_doctor, view_doctors, load_doctors

PATIENTS_FILE = "patients.txt"
ABOUT_FILE = "about.txt"

def title_case(s):
    return ' '.join([w.capitalize() for w in s.split()])

def load_patients():
    patients = []
    try:
        with open(PATIENTS_FILE, "r", encoding="utf-8") as f:
            for line in f:
                if not line.strip():
                    continue
                parts = line.strip().split('|')
                if len(parts) >= 8:
                    patient = {
                        "id": parts[0].strip(),
                        "name": title_case(parts[1].strip()),
                        "age": parts[2].strip(),
                        "gender": title_case(parts[3].strip()),
                        "disease": title_case(parts[4].strip()),
                        "doctor": title_case(parts[5].strip()),
                        "bill": parts[6].strip(),
                        "doctor_time": parts[7].strip(),
                        "medicines": parts[8].strip() if len(parts) >= 9 else ""
                    }
                    patients.append(patient)
    except Exception as e:
        messagebox.showerror("Error", f"Could not load patients.txt\n{e}")
    return patients

def save_patients(patients):
    try:
        with open(PATIENTS_FILE, "w", encoding="utf-8") as f:
            for p in patients:
                f.write(f"{p['id']}|{p['name']}|{p['age']}|{p['gender']}|{p['disease']}|{p['doctor']}|{p['bill']}|{p['doctor_time']}|{p.get('medicines','')}\n")
    except Exception as e:
        messagebox.showerror("Error", f"Could not save patients.txt\n{e}")

def show_about():
    try:
        with open(ABOUT_FILE, "r", encoding="utf-8") as f:
            about_text = f.read()
    except Exception as e:
        about_text = "About information not available.\n" + str(e)
    about_win = tk.Toplevel()
    about_win.title("About EMPOWER HOSPITAL")
    about_win.geometry("500x400")
    about_win.configure(bg="#fff9c4")  # Soft yellow
    tk.Label(about_win, text="EMPOWER HOSPITAL", font=("Segoe UI", 18, "bold"), fg="#1976d2", bg="#fff9c4").pack(pady=10)
    text = tk.Text(about_win, wrap="word", font=("Segoe UI", 11), bg="#fffde7", fg="#222")
    text.insert("1.0", about_text)
    text.config(state="disabled")
    text.pack(expand=True, fill="both", padx=10, pady=10)
    tk.Button(about_win, text="Close", command=about_win.destroy, bg="#c62828", fg="white", activebackground="#ef5350", font=("Segoe UI", 10, "bold")).pack(pady=8)

class HospitalApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("EMPOWER HOSPITAL")
        # Make the window open in full screen
        self.state('zoomed')  # For Windows full screen
        # self.attributes('-fullscreen', True)  # Uncomment for true fullscreen (esc to exit)
        self.configure(bg="#f3f7fa")
        self.resizable(False, False)

        # Modern color palette for backgrounds
        self.bg_colors = ["#f3f7fa", "#e1f5fe", "#ffe0b2", "#f8bbd0", "#c8e6c9", "#fff9c4", "#d1c4e9", "#b2dfdb"]
        self.current_bg = 0
        self.configure(bg=self.bg_colors[self.current_bg])

        # Animated border effect
        self.border_frame = tk.Frame(self, bg="#1976d2", bd=7, relief=tk.RIDGE)
        self.border_frame.pack(fill=tk.BOTH, expand=True, padx=12, pady=12)

        # Menu buttons frame with colored background
        btn_frame = tk.Frame(self.border_frame, bg="#1976d2")
        btn_frame.pack(side=tk.TOP, fill=tk.X, pady=12)

        # Modern button style with more color and icons
        btn_style = {
            "fg": "white",
            "activeforeground": "#222",
            "font": ("Segoe UI Emoji", 13, "bold"),
            "bd": 0,
            "highlightthickness": 0,
            "cursor": "hand2",
            "padx": 2,
            "pady": 2
        }

        tk.Button(btn_frame, text="➕ Add Patient", width=15, command=self.add_patient,
                  bg="#43a047", activebackground="#66bb6a", **btn_style).pack(side=tk.LEFT, padx=7)
        tk.Button(btn_frame, text="🔍 Search", width=12, command=self.search_patient_by_id,
                  bg="#039be5", activebackground="#4fc3f7", **btn_style).pack(side=tk.LEFT, padx=7)
        tk.Button(btn_frame, text="🩺 Assign Doctor", width=16, command=self.assign_doctor,
                  bg="#8e24aa", activebackground="#ba68c8", **btn_style).pack(side=tk.LEFT, padx=7)
        tk.Button(btn_frame, text="💊 Medicines", width=13, command=self.assign_medicines,
                  bg="#009688", activebackground="#4db6ac", **btn_style).pack(side=tk.LEFT, padx=7)
        tk.Button(btn_frame, text="📄 Patient Report", width=16, command=self.patient_report,
                  bg="#fbc02d", activebackground="#fff176", **btn_style).pack(side=tk.LEFT, padx=7)
        tk.Button(btn_frame, text="💳 Bill", width=10, command=self.generate_bill,
                  bg="#d84315", activebackground="#ff8a65", **btn_style).pack(side=tk.LEFT, padx=7)
        tk.Button(btn_frame, text="❗ About", width=8, command=show_about,
                  bg="#00acc1", activebackground="#4dd0e1", **btn_style).pack(side=tk.RIGHT, padx=7)
        tk.Button(btn_frame, text="⏻ Exit", width=8, command=self.destroy,
                  bg="#c62828", activebackground="#ef5350", **btn_style).pack(side=tk.RIGHT, padx=7)
        tk.Button(btn_frame, text="🔄 Refresh", width=10, command=self.refresh_table,
                  bg="#1976d2", activebackground="#64b5f6", **btn_style).pack(side=tk.LEFT, padx=7)

        # --- Doctor Management as a Dropdown Menu ---
        doctor_menu_btn = tk.Menubutton(
            btn_frame, text="👨‍⚕️ Doctor", width=14,
            bg="#3949ab", activebackground="#7986cb",
            **btn_style, relief=tk.RAISED, direction="below"
        )
        doctor_menu = tk.Menu(doctor_menu_btn, tearoff=0, bg="#e3f2fd", fg="#222", font=("Segoe UI Emoji", 11, "bold"))
        doctor_menu.add_command(label="👁️ View All Doctors", command=view_doctors)
        doctor_menu.add_command(label="➕ Add Doctor", command=add_doctor)
        doctor_menu.add_command(label="➖ Remove Doctor", command=remove_doctor)
        doctor_menu.add_command(label="✏️ Update Doctor", command=update_doctor)
        doctor_menu_btn.config(menu=doctor_menu)
        doctor_menu_btn.pack(side=tk.RIGHT, padx=7)

        # Table for all patients with style
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview.Heading", background="#1976d2", foreground="white", font=("Segoe UI", 11, "bold"))
        style.configure("Treeview", background="#e3f2fd", fieldbackground="#e3f2fd", foreground="#222", rowheight=28, font=("Segoe UI", 10))
        style.map("Treeview", background=[("selected", "#ffe082")])

        # Do not show "Medicines" in the main table
        self.cols = ["Patient ID", "Name", "Age", "Gender", "Disease", "Doctor", "Bill", "Doctor Assigned Time"]
        style.configure("Vertical.TScrollbar", gripcount=0,
                        background="#1565c0", darkcolor="#0d47a1", lightcolor="#1976d2",
                        troughcolor="#bbdefb", bordercolor="#1976d2", arrowcolor="white")
        vsb = ttk.Scrollbar(self.border_frame, orient="vertical", style="Vertical.TScrollbar")
        self.tree = ttk.Treeview(self.border_frame, columns=self.cols, show="headings", yscrollcommand=vsb.set)
        vsb.config(command=self.tree.yview)
        vsb.pack(side=tk.RIGHT, fill=tk.Y, padx=(0, 10), pady=10)
        for col in self.cols:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120 if col != "Doctor Assigned Time" else 160)
        self.tree.pack(expand=True, fill="both", padx=(10,0), pady=10)
        self.refresh_table()

        # Date and time label
        self.datetime_label = tk.Label(self.border_frame, font=("Segoe UI", 11, "bold"), bg="#bbdefb", fg="#0d47a1")
        self.datetime_label.pack(fill=tk.X)
        self.update_datetime()

        # Start animation
        self.animate_bg()

    def animate_bg(self):
        self.current_bg = (self.current_bg + 1) % len(self.bg_colors)
        self.configure(bg=self.bg_colors[self.current_bg])
        self.after(1200, self.animate_bg)

    def update_datetime(self):
        now = datetime.datetime.now().strftime("Date And Time: %d-%m-%Y %H:%M:%S")
        self.datetime_label.config(text=now)
        self.after(1000, self.update_datetime)

    def refresh_table(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        patients = load_patients()
        # Sort patients by Patient ID (as integer)
        patients.sort(key=lambda p: int(p.get("id", "0")))
        for p in patients:
            row = [
                p.get("id", ""),  # Still use 'id' from data, but header is "Patient ID"
                p.get("name", ""),
                p.get("age", ""),
                p.get("gender", ""),
                p.get("disease", ""),
                p.get("doctor", ""),
                p.get("bill", ""),
                p.get("doctor_time", "")
            ]
            self.tree.insert("", "end", values=row)

    def add_patient(self):
        win = tk.Toplevel(self)
        win.title("Add Patient")
        win.geometry("250x350")
        win.configure(bg="#e3f2fd")  # Light blue background
        fields = ["Patient ID", "Name", "Age", "Gender"]
        entries = {}
        for field in fields:
            tk.Label(win, text=field, bg="#e3f2fd", fg="#1976d2", font=("Segoe UI", 10, "bold")).pack()
            entry = tk.Entry(win, bg="#fffde7", fg="#222", font=("Segoe UI", 10))
            entry.pack()
            entries["id" if field == "Patient ID" else field.lower()] = entry

        # Disease selection
        tk.Label(win, text="Disease", bg="#e3f2fd", fg="#1976d2", font=("Segoe UI", 10, "bold")).pack()
        common_diseases = [
            "Fever", "Cold", "Headache", "Cough", "Hypertension",
            "Diabetes", "Asthma", "Allergy", "Stomach Pain", "Back Pain"
        ]
        disease_var = tk.StringVar(value=common_diseases[0])
        disease_combo = ttk.Combobox(win, textvariable=disease_var, values=common_diseases, state="readonly")
        disease_combo.pack()

        tk.Label(win, text="Or enter your own disease:", bg="#e3f2fd", fg="#1976d2", font=("Segoe UI", 9)).pack()
        custom_disease_entry = tk.Entry(win, bg="#fffde7", fg="#222", font=("Segoe UI", 10))
        custom_disease_entry.pack()

        def submit():
            patients = load_patients()
            disease = custom_disease_entry.get().strip()
            if not disease:
                disease = disease_var.get()
            new_patient = {
                "id": entries["id"].get().strip(),
                "name": title_case(entries["name"].get().strip()),
                "age": entries["age"].get().strip(),
                "gender": title_case(entries["gender"].get().strip()),
                "disease": title_case(disease),
                "doctor": "Not Assigned",
                "bill": "0.00",
                "doctor_time": "-",
                "medicines": ""
            }
            for p in patients:
                if p["id"] == new_patient["id"]:
                    messagebox.showerror("Error", "Patient ID already exists.", parent=win)
                    return
            patients.append(new_patient)
            save_patients(patients)
            messagebox.showinfo("Success", "Patient added successfully.", parent=win)
            win.destroy()
            self.refresh_table()

        tk.Button(win, text="Add", command=submit, bg="#43a047", fg="white", activebackground="#66bb6a", font=("Segoe UI", 10, "bold")).pack(pady=10)

    def search_patient_by_id(self):
        pid = simpledialog.askstring("Search Patient by ID", "Enter Patient ID:", parent=self)
        if not pid:
            return
        patients = load_patients()
        for p in patients:
            if p["id"] == pid.strip():
                info = (
                    f"Patient ID: {p['id']}\n"
                    f"Name: {p['name']}\n"
                    f"Age: {p['age']}\n"
                    f"Gender: {p['gender']}\n"
                    f"Disease: {p['disease']}\n"
                    f"Doctor: {p['doctor']}\n"
                    f"Bill: {p['bill']}\n"
                    f"Doctor Assigned Time: {p['doctor_time']}\n"
                    f"Medicines: {p.get('medicines', 'None')}"
                )
                # Custom popup with color
                win = tk.Toplevel(self)
                win.title("Patient Details")
                win.configure(bg="#fff9c4")  # Soft yellow
                tk.Label(win, text="Patient Details", font=("Segoe UI", 12, "bold"), bg="#fff9c4", fg="#d84315").pack(pady=5)
                tk.Label(win, text=info, font=("Segoe UI", 10), bg="#fffde7", fg="#222", justify="left").pack(padx=10, pady=10)
                tk.Button(win, text="Close", command=win.destroy, bg="#c62828", fg="white", activebackground="#ef5350", font=("Segoe UI", 10, "bold")).pack(pady=5)
                return
        messagebox.showerror("Error", "Patient Not Found.", parent=self)

    def assign_doctor(self):
        pid = simpledialog.askstring("Assign Doctor", "Enter Patient ID:", parent=self)
        if not pid:
            return
        patients = load_patients()
        for p in patients:
            if p["id"] == pid.strip():
                try:
                    age = int(p["age"])
                except ValueError:
                    messagebox.showerror("Error", "Invalid age for patient.", parent=self)
                    return
                now = datetime.datetime.now()
                hour = now.hour
                # Night shift: 22:00 to 07:00
                if hour >= 22 or hour < 7:
                    doctor = "Dr.Prasad"
                    messagebox.showinfo("Doctor Assigned", "Night shift: Doctor assigned: Dr.Prasad", parent=self)
                else:
                    doctor = None
                    is_female = p["gender"].strip().lower() == "female"
                    # --- Dynamically load doctors from doctor.txt ---
                    doctors = load_doctors()
                    options = []
                    display_lines = []
                    num = 1
                    for d in doctors:
                        # Only show Gynecologist for females above 12
                        if "gynecologist" in d["specialty"].lower():
                            if not (is_female and age > 12):
                                continue
                        display_lines.append(f"{num}. {d['name']} ({d['specialty']})")
                        options.append(d["name"])
                        num += 1
                    if not options:
                        messagebox.showerror("Error", "No suitable doctors available.", parent=self)
                        return
                    # Custom popup for doctor selection
                    win = tk.Toplevel(self)
                    win.title("Assign Doctor")
                    win.configure(bg="#f8bbd0")  # Pink
                    tk.Label(win, text="Select Doctor", font=("Segoe UI", 12, "bold"), bg="#f8bbd0", fg="#8e24aa").pack(pady=5)
                    opt_str = "\n".join(display_lines)
                    tk.Label(win, text=opt_str, font=("Segoe UI", 10), bg="#fce4ec", fg="#222", justify="left").pack(padx=10, pady=10)
                    choice_var = tk.IntVar()
                    entry = tk.Entry(win, textvariable=choice_var, font=("Segoe UI", 10), bg="#fffde7")
                    entry.pack()
                    def submit_doctor():
                        choice = choice_var.get()
                        if not choice or choice < 1 or choice > len(options):
                            messagebox.showerror("Error", "Invalid doctor choice.", parent=win)
                            return
                        doctor = options[choice - 1]
                        p["doctor"] = doctor
                        p["doctor_time"] = now.strftime("%d-%m-%Y %H:%M:%S")
                        save_patients(patients)
                        messagebox.showinfo("Success", f"Doctor assigned: {doctor}", parent=win)
                        win.destroy()
                        self.refresh_table()
                    tk.Button(win, text="Assign", command=submit_doctor, bg="#8e24aa", fg="white", activebackground="#ba68c8", font=("Segoe UI", 10, "bold")).pack(pady=5)
                    return
                p["doctor"] = doctor
                p["doctor_time"] = now.strftime("%d-%m-%Y %H:%M:%S")
                save_patients(patients)
                messagebox.showinfo("Success", f"Doctor assigned: {doctor}", parent=self)
                self.refresh_table()
                return
        messagebox.showerror("Error", "Patient Not Found.", parent=self)

    def assign_medicines(self):
        pid = simpledialog.askstring("Assign Medicines", "Enter Patient ID:", parent=self)
        if not pid:
            return
        patients = load_patients()
        patient = None
        for p in patients:
            if p["id"] == pid.strip():
                patient = p
                break
        if not patient:
            messagebox.showerror("Error", "Patient Not Found.", parent=self)
            return

        # Top 20 common medicines
        medicines = [
            "Paracetamol", "Ibuprofen", "Amoxicillin", "Cetirizine", "Azithromycin",
            "Metformin", "Amlodipine", "Omeprazole", "Atorvastatin", "Salbutamol",
            "Dolo 650", "Pantoprazole", "Levocetirizine", "Ciprofloxacin", "Diclofenac",
            "Ranitidine", "Losartan", "Montelukast", "Dexamethasone", "Clopidogrel"
        ]

        win = tk.Toplevel(self)
        win.title("Assign Medicines")
        win.geometry("350x450")
        win.configure(bg="#e3f2fd")
        tk.Label(win, text=f"Assign Medicines to {patient['name']}", font=("Segoe UI", 12, "bold"),
                 bg="#e3f2fd", fg="#009688").pack(pady=10)

        # Listbox for multiple selection
        listbox = tk.Listbox(win, selectmode=tk.MULTIPLE, font=("Segoe UI", 11), bg="#fffde7", fg="#222", height=12)
        for med in medicines:
            listbox.insert(tk.END, med)
        listbox.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        tk.Label(win, text="Or enter custom medicines (comma separated):", bg="#e3f2fd", fg="#1976d2", font=("Segoe UI", 9)).pack()
        custom_entry = tk.Entry(win, bg="#fffde7", fg="#222", font=("Segoe UI", 10))
        custom_entry.pack(padx=10, pady=5, fill=tk.X)

        def submit_medicines():
            selected = [medicines[i] for i in listbox.curselection()]
            custom = [m.strip() for m in custom_entry.get().split(",") if m.strip()]
            all_meds = selected + custom
            if not all_meds:
                messagebox.showerror("Error", "No medicines selected.", parent=win)
                return
            # Save medicines to patient record (add a new key if not present)
            patient["medicines"] = ", ".join(all_meds)
            # Save back to file (update all patients)
            save_patients(patients)
            messagebox.showinfo("Success", f"Medicines assigned:\n{patient['medicines']}", parent=win)
            win.destroy()

        tk.Button(win, text="Assign", command=submit_medicines, bg="#009688", fg="white",
                  activebackground="#4db6ac", font=("Segoe UI", 10, "bold")).pack(pady=10)

    def patient_report(self):
        pid = simpledialog.askstring("Patient Report", "Enter Patient ID:", parent=self)
        if not pid:
            return
        patients = load_patients()
        for p in patients:
            if p["id"] == pid.strip():
                win = tk.Toplevel(self)
                win.title("Patient Report")
                win.geometry("400x400")
                win.configure(bg="#d1c4e9")  # Lavender
                now = datetime.datetime.now().strftime("Date And Time: %d-%m-%Y %H:%M:%S")
                tk.Label(win, text=now, font=("Segoe UI", 10, "bold"), bg="#d1c4e9", fg="#3949ab").pack(pady=(10, 5))
                # Vertical report layout
                fields = [
                    ("Patient ID", p.get("id", "")),
                    ("Name", p.get("name", "")),
                    ("Age", p.get("age", "")),
                    ("Gender", p.get("gender", "")),
                    ("Disease", p.get("disease", "")),
                    ("Doctor", p.get("doctor", "")),
                    ("Bill", p.get("bill", "")),
                    ("Doctor Assigned Time", p.get("doctor_time", "")),
                    ("Medicines", p.get("medicines", ""))
                ]
                for label, value in fields:
                    frame = tk.Frame(win, bg="#f3e5f5")
                    frame.pack(fill=tk.X, padx=20, pady=3)
                    tk.Label(frame, text=f"{label}:", font=("Segoe UI", 10, "bold"), bg="#f3e5f5", fg="#512da8", anchor="w", width=20).pack(side=tk.LEFT)
                    tk.Label(frame, text=value, font=("Segoe UI", 10), bg="#ede7f6", fg="#222", anchor="w").pack(side=tk.LEFT, fill=tk.X, expand=True)
                tk.Button(win, text="Close", command=win.destroy, bg="#c62828", fg="white", activebackground="#ef5350", font=("Segoe UI", 10, "bold")).pack(pady=15)
                return
        messagebox.showerror("Error", "Patient Not Found.", parent=self)

    def generate_bill(self):
        pid = simpledialog.askstring("Generate Bill", "Enter Patient ID:", parent=self)
        if not pid:
            return
        patients = load_patients()
        for p in patients:
            if p["id"] == pid.strip():
                # Automatic bill calculation based on doctor specialty
                doctor_name = p["doctor"].strip().lower()
                bill = None

                # Night shift Dr.Prasad
                if doctor_name == "dr.prasad":
                    bill = 450
                else:
                    # Find doctor specialty from doctor.txt
                    doctors = load_doctors()
                    specialty = None
                    for d in doctors:
                        if d["name"].strip().lower() == doctor_name:
                            specialty = d["specialty"].strip().lower()
                            break
                    if specialty:
                        if "children specialist" in specialty:
                            bill = 650
                        elif "general physician" in specialty or "general" in specialty:
                            bill = 550
                        elif "pscologicalist" in specialty or "psychological" in specialty:
                            bill = 950
                        elif "gynecologist" in specialty:
                            bill = 750
                        elif "dermatologist" in specialty:
                            bill = 850
                    # fallback if not matched
                    if bill is None:
                        bill = 500

                p["bill"] = f"{bill:.2f}"
                save_patients(patients)
                # Custom popup for bill
                win = tk.Toplevel(self)
                win.title("Bill Generated")
                win.configure(bg="#b2dfdb")  # Mint
                tk.Label(win, text="Bill Generated", font=("Segoe UI", 12, "bold"), bg="#b2dfdb", fg="#00695c").pack(pady=5)
                tk.Label(win, text=f"Bill generated automatically for {p['name']}.\nTotal: {p['bill']}", font=("Segoe UI", 11), bg="#e0f2f1", fg="#222").pack(padx=10, pady=10)
                tk.Button(win, text="Close", command=win.destroy, bg="#c62828", fg="white", activebackground="#ef5350", font=("Segoe UI", 10, "bold")).pack(pady=5)
                self.refresh_table()
                return
        messagebox.showerror("Error", "Patient Not Found.", parent=self)

if __name__ == "__main__":
    app = HospitalApp()
    app.mainloop()
