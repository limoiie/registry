# Registry

A base for these classes that propose to be used as a registry.

There is a common need when one's framework deals with many custom classes at
the same time, such as maintaining a build factory, one may want to register
these classes at their definition, probably binding with some meta information.
Here comes the `registry`, which provides convenient methods for registering
classes and querying meta information.

## Get started

Here is a simple example that class `Tool` acts as a registry, and registers
custom tool with a custom builder:

```python
import registry

class Toolbox(registry.Registry):
    def build(self, name):
        cls = self.query(name=name)
        builder = self.meta_of(cls)['builder']
        return builder()

@Toolbox.register(name='Hammer', builder=..., location='toolbox')
class Hammer:
    pass
```

In the above code, class `Toolbox` becomes a registry by deriving from 
`registry.Registry`. After that, `Toolbox` can collect other tools using the
annotator `Toolbox.register`.

## Usages

Registry provides two kinds of registry style.

### Registry in annotator style

One can register classes using the `register` annotator. In this style, the
registered class can keep itself clean.

```python
import registry

class Toolbox(registry.Registry):
    pass

@Toolbox.register(name='spanner', location='toolbox')
class ToolOne:
    pass
```

### Registry in derive style

If all the registered class should be the registry's subclasses, the registry
class can derive `registry.SubclassRegistry` so that all its subclasses can
be registered automatically.

```python
import registry

class Toolbox(registry.SubclassRegistry):
    def class_name(self):
        return self.__class__.__name__

class ToolOne(Toolbox, name='hammer', location='scaffold'):
    pass
```

### Query the class

One can query the registered class using partial meta info.

```python
import registry

class Toolbox(registry.Registry): ...

class ToolOne(Toolbox, name='hammer', location='scaffold'): ...

A = Toolbox.query(name='hammer')
B = Toolbox.query(name='hammer', location='scaffold')

assert A is ToolOne
assert B is ToolOne
```

### Query the meta info

One can also query the complete meta info.

```python
import registry

class Tool(registry.Registry): ...

class ToolOne(Tool, name='hammer', location='scaffold'): ...

A = Tool.query(name='hammer')
meta = Tool.meta_of(A)

assert meta['name'] == 'hammer'
assert meta['location'] == 'scaffold'
```