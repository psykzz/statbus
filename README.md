# lakiller.cz
This is an open source statbus for the [/tg/station](https://github.com/tgstation/tgstation/) database code Space Station 13 server. It was created to provide a python alternative for those that dislike other languages.

# Requirements
The following packages are required:
* bottle
* mysql-connector-python

You can install the requirements from the requirements.txt file.

# Setting up
Make sure you have a read-only database account and that you have whitelisted just the server you will be hosting this on for security reasons. Head into the config folder and either create a new file called production.ini (recommended for further security reasons) or open the config.ini file and edit the appropriate values.

```
[Database]
dbusername = username //The username for your database account.
dbpassword = password //The password for your database account.
dbhost = 127.0.0.1 //The IP address of your database server. If you're running both on one machine, leave it be.
dbport = 3306 //The port of your database server.
dbname = feedback //This is the name of the database, you likely won't need to change it.
```

# Contributing
Any help is welcome, your best bet is reaching out to me first on [this](https://discord.gg/2dFpfNE) Discord to talk about the feature you want to implement or to provide details about a bug.