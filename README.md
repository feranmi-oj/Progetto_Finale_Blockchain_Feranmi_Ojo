## START2LIMITED_SHOES_EDITION🔍
START2LIMITED_SHOES_EDITION is a platform to manage the sale of limited edition shoes through a charity auction.
    Each auction has a certain duration, and users of the platform can place any amount on any auction still in progress.
    the platform uses two databases: it uses Redis as the main database.
    In fact, if the platform in the future can generate a lot of attention and be used by an ever-increasing number of users who may require having to scale horizontally to handle the traffic, it needs a very fast database to manage the various bets, to then store the outcome of the auction,
    like all other user data, on a relational database.
**IMPORTANT**
Only super users can auction shoes

### Installation:
Before running the project, remember to install the followings:

* python virtual environment
* django
* djongo
* web3
* django-redis
* redis
* pymongo
### Start the project

- Before starting the runserver  in the terminal you need to do a first migration with:
```sh
    $ python manage.py migrate
 ```
    
* And create a superuser with: 
```sh
    $ python manage.py createsuperuser
 ```
- **Example Superuser**
 
    username: admin 
    
     password: admin


- Then, start the project by typing:
```sh
    $ python manage.py runserver 
```
   
* and to access the platform and start buying limited edtion shoes you must register on the registration page
## Built with:🔗
* Python
* Django
* Web3
* Redis
* HTML/CSS

## START2LIMITED_SHOES_EDITION Presentation
To have a preview of the site you can have a look at my Presentation
presentation file: "[Progetto-Finale-di-Feranmi-Ojo.pptx](https://github.com/feranmi-oj/Progetto_Finale_Blockchain_Feranmi_Ojo/blob/master/Progetto-Finale-Blockchain-di-Feranmi-Ojo.pptx)"


