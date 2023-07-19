# Singletons

In code, we frequently want to indicate "there is only ever one of these".

## Public & Private in Python.

Python does not have a concept of "public" or "private" variables built into the language.

However, a common convention is to prefix names with an underscore `_` to indicate the named thing is private.

For example:

```py
class SomeClass():
    def __init__(self):
        self.myPublicVariable = 5
        self._myPrivateVariable = 6
```

In this case, it indicates `_myPrivateVariable` should not be read or written outside `SomeClass`.

This can also be done to classes:

```py
class SomePublicClass():
    def __init__(self):
        self.myPublicVariable = 5
        self._myPrivateVariable = 6

class _SomePrivateClass():
    def __init__(self):
        self.myPublicVariable = 5
        self._myPrivateVariable = 6
```

In this case, it indicates `_SomPerivateClass` should not be instantiated outside the file both those classes are delcared in.

## How to make a Singleton

In general, a singleton pattern is accomplished by:

1. Declaring a private class, and putting all main functionality inside of it
2. Delcaring a single, private instance of that class, named `_inst`. `_inst` should start equal to `None`
3. Providing a public `getInstance()` function which creates and returns the instance if `_inst` is `None` (IE, on the first call), and simply returns the existing instance on subsequent calls.

## Making a Class into a Singleton

Along with the fact that python supports global variables (delcared outside any class structure), we can emulate a simple singleton class architecture like this:

In `mySingletonClass.py`:
```py

# Declare your class, naming it to start with an underscore _
class _MySingletonClass():
    def __init__(self):
        # TODO - class init

    # Example method - TODO delete or change this for your usage
    def doAThing(self):
        return 42

    # TODO - other class functions

# Declare the single instance of the class
_inst = None

##################################
## Public API

#Provide a single public function to instantiate the class if needed, 
# then get the instance of the class
def getInstance():
    global _inst
    if(_inst is None):
        _inst = _AutoSequencer()
    return _inst

```

## Using a Singleton

To use it in another file, first import the whole module, and give it a nice name.

```py
# Singleton Import Pattern
import someFolder.mySingletonClass as MySingletonClass

#For Reference- non-singleton import pattern
from someFolder.myNonSingletonClass import MyNonSingletonClass
```

Then, use `getInstance` to access the instance, and call methods from it:

```py
print(MySingletonClass.getInstance().doAThing())
```

(the above should print `"42"`)
