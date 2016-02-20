Dreamer Team Project Plan
-----------------------

### 1. Team

525698 Teemu Huovinen
544566 Iiro Nurmi
544430 Mehrad Mohammadi


### 2. Goal

Our goal is the highest grade. We start by working with the mandatory features, and add as many optional features as we can.

### 3. Plans
Phase 1 planning and design:
Start by designing the platform, that includes the database schema and possible architecture/domain modeling.
Few mockups or if not too time consuming, we will build the "mockups" with HTML/CSS. The plan is to have a good picture on how the platform should look like.

Phase 2 Basic features:
Start to implement features based on the models. Basic player and developer features (CRUD create, read, update, delete).
Basic UI for those features.
From basic CRUD features on, implement more advanced.
This phase includes user registration and possibly authentication.

Phase 3 continuing to more features:
Features include:
* Authentication
* Payment functionality
* Game/service interaction

Phase 4 optional features (if time):
Optional features in prioritized order:

* 3rd party login
* RESTful API (which we will keep in mind from the start)
* Mobile friendly (which we will keep in mind from the start)
* Save-load and resolution feature
* Social media sharing

Phase 5 testing and polishing:
The phase 5 includes a lot of testing and then on fixing and enhancing the platform.



### 4. Process and Time Schedule

#### 4.1. Deadlines

* 13.12.2015   Group registration
* 20.12.2015   Project Plan
* 20.02.2016   Final submission


#### 4.2. Communication

Telegram is used for chat-type communication. Trello will be used for tracking of the progress of features.
We will try to arrange at least one face to face meeting per week.

#### 4.3. Initial schedule

* 04.01 - 14.01: Iiro is on holiday (partying) at Majorca.
* 04.01 - 10.01: Initial project setup
* 11.01 - 17.01: Design and environment setup
    * Database schema
    * Possible architecture/domain modeling
* 18.01 - 31.01: Basic player and developer features
    * User registration (possible authentication)
    * Player: Buy, play games, see high scores, record scores
    * Developer: Add games, see list of game sales
* 01.02 - 07.02: Mandatory features contd.
    * Authentication
    * Payment functionality
    * Game/service interaction
* 07.02 - 20.02: Optional functionalities and testing

### 5. Testing

We will practice TDD-style of feature design on a smaller feature, but not the whole project.
We will do unit-testing, where unit-tests are developed as part of feature development.
Acceptance testing will be performed in Heroku.

### 6. Risk Analysis

* Unforeseen, longer absences (sicknesses etc).
    * Only three group members so losing even one group member for a week is detrimental.

* Falling behind in schedule
    * Other courses, design refactoring

* Not dividing the project to tasks well enough
    * Lacking expertise produces development and design overhead

* Design failures
    * Not taking all features into consideration during design

* Teemu getting a job
    * Minor risk with a big impact to group member availability

### 7. Implemented features

<!-- What features you implemented and how much points you would like to give to yourself from those? -->


* Authentication (200 points)
    * Implemented with Django auth (with a confirmation e-mail)
    * Default user model is extended with UserProfile

* Basic customer functionality (300 points)
    * Buy a game, play bought games, record high scores
    * Can play only bought games
    * Cool search functionality

* Basic developer functionality (180 points)
    * Add, edit and delete a game
    * See game sales statistics
    * Can play own games only if separately bought (-20)

* Game/service interaction (100-200 points)
    * Interactions include receiving messages from the games:
      * receiving messages from the game: LOAD_REQUEST, SAVE, SETTING, and SCORE
      * sending messages to the games: LOAD and ERROR

* Quality of work (50 points)
    * Awesome UI and user experience
    * Reused utility functions
    * Almost nonexistent testing

* Non-functional requirements (190 points)
    * Project plan didn't include any diagrams (use case scenario etc.) (-10 points)
    * Project management and team communication was golden
        * Trello was used for task management, and Telegram was used for communication

* Game state Save/load (0-100 points):
    * Save/load functions are implemented, they show corresponsive temporary messages to let user know about them as well.

* 3rd party login (100 points)
    * Facebook login is integrated to the system.
    * After facebook login, the user chooses the user group (dev or customer)

* Mobile friendly design (50 points)
    * Responsive design is taken into account from the ground up
    * Bootstrap flatly theme is used to give the page a personal(ish) look

* Social media sharing (50 points)
    * Games can be shared from the game's page with custom description

<!-- Where do you feel that you were successful and where you had most problems.
Give sufficient details, this will influence the non-functional points awarded. -->

Problems:
* There were some problems with forms, understanding 'the Django way' was troublesome, minor problems.
* The structure of the GameData model and how to connect it to other models
* Back/frontend communication, JSON serialization
* Registration was a pain and we ended up changing our extended user model scheme

<!-- How did you divide the work between the team members - who did what? -->
We divided pretty well the project to individual tasks.
Iiro:
    - Developer pages (add/edit/delete)
    - Browse games page
    - Login finalization (page styling and error handling)
    - Social login and social sharing
    - Styling, responsivenes, templates

<!-- Instructions how to use your application and link to Heroku where it is deployed. -->
Heroku: http://dreamerteam.herokuapp.com/

Index page has the owned games for the user. If not logged in, will redirect to browse games (/games).

Game page (game/id) (access by pressing game div). Has the game name, price, description etc. Can be bought if user logged in and not already bought. Social sharing.
If user logged in and user has bought the game, the game can be played here. Shows the top scores as well.

Browse games (/games), has search and sort functionality. If user is not logged in the, game buying is disabled. If user has logged in, the owned games are not visible here. Gamelist hides the buy button, if screen has no space for it. Then the game can be bought from the individual game page (game/id).

Dev pages (/dev/). Developer can access the developer pages. From there user can create/edit/delete the games. Game statistics are also available there.
Deleting the game is in edit game form (delete button).

<!-- If a specific account/password (e.g. game developer) is required to try out and test some aspects of the work, please provide the details. -->
You can register yourself as a developer or customer. There is already developer and customer accounts:
    username: customer
    password: customer
    username: developer
    password: developer
