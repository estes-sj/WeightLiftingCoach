""" List is a collection which is ordered and changeable. Allows duplicate members.

Tuple is a collection which is ordered and unchangeable. Allows duplicate members.

Set is a collection which is unordered, unchangeable*, and unindexed. No duplicate members.

Dictionary is a collection which is ordered** and changeable. No duplicate members. """

thisdict = {
  "brand": "Ford",
  "electric": False,
  "year": 1964,
  "colors": ["red", "white", "blue"]
}
print(thisdict)
print(len(thisdict))
print(type(thisdict))

x = thisdict["model"]
# or 
x = thisdict.get("model")

# return all keys
x = thisdict.keys()

# return all values
x = thisdict.values()

# change/add
thisdict["color"] = "white"

print(x) #after the change

# key value pairs
x = thisdict.items()

# check if key exists
if "model" in thisdict:
    print("Yes, 'model' is one of the keys in the thisdict dictionary")

# update
thisdict.update({"year": 2020})

# remove
thisdict.pop("model")

# removes last inserted
thisdict.popitem()

#The del keyword removes the item with the specified key name:
del thisdict["model"]

del thisdict
print(thisdict) #this will cause an error because "thisdict" no longer exists.

""" clear()	Removes all the elements from the dictionary
copy()	Returns a copy of the dictionary
fromkeys()	Returns a dictionary with the specified keys and value
get()	Returns the value of the specified key
items()	Returns a list containing a tuple for each key value pair
keys()	Returns a list containing the dictionary's keys
pop()	Removes the element with the specified key
popitem()	Removes the last inserted key-value pair
setdefault()	Returns the value of the specified key. If the key does not exist: insert the key, with the specified value
update()	Updates the dictionary with the specified key-value pairs
values()	Returns a list of all the values in the dictionary
 """