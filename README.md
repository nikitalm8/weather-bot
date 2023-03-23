# Simple Weather Bot

## Requirements
- Python 3.9+
- Ubuntu 22+ / Windows 10

## Installation
### Clone repository
```bash
$ git clone
$ cd weather-bot
```

### Install Python 3.9+ and pip
```bash
$ sudo apt update && sudo apt upgrade
$ sudo apt install python3 python3-pip python3-venv
```

### Setup virtual environment and install dependencies
```bash
$ python3 -m venv .venv
$ source .venv/bin/activate
$ pip install -r requirements.txt
```

### Update `config.yaml` file

### Optional: install `asyncpg` for PostgreSQL support
```bash
$ pip install asyncpg
```

### Setup service
Specify `WorkingDirectory` in `weather-bot.service` file, then move service file to `/etc/systemd/system/` and reload daemon.
```bash
$ sudo cp weather-bot.service /etc/systemd/system/weather-bot.service
$ sudo systemctl enable weather-bot
$ sudo systemctl start weather-bot
```

## Usage
### If service is not set up:
```bash
$ cd weather-bot/
$ source .venv/bin/activate
$ cd bot
$ python3 main.py
```
### If service is set up:
```bash
$ sudo systemctl restart weather-bot
```

## Databases
Using default `SQLite3` database is not recommended for production. It's better to use `PostgreSQL` or `MySQL`. All parameters can be changed in `config.yaml` file.
