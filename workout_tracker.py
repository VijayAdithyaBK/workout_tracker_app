import sqlite3
import tkinter as tk
from datetime import date

# Connect to the SQLite database
conn = sqlite3.connect('workout_tracker.db')
cursor = conn.cursor()


def create_tables():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS exercises (
            id INTEGER PRIMARY KEY,
            name TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS workouts (
            id INTEGER PRIMARY KEY,
            exercise_id INTEGER,
            date DATE,
            reps INTEGER,
            FOREIGN KEY (exercise_id) REFERENCES exercises (id)
        )
    ''')
    conn.commit()


def add_exercise(name):
    cursor.execute('INSERT INTO exercises (name) VALUES (?)', (name,))
    conn.commit()


def add_workout(exercise_id, reps):
    today = date.today()
    cursor.execute('INSERT INTO workouts (exercise_id, date, reps) VALUES (?, ?, ?)',
                   (exercise_id, today, reps))
    conn.commit()


def delete_exercise(exercise_id):
    cursor.execute('DELETE FROM exercises WHERE id = ?', (exercise_id,))
    cursor.execute('DELETE FROM workouts WHERE exercise_id = ?', (exercise_id,))
    conn.commit()


def list_exercises():
    cursor.execute('SELECT * FROM exercises')
    exercises = cursor.fetchall()

    if exercises:
        exercise_listbox.delete(0, tk.END)
        for exercise in exercises:
            exercise_listbox.insert(tk.END, exercise[1])  # Display exercise name without numbers


def list_exercises_for_view():
    cursor.execute('SELECT * FROM exercises')
    exercises = cursor.fetchall()

    if exercises:
        exercise_listbox_view.delete(0, tk.END)
        for exercise in exercises:
            exercise_listbox_view.insert(tk.END, exercise[1])  # Display exercise name without numbers


def log_workout_screen():
    log_frame.pack_forget()
    main_menu_frame.pack_forget()
    view_reps_frame.pack_forget()
    settings_frame.pack_forget()
    log_frame.pack()
    log_frame_back_button.pack(side=tk.BOTTOM)  # Place the back button at the bottom


def view_reps_screen():
    log_frame.pack_forget()
    main_menu_frame.pack_forget()
    view_reps_frame.pack()
    settings_frame.pack_forget()

    # Clear existing items in the listbox
    view_reps_frame_listbox.delete(1.0, tk.END)

    # Populate the listbox with exercises
    list_exercises_for_view()
    view_reps_frame_listbox.pack()
    view_reps_frame_label.config(text="Select an exercise to view reps for the current month:")

    # Create the "View Reps" button only once
    if not hasattr(view_reps_screen, 'view_reps_button'):
        view_reps_screen.view_reps_button = tk.Button(view_reps_frame, text="View Reps", command=view_reps)
        view_reps_screen.view_reps_button.pack()

    # Place the back button at the bottom
    view_reps_frame_back_button.pack(side=tk.BOTTOM)


def settings_screen():
    log_frame.pack_forget()
    main_menu_frame.pack_forget()
    view_reps_frame.pack_forget()
    settings_frame.pack()

    # Populate the listbox in the settings screen with exercises
    list_exercises()

    settings_frame_listbox.delete(0, tk.END)  # Clear existing items
    for exercise in exercise_listbox.get(0, tk.END):
        settings_frame_listbox.insert(tk.END, exercise)

    settings_frame_label.config(text="Select an exercise to delete or add:")

    # Place the back button at the bottom
    settings_frame_back_button.pack(side=tk.BOTTOM)


def back_to_main_menu(frame):
    frame.pack_forget()
    main_menu_frame.pack()


def log_workout():
    selected_index = exercise_listbox.curselection()
    if selected_index:
        exercise_id = selected_index[0] + 1  # Adjust for 0-based indexing
        reps = reps_entry.get()
        add_workout(exercise_id, reps)
        reps_entry.delete(0, tk.END)
        log_status_label.config(text="Workout logged successfully!")


def view_reps():
    selected_index = exercise_listbox_view.curselection()
    if selected_index:
        exercise_id = selected_index[0] + 1  # Adjust for 0-based indexing
        cursor.execute('''
            SELECT strftime('%Y-%m', date) AS month, SUM(reps) 
            FROM workouts 
            WHERE exercise_id = ? 
            GROUP BY month
            ORDER BY month
        ''', (exercise_id,))
        monthly_reps_data = cursor.fetchall()
        if monthly_reps_data:
            view_reps_frame_listbox.delete(1.0, tk.END)
            view_reps_frame_listbox.insert(tk.END, "Month     | Reps\n")
            view_reps_frame_listbox.insert(tk.END, "----------------\n")
            for row in monthly_reps_data:
                month = row[0]
                reps = row[1]
                view_reps_frame_listbox.insert(tk.END, f"{month} | {reps}\n")
        else:
            view_reps_frame_listbox.delete(1.0, tk.END)
            view_reps_frame_listbox.insert(tk.END, "No workout data available for this exercise.")
    else:
        view_reps_frame_listbox.delete(1.0, tk.END)
        view_reps_frame_listbox.insert(tk.END, "Select an exercise first.")


def settings_delete_exercise():
    selected_index = settings_frame_listbox.curselection()
    if selected_index:
        selected_index = selected_index[0]  # Get the index of the selected item
        exercise_name = settings_frame_listbox.get(selected_index)  # Get the selected exercise name
        cursor.execute('SELECT id FROM exercises WHERE name = ?', (exercise_name,))
        exercise_id = cursor.fetchone()
        if exercise_id:
            exercise_id = exercise_id[0]  # Extract the exercise ID
            delete_exercise(exercise_id)
            settings_frame_listbox.delete(selected_index)  # Delete the selected exercise from the listbox
            log_status_label.config(text="Exercise deleted successfully!")
        else:
            log_status_label.config(text="Exercise not found in the database.")


def settings_add_exercise():
    exercise_name = settings_frame_entry.get()
    if exercise_name:
        add_exercise(exercise_name)
        settings_frame_listbox.insert(tk.END, exercise_name)
        settings_frame_entry.delete(0, tk.END)

        # Update the list of exercises in the log workout screen
        list_exercises()

    else:
        log_status_label.config(text="Please enter an exercise name.")


# Create the main application window
app = tk.Tk()
app.title("Workout Tracker")

# Create frames for each screen
main_menu_frame = tk.Frame(app)
log_frame = tk.Frame(app)
view_reps_frame = tk.Frame(app)
settings_frame = tk.Frame(app)

# Create and configure GUI widgets for the main menu
main_menu_label = tk.Label(main_menu_frame, text="Main Menu")
log_workout_button = tk.Button(main_menu_frame, text="Log Workout", command=log_workout_screen)
view_reps_button = tk.Button(main_menu_frame, text="View Reps", command=view_reps_screen)
settings_button = tk.Button(main_menu_frame, text="Settings", command=settings_screen)

# Create and configure GUI widgets for the log workout screen
log_frame_label = tk.Label(log_frame, text="Log Workout")
exercise_listbox = tk.Listbox(log_frame, selectmode=tk.SINGLE)
reps_label = tk.Label(log_frame, text="Reps:")
reps_entry = tk.Entry(log_frame)
log_button = tk.Button(log_frame, text="Log Workout", command=log_workout)
log_status_label = tk.Label(log_frame, text="", fg="green")
log_frame_back_button = tk.Button(log_frame, text="Back to Main Menu", command=lambda: back_to_main_menu(log_frame))

# Create and configure GUI widgets for the view reps screen
view_reps_frame_label = tk.Label(view_reps_frame, text="View Reps")
exercise_listbox_view = tk.Listbox(view_reps_frame, selectmode=tk.SINGLE)
view_reps_frame_back_button = tk.Button(view_reps_frame, text="Back to Main Menu",
                                        command=lambda: back_to_main_menu(view_reps_frame))
view_reps_frame_listbox = tk.Text(view_reps_frame, height=10, width=30)

# Create and configure GUI widgets for the settings screen
settings_frame_label = tk.Label(settings_frame, text="Settings")
settings_frame_listbox = tk.Listbox(settings_frame, selectmode=tk.SINGLE)
settings_frame_entry = tk.Entry(settings_frame)
settings_frame_add_button = tk.Button(settings_frame, text="Add Exercise", command=settings_add_exercise)
settings_frame_delete_button = tk.Button(settings_frame, text="Delete Exercise", command=settings_delete_exercise)
settings_frame_back_button = tk.Button(settings_frame, text="Back to Main Menu",
                                       command=lambda: back_to_main_menu(settings_frame))

# Place widgets on the main menu screen
main_menu_label.pack()
log_workout_button.pack()
view_reps_button.pack()
settings_button.pack()

# Place widgets on the log workout screen
log_frame_label.pack()
exercise_listbox.pack()
reps_label.pack()
reps_entry.pack()
log_button.pack()
log_status_label.pack()
log_frame_back_button.pack(side=tk.BOTTOM)

# Place widgets on the view reps screen
view_reps_frame_label.pack()
exercise_listbox_view.pack()
view_reps_frame_listbox.pack()
view_reps_frame_back_button.pack()

# Place widgets on the settings screen
settings_frame_label.pack()
settings_frame_listbox.pack()
settings_frame_entry.pack()
settings_frame_add_button.pack()
settings_frame_delete_button.pack()
settings_frame_back_button.pack()

# Create database tables if they don't exist
create_tables()

# Populate the exercise list
list_exercises()

# Start the GUI application with the main menu
main_menu_frame.pack()
app.mainloop()

# Close the database connection when the GUI is closed
conn.close()
