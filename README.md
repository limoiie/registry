# Registry

A base for these classes that propose to be used as a registry.

## Usages

```python
import src.registry.subclass_registry
from src import registry


class Tool(src.registry.subclass_registry.SubclassRegistry):
    def class_name(self):
        return self.__class__.__name__


class ToolOne(Tool, name='spanner', location='toolbox'):
    pass


class ToolTwo(Tool, name='hammer', location='scaffold'):
    pass


A = Tool.query(name='spanner')
B = Tool.query(name='hammer', location='scaffold')

assert A().class_name() == 'ToolOne'
assert B().class_name() == 'ToolTwo'

assert ToolOne is A
assert ToolTwo is B
```