# WatchWise

**WatchWise** is a Python/Django project for tracking movies and TV shows.

## Project Setup

Follow these steps to set up the project:

### **Step 1**: Clone the project

```bash
git clone https://github.com/lucchesilorenzo/watchwise_prova.git
```

### **Step 2**: Navigate to the directory

```bash
cd watchwise_prova
code .
```

### **Step 3**: Create and activate a virtual environment

```bash
python -m venv .venv
```

#### Activate for MacOS & Linux

```bash
source .venv/bin/activate
```

#### Activate for Windows (Git Bash)

```bash
source .venv/Scripts/activate
```

### **Step 4**: Install dependencies

```bash
pip install -r requirements.txt
```

### **Step 5**: Download PyGraphViz packages for Windows

Download the latest Windows packages from
[here.](https://graphviz.org/download)

1. Extract the ZIP archive
2. Copy all the files from the bin folder and paste them into watchwise_prova/.venv/Scripts

A list of commands for graph models
[here.](https://django-extensions.readthedocs.io/en/latest/graph_models.html)

### **Step 6**: Migrate the database and create a superuser

```bash
cd watchwise_project
```

```bash
python manage.py migrate
python manage.py createsuperuser
```

### **Step 7**: Run the server

```bash
python manage.py runserver
```

### **Step 8**: Go to http://127.0.0.1:8000/watchwise/
