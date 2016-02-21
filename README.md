#### Deploying to heroku
Follow instructions in https://devcenter.heroku.com/articles/getting-started-with-python#introduction
main commands:
    heroku create
    git push heroku master

#### Usage instructions

Index page has the owned games for the user. If not logged in, will redirect to browse games (/games).

Game page (/game/id) (access by pressing game div). Has the game name, price, description etc. Can be bought if user logged in and not already bought. Social sharing.
If user logged in and user has bought the game, the game can be played here. Shows the top scores as well.

Browse games (/games), has search and sort functionality. If user is not logged in the, game buying is disabled. If user has logged in, the owned games are not visible here. Gamelist hides the buy button, if screen has no space for it. Then the game can be bought from the individual game page (game/id).

Dev pages (/dev/). Developer can access the developer pages. From there user can create/edit/delete the games. Game statistics are also available there.
Deleting the game is in edit game form (delete button).

Login (accounts/login). User can either log from the navigation login or from the url (accounts/login). Facebook login will ask user to create userprofile after succesful facebook login.

Register pages (accounts/register) allows user to create new account and select account type (dev or customer). New account need to be active. User is inactive by default. You can activate your user from /admin with admin credentials (admin, pass:DreamOn).

You can register yourself as a developer or customer. There is already developer and customer accounts:
    username: customer
    password: customer
    username: developer
    password: developer
