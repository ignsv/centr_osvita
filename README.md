## local deployment using vagrant
* ``vagrant up``
* ``vagrant ssh``
* ``cd /vagrant``
* ``cp env.example ./config/.env``
## Next you are in virual env
* ``pip install -r requirements/base.txt``
* ``./manage.py migrate``
## Load test data
* ``/manage.py loaddata test_db.json``
## Run the server
* ``./manage.py runserver``