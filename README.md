# WatchWise

WatchWise is a full-stack project designed for tracking both movies and TV shows. It is developed using Django/Python for the backend and HTML/CSS/Bootstrap for the frontend.

The program aims to assist users in navigating the TMDB database, a very popular public media database. It offers numerous functionalities, including saving TV shows and movies into the database along with preferences and comments, filtering records by name and list type, updating and deleting entries, and much more.


## Project Setup

Follow these steps to set up the project:


### **Step 1**: Clone the project

```sh
git clone https://github.com/lucchesilorenzo/watchwise_prova.git
```


### **Step 2**: Navigate to the directory

```sh
cd watchwise_prova
code .
```


### **Step 3**: Create and activate a virtual environment

```sh
python -m venv .venv

# Activate for MacOS & Linux
source .venv/bin/activate

# Activate for Windows (Git Bash)
source .venv/Scripts/activate
```

### **Step 4**: Install dependencies

```sh
pip install -r requirements.txt
```


### **Step 5**: Download PyGraphViz packages for Windows

Download the latest Windows packages from
[here.](https://graphviz.org/download)

1. Extract the ZIP archive
2. Copy all the files from the bin folder and paste them into ```watchwise_prova/.venv/Scripts```

A list of commands for graph models
[here.](https://django-extensions.readthedocs.io/en/latest/graph_models.html)


### **Step 6**: Migrate the database and create a superuser

```sh
cd watchwise_project
python manage.py migrate
python manage.py createsuperuser
```


### **Step 7**: Run the server

```sh
python manage.py runserver
```


### **Step 8**: Go to http://127.0.0.1:8000/watchwise/


## Future Plans

- Implement authentication and optimize user login/logout functionalities.
- Enhance the front-end experience with a robust framework like React or Angular.


## References

https://developer.themoviedb.org/reference/intro/getting-started


## Team

- Lorenzo Lucchesi
- Gianni Jin