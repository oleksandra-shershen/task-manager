# IT Task Manager

## Overview
Task Manager is a Django-based web application designed for IT companies to manage their workers' tasks efficiently. This tool facilitates task assignment, progress tracking, and management through an intuitive web interface.

## Live Demo
Check out the live demo of the project here:
[Task Manager Live Demo](https://task-manager-l5zb.onrender.com)

## Test Credentials
- **Username:** test.user
- **Password:** privet1234

## Features
- **User Authentication:** Allows workers/users to register, log in.
- **Worker Profile Interface:** Users can view and update their profiles, including changing personal information.
- **Task Management:** Enables creating, updating, deleting, and marking tasks as completed.
- **Kanban Board:** Visualize task progress across different stages using the Kanban board, making it easy to manage multiple tasks efficiently.
- **Calendar View:** Features a calendar that displays task deadlines, helping users manage their time and deadlines more effectively.
- **Powerful Admin Panel:** Provides advanced management features for administrators to oversee all aspects of the platform.
- **Responsive Design:** Ensures a seamless experience across various devices and screen sizes.


## Technologies
- Django
- Python 3
- HTML5
- CSS3
- Bootstrap
- JavaScript

## Installation
Ensure Python 3 is already installed on your system. Follow these steps to set up the project locally:

1. **Clone the repository:**
```bash
https://github.com/oleksandra-shershen/task-manager.git
cd task-manager
```
This command downloads the project files to your local machine and changes your current directory to the project's root.

2. **Switch to the development branch:**
```bash
git checkout -b develop
```
This command creates and checks out a new branch called 'develop', which is typically used for development purposes.

3. **Set up a Python virtual environment:**
```bash
python3 -m venv venv
source venv/bin/activate (for UNIX)
venv\Scripts\activate (for Windows)
```
Creating a virtual environment isolates your Python/Django setup on a per-project basis, ensuring that dependencies from different projects do not conflict.

4. **Install required packages:**
```bash
pip install -r requirements.txt
```
This command installs all the necessary Python packages defined in the requirements.txt file to run the project.

5. **Run database migrations:**
```bash
python manage.py migrate
```
This command applies database migrations to your DBMS. It's essential for setting up or updating your database schema.

6. **Start the Django development server:**
```bash
python manage.py runserver
```
Launches the Django development server, allowing you to access the web application via http://127.0.0.1:8000/ in your web browser.


Each of these steps helps set up the Task Manager project in a development environment, making it ready for use and further development.

# DB Structure:
![image](https://github.com/oleksandra-shershen/task-manager/assets/105819546/6e5cda7d-bb3b-4e29-a8d0-d18f9d796ce5)
[Link](https://dbdiagram.io/d/task-manager-661cd94d03593b6b61fd9694) to the diagram



