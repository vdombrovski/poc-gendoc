Gendoc - an experimental inline doc generator
===

What is this?
---

This project is a PoC for parsing inline documentation. For now it only works with .c files and is quite limited.

How to use
---

Get inside the project folder

```sh
$ virtualenv2 env
$ pip install -r requirements.txt
$ ./gendoc.py ./example
$ cat ./result.md
```
