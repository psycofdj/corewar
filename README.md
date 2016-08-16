<!-- markdown-toc start - Don't edit this section. Run M-x markdown-toc-generate-toc again -->
**Table of Contents**

- [Introduction](#introduction)
- [How to play](#how-to-play)
- [Install](#install)
- [Configuration](#configuration)
- [Run](#run)
    - [Standalone](#standalone)
    - [WebServer](#webserver)

<!-- markdown-toc end -->

Introduction
============

Corewar is a coding game where programs confront each others in a virtual machine.
Coded in a asm-like language, your program is assembled as a ship that races a cycling memory.
Each instructions cost a certain amount of CPU cycle, the fastest ship to complete 3 laps wins.


How to play
===========

You can either install corewar on your local machine or go to my self-hosted instance :
* http://corewar.marcelet.com/rules/ (French documentation)


Install
=======

```bash
# install dependencies
sudo apt-get install mysql-server python-mako python-ply python-cherrypy python-mysqldb

# checkout from git repo
git clone https://github.com/psycofdj/corewar.git

# enter corewar directory
cd corewar/src

# create default configuration
cp corewar.cfg.sample corewar.cfg

# bootstrap database
# -> it will prompt for mysql admin user/pass
# -> and creates new database and user according to corewar.cfg
./setup.py --install --modules=corewar
```

Configuration
=============

All options available from ```./corewar.py --help``` can be added in corewar.cfg file


Run
===

Corewar can be used as a standalone program to assemble and run ships or as a daemon web-server.


Standalone
----------

* compile ship : this command checks your code in file my_ship.s and output errors if any

```bash
./corewar.py --league=race --check-compile my_ship.s
```

* run ship : this command compiles and run your code in file my_ship.s

```bash
./corewar.py --league=race my_ship.s
```

you can add executions logs (to debug you ship) with the --log-level switch.

```bash
./corewar.py --league=race my_ship.s --log-level=10
```


WebServer
---------

First run :
```bash
./corewar.py --web-start
```

Then go to [http://localhost:8080](http://localhost:8080)

Ports and logs options can be specified from command line or corewar.cfg.
