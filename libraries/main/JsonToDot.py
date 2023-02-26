# To convert json to dont notation or to extract the values from nested json or to get all keys from json-Gurdeep
import json
import sys


def getKeysvalue(val, key=""):
    if isinstance(val, dict):
        # if its root element dont append '.'
        if val and key=="":
            for k in val.keys():
                getKeysvalue(val[k], key + str(k))
        # if its a node append '.' before Key
        elif val:
            for k in val.keys():
                getKeysvalue(val[k], key +"."+ str(k))
        else:
            print("{} : {}".format(key,"{}"))
    elif isinstance(val, list):
        if val:
            for i,k in enumerate(val):
            #getKeysvalue(k, old + "." + str(i))
                getKeysvalue(k, key + str([i]))
        else:
            print("{} : []".format(key,"{}"))
    else:
        print("{} : {}".format(key,str(val)))


def getKeys(val, old=""):
    if isinstance(val, dict):
        if val and old == "":
            for k in val.keys():
                getKeys(val[k], old + str(k))
        elif val:
            for k in val.keys():
                getKeys(val[k], old + "." + str(k))
        else:
            print("{}".format(old))
    elif isinstance(val, list):
        if val:
            for i, k in enumerate(val):
                # getKeys(k, old + "." + str(i))
                getKeys(k, old + str([i]))
        else:
            print("{}".format(old))
    else:
        print("{}".format(old))

def getvalues(val, old=""):
    if isinstance(val, dict):
        if val and old=="":
            for k in val.keys():
                getvalues(val[k], old + str(k))
        elif val:
            for k in val.keys():
                getvalues(val[k], old +"."+ str(k))
        else:
          print("{}".format(old))
    elif isinstance(val, list):
        if val:
          for i,k in enumerate(val):
            getvalues(k, old + "." + str(i))
        else:
          print("{}".format(old))
    else:
        print("{}".format(str(val)))

json_values=[]
def getvaluestolist(val, old=""):
    if isinstance(val, dict):
        if val and old=="":
            for k in val.keys():
                getvaluestolist(val[k], old + str(k))
        elif val:
            for k in val.keys():
                getvaluestolist(val[k], old +"."+ str(k))
        else:
          print("{}".format(old))
    elif isinstance(val, list):
        if val:
          for i,k in enumerate(val):
            getvaluestolist(k, old + "." + str(i))
        else:
          print("{}".format(old))
    else:
        # print("{}".format(str(val)))
        json_values.append(val)
    return json_values

