#Installation Steps#

This will all be done from the command line

1. Ensure Python and pip are installed on your system
    a. `python -V` will tell you if python is installed
    b. `pip -V` will tell you if pip is installed

2. Once Python and pip are confirmed as installed, install requirements
    a. From top level directory of this repo, run `pip install -r requirements.txt`

3. In second level directory (where `manage.py` resides)
    1. `./manage.py migrate`
    2. `./manage.py createsuperuser` and follow directions on screen
    3. `./manage.py shell`
    4. `from db_pop import pop_db`
    5. `pop_db()`
    6. `exit`
    7. `./manage.py runserver 0.0.0.0:8000`

You can now access the app at localhost:8000 (or the ip address of wherever your workstation is)

`localhost:8000` will give you the point of sale view. Creating a transaction will give you the transaction created view
`localhost:8000/create_event/` will give you the create event view (needed to create transactions). Creating an event will give you the event created view
`localhost:8000/admin` will take you to the admin site (which is already styled, but you can poke around in the backend using your superuser credentials)

Templates can be found in pos/pos/templates/pos
CSS and Javascript can go into pos/pos/static. CSS already has a directory, pos/pos/static/css
