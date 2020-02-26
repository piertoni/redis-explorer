# Redis Explorer

A simple software with minimal requirements to navigate inside a `redis` database.

It uses tkinter GUI as it is part of python standard library.

## Installation

Type `pip install git+https://github.com/piertoni/redis-explorer.git`

## Getting Started

After the installation you can launch the software with:

`redis-explorer`

This will try to connect with default arguments:

* host ='0.0.0.0'
* port = 6379
* database = 0
* password = No password

Or you can provide them using the shell like:

`redis-explorer --host myhost --port 25001 --db 1 --pw mysecret`
