# Historian

This is the python version of the Historian undo/redo manager. Based on the
tests it is stable.

## Concept

Historian works by registering inverse commands with it during the process of
executing a command. For example, in the process of incrementing a variable,
a decrement command would be registered with the Historian. When undoing the
increment command, the decrement command is called as it is the one registered
with the historian. Commands are stored chronologically so undo/redo operations
are all registered in the order that their inverses occur. See [usage](#usage)
for examples.

## Usage

0. Import:

```
from historian import Historian
```

1. Instantiate the Historian:

```
H = Historian()
```

2. Create commands that are inverses of each other and register the inverse
   operation of each with the Historian:

```
a = 0

def inc(n):
    global a
    a += n
    H.register(dec, n)

def dec(n):
    global a
    a -= n
    H.register(inc, n)
```

3. Do stuff:

```
# a starts at 0
inc(2) # a is 2
inc(2) # a is 4
dec(1) # a is 3
dec(2) # a is 1
```

4. Undo/redo stuff:

```
H.undo() # a is 3
H.undo(2) # a is 2
H.redo() # a is 4
# etc...
```

## Methods

### Constructor

A `limit` can be passed to the constructor to limit the size of the history. By
default `limit = 10`.

### `register(cmd, *args, **kwargs)`

Registers a (inverse) command with the Historian.

`*args` and `**kwargs` are the arguments to pass to the inverse command when it
is called on an undo/redo.

### `undo(n)`

Undoes last `n` commands. Passing `0` will undo all.

### `redo(n)`

Redoes last `n` commands. Passing `0` will redo all.

### `clear(kinds)`

Clears the history. `kinds` is a string or tuple specifying which history to
clear. Can be `"undo"`, `"redo"`, or `("undo","redo")`.

### `size(kind)`

Returns the size of the history. `kind` can be `"undo"` (the default) or
`"redo"`

## Mixin

As an added convenience there's a mixin class included which will add `undo()`
and `redo()` methods to another class and the `_undomgr` instance variable. It
is a simple wrapper around the `Historian` class. For example

```
from historian import HistorianMixin

class MyClass(HistorianMixin):
    def __init__(self):
        HistorianMixin.__init__(self)
        self.myvar = 0

    def inc(self, n):
        self.myvar += n
        self._undomgr.register(self.dec, n)

    def dec(self, n):
        self.myvar -= n
        self._undomgr.register(self.inc, n)
```

The above `MyClass` class can now call `undo()` and `redo()` to undo and redo
the most recent `inc()` and `dec()` calls.
