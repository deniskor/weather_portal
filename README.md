# Mini Weather Portal (Django 2.2 project)

This is a mini weather portal.

## How to install
#### Requirements
*   Python 3.7 (```sudo apt install python3.7```)
*   Virtual Environment (```sudo apt install python3.7-venv```)
*   git bash (```sudo apt install git```)
*   nano (or another text editor)

#### Cloning repo and creating Virtualenv:
1)  ```git clone https://github.com/deniskor/weather_portal.git```
2)  ```cd weather_portal```
3)  ```python3.7 -m venv venv```
4)  ```source venv/bin/activate```
5)  ```pip install -r requirements.txt```

#### Creating environment file:
1) ```nano **.env**``` (*this file must be stored in directory with manage.py*)
2) Write environment variables:
    ```
   POSTGRES_CONNECTION_STRING=postgres://[username]:[password]@[host]:[port]/[db_name]
   SECRET_KEY={unique string}
   OPEN_WEATHER_API_TOKEN={your openweather api token}
   DEBUG=False (or True if you want) 
    ```
3) Save **.env** file in text editor

#### Django migrations and static:
1) ```python manage.py migrate```
2) ```python manage.py shell < load_cities_db.py```
3) ```python manage.py collectstatic```


#### Run server
1) ```python manage.py runserver``` 


