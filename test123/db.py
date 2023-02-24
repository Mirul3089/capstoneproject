# import cx_Oracle

# connection = cx_Oracle.connect("test/test@127.0.0.1:1521/orcl")
# cursor = connection.cursor()
from pprint import pprint

def pretty_print(msg, indent=2):
    print()
    pprint(msg,indent=indent)
