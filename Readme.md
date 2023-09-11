# Workout Tracker Application

The Workout Tracker Application is a versatile and user-friendly tool designed to simplify the process of tracking workouts, monitoring progress, and managing your exercise routine. Whether you're a fitness enthusiast, a beginner on a fitness journey, or someone looking to maintain an active lifestyle, this application can help you achieve your fitness goals and maintain an organized workout routine.

![Workout Tracker](screenshots/main_menu.png)

## Features

- **Log Workout:** Easily record your daily workouts, selecting from a list of predefined exercises or adding custom exercises to match your specific routine.

- **View Reps:** Analyze your workout history by viewing the total reps completed for specific exercises in each month. Gain insights into your progress and set realistic fitness goals.

- **Settings:** Customize your exercise list by adding new exercises or deleting ones you no longer need, ensuring your workout tracking is tailored to your unique fitness journey.

## File Structure

The project's file structure is well-organized to keep the codebase clean and maintainable. Key files and directories include:

- `create_database.py` and `workout_tracker.py` for application functionality.
- `workout_tracker.db` for data storage.
- `README.md` for documentation.
- `screenshots` directory for user guidance.

## Database Schema

The application's database schema ensures efficient data management and data integrity. It consists of the `exercises` and `workouts` tables, facilitating the storage of exercise and workout information.

## Usage

Detailed instructions on how to navigate the application's Main Menu and utilize its features effectively are provided in the [Usage Guide](#usage).

## Getting Started

1. Clone this repository to your local machine.
2. Set up a Python virtual environment:
   ```bash
   python -m venv venv
   ```
3. Activate the virtual environment:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS and Linux:
     ```bash
     source venv/bin/activate
     ```
4. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Run the `create_database.py` script to create the database:
   ```bash
   python create_database.py
   ```
6. Start the application by running the `workout_tracker.py` script:
   ```bash
   python workout_tracker.py
   ```

## Contribution

Contributions to the Workout Tracker Application are welcome! If you find issues, have suggestions, or want to contribute improvements, please open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE). You are free to use, modify, and distribute this software for personal or commercial use.
