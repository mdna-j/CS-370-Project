**Petabyte** – A Virtual Pet Desktop App

Petabyte is a Tamagotchi-inspired virtual pet desktop application built in Python using the Kivy framework. Users care for a digital pet whose behavior dynamically reflects the user's interactions and habits. The pet responds emotionally to both user input and tracked activity, offering a gamified way to encourage positive habits.

---

Features

- Interactive pet system with hunger, mood, health, and energy tracking
- Mood tracker with real-time emotional feedback
- Idle system that applies penalties for user inactivity
- Save/load system SQLite
- Login system to support multiple user profiles
- GUI built with Kivy for cross-platform desktop support
  
---

Technologies

| Tech/Tool    | Purpose                        |
|--------------|--------------------------------|
| `Python`     | Core logic                     |
| `Kivy`       | GUI framework for desktop UI   |
| `SQLite`     | Lightweight database used to store user and pet data  |
| `unittest`   | Unit testing                   |
| `Trello`     | Project planning               |
| `GitHub`     | Source control & collaboration |
| `Pixelab(Bitforge)`| Pet generation API |

---

Directory Structure  
PetaByte/  
├── database/           # SQLite database scripts and schema  
├── habit_tracker/      # Habit tracking logic and unit tests   
├── idle_tracker/       # Idle activity detection and mood mapping   
├── login_manager/      # User login and authentication system   
├── mood_tracker/       # Logic for mood changes and effects   
├── petsystem/          # Pet generation and animation logic   
├── UI/                 # Kivy GUI screens and styling   
├── main.py             # Application entry point   
├── README.md           # Project documentation   

---

How to Clone the Project:  
Step 1: Install Git  
Windows: Go to https://git-scm.com/download/win  
Run the downloaded installer and follow the default setup instructions.  

macOS: Open the Terminal app.  
Run this command: xcode-select --install  

Follow the prompts to install Git.  


Step 2: Open a Terminal or Command Prompt  
On Windows, press Windows + R, type cmd, and press Enter.  

On macOS, open the Terminal from Applications > Utilities.  

Step 3: Choose a Folder to Clone Into  
You can use cd to navigate to where you want to clone the project.   
Example: cd Desktop or cd Documents  

Step 4: Clone the Project from GitHub  
Use this command:  
git clone https://github.com/mdna-j/CS-370-Project.git  
This will create a folder called CS-370-Project in your current directory.   

Step 5: Open the Project  
Open the cloned folder in your code editor (like PyCharm or VS Code).  

Example in PyCharm:  
Open PyCharm  
Click "Open"  
Navigate to the cloned CS-370-Project folder and select it.  

---


**Group Members**:  
Jose Medina  
Kevin Mendoza  
Parker Miller  
