# back-communicenter

first create virtual enviroment: 
~~~
python -m venv "name of virtual enviroment"
~~~

see requirements.txt and install depencences

Setup the database:

~~~
flask db init
flask db migrate -m "migration name"
flask db upgrade
~~~

run the application:
~~~
flask run
~~~
