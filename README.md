# 🧮 Code rows counter
A simple, small utility for counting lines in selected text files

## 📖 Few examples
**Counting rows in [bottle.py](https://github.com/bottlepy/bottle)**
```
$ curl -fsSLO https://raw.githubusercontent.com/bottlepy/bottle/master/bottle.py
$ python crc.py -f bottle.py
> total lines: 4583
```
**Counting rows in [flask](https://github.com/pallets/flask)**
```
$ git clone https://github.com/pallets/flask.git
$ python crc.py -d flask/src/flask
> total lines: 6293
```
> Note: this command will process entries only inside `flask/src/flask` folder, but not in its subdirectories

**Counting rows in [linux kernel](https://github.com/torvalds/linux)**
```
$ git clone https://github.com/torvalds/linux.git
$ python crc.py -r -d linux
> total lines: 45419695
```