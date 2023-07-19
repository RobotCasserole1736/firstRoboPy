# Singletons

In code, we frequently want to indicate "there is only ever one of these".

This can be difficult in python, as it does not have a concept of "public" or "private" variables built into the language at runtime.

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

In this case, it indicates `_SomPrivateClass` shoudl not be instantiated outside the module both those classes are delcared in.

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

# Declare and instantiate a single instace of the class, saved in a variable named _inst

_inst = _MySingletonClass()

##################################
## Public API

#Provide a single public function to get the instance of the class

def getInstance():
    return _inst

```

Then, to use it in another file, first import the whole module, and give it a nice name

```py
import someFolder.mySingletonClass as MySingletonClass
```

Finally, use `getInstance` to access the instance, and call methods from it:

```py
print(MySingletonClass.getInstance().doAThing())
```

(the above should print `"42"`)
