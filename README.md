# Setup and run

## Link

git@github.com:eamanola/securiltyflawed.git

## Installation instructions

The app is built on top of django framework. please refer to official documentation for installation guide [here](https://docs.djangoproject.com/en/3.2/topics/install/).

## Setting up db and users

To setup the app run

`$ python3 manage.py migrate`

this will setup the db, as well as create 2 test users.

## Resetting the app

To reset the app, simply remove `db.sqlite3` file, and run

`$ python3 manage.py migrate`

again.

## Running the app

To run app, run

`$ python3 manage.py runserver`

and follow instructions in the terminal.

## Default users

By default two users are created

* user1:user1
* user2:user2

# Security Flawed

This is a simple messaging app, where users can send free text to each other. 5 intentional security flaws are introduced into the system, and they are listed below. Any other flaw in the app is unintentional, and should be reported to FBI asap.

Flaws below are named as mentioned in [OWASP TOP10](https://owasp.org/www-project-top-ten/).

Line numbers are replaced, with the code on line, as the number may change during writing.

## Flaw 1) A1:2017-Injection

### in code:

module: `views.message`

line: `conn = sqlite3.connect('./db.sqlite3')` onwards

### description

In module views.message, responsible for handling sent messages, the developer has decided for unfathomable reasons, insert part of the message object, namely the message text itself using sql directly.

Furthermore he is using string concatenation to create the sql query.

To make things worse, he is using `executescript` api (instead of `execute`) to execute a single sql command.

With such a setup, it easy for an attacker to execute unintended sql. For example delete all messages, by sending a message `1\"; DROP TABLE messaging_message;`. If you try this, please see above "resetting the app", to get the app running again.

### Fix

Most fixes for this are provided both by django, and python itself. As evident in description above, many steps are required to enable this vulnerability.

In the trivial case of saving a string to db, the developer should continue to use django's ORM, and not use direct sql at all. Django will take case of proper string escaping for us.

In case, for whatever reason, direct sql access is required, the developer is strongly recommended to use sqlite3 placeholders (?) instead of escaping the parameters themselves. More info about placeholders [here](https://docs.python.org/3/library/sqlite3.html).

Furthermore, when a single command is being executed, developer should use the limited `execute` API.

## Flaw 2) A2:2017-Broken Authentication

### in code

module: `securityflawed.settings`

line: `SESSION_ENGINE = 'securityflawed.flawedsession'`

### description

Here the session engine key generation has be overwritten, with a predictable key generator. This makes the session id prone to brute force guessing.

Should an attacker find a value of session id, they can impersonate the user, who is logged with the guessed session id.

### Fix

Session id should be made long and complex enough, that brute force guessing is not feasible. A good place to start is just use the default django / framework implementation.

## Flaw 3) A3:2017-Sensitive Data Exposure

### in code

module: `template.user.html`

line: `<option value="{{user.id}}">{{user.username}} [{{user.email}}]</option>`

### description

Here the developer has unnecessarily exposed all of the user emails to all of the other users.

This allows an ill-intended user to collect all the emails in the system for his malicious purposes, but does not provided a well intended, or normal user any additional value.

While showing email makes sense in an email application, it is not required for a messaging app. Hence should not be shown.

### fix

From functionality point of view showing emails is not necessary, and `user.username` is enough identify unique accounts.

## Flaw 4) A5:2017-Broken Access Control

### In code

module: `views.user`

line: `user = User.objects.get(username=user_name)`

### description

In views.user, which is responsible for showing a user's messages and allowing the logged user to send messages to other users, login is required. However the developer has decided to allow direct access to a specific user's page, by adding username to the url (/:user_name). This has unintentionally enabled any user to access any other user's page, and read their messages.

### fix

while adding username to the url is a nice touch, the current user should not be deduced from the url (parameters), but from session logged user via `request.user`. The flawed line should then be `user = request.user`.

## Flaw 5) A7:2017-Cross-Site Scripting XSS

module: `template.user.html`

line: `{% autoescape off %}`

## Description

As the line suggests developer has decided to turn off autoescape feature of django. The reasoning here might be to allow for example, inserting html images and stylings into the messages. This however also allows sending <script /> tags, eg <script>alert(1)</script>.

## Fix

The escaping of html tags should be always kept on. In case styling and images feature is needed, other syntax libraries, such as, README.md syntax shoule be used.
