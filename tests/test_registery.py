import dataclasses

from registry.registry import Registry
from registry.subclass_registry import SubclassRegistry


class TestRegistry:
    class FakeTool(Registry):
        pass

    @FakeTool.register(return_annotated=True, name='one', limit=9)
    class ToolOne:
        def name(self):
            return self.__class__.__name__

    @FakeTool.register(return_annotated=False, default_return=None, name='two')
    class ToolTwo:
        def name(self):
            return self.__class__.__name__

    def test_query(self):
        ToolOne = TestRegistry.FakeTool.query(name='one')
        ToolTwo = TestRegistry.FakeTool.query(name='two')

        assert ToolOne is TestRegistry.ToolOne
        assert TestRegistry.ToolTwo is None

        assert ToolOne().name() == 'ToolOne'
        assert ToolTwo().name() == 'ToolTwo'

    def test_meta(self):
        ToolOne = TestRegistry.FakeTool.query(name='one')
        assert TestRegistry.FakeTool.meta_of(ToolOne) == \
               dict(name='one', limit=9)


class TestRegistryWithMetaType:
    @dataclasses.dataclass
    class Meta:
        name: str = ''
        limit: int = 0

    class FakeTool(Registry[Meta]):
        pass

    @FakeTool.register(return_annotated=True, name='one', limit=9)
    class ToolOne:
        def name(self):
            return self.__class__.__name__

    @FakeTool.register(return_annotated=False, name='two')
    class ToolTwo:
        def name(self):
            return self.__class__.__name__

    def test_query(self):
        FakeTool = TestRegistryWithMetaType.FakeTool

        ToolOne = FakeTool.query(name='one')
        ToolTwo = FakeTool.query(fn=lambda m: m.name == 'two')

        assert ToolOne is TestRegistryWithMetaType.ToolOne
        assert TestRegistryWithMetaType.ToolTwo is None

        assert ToolOne().name() == 'ToolOne'
        assert ToolTwo().name() == 'ToolTwo'

    def test_meta(self):
        FakeTool = TestRegistryWithMetaType.FakeTool

        ToolOne = FakeTool.query(name='one')
        meta = FakeTool.meta_of(ToolOne)
        expected_meta = TestRegistryWithMetaType.Meta(name='one', limit=9)
        assert meta == expected_meta


class TestSubclassRegistry:
    class FakeTool(SubclassRegistry):
        @classmethod
        def name(cls):
            return cls.__name__

    class ToolOne(FakeTool, name='one', limit=9):
        pass

    class ToolTwo(FakeTool, name='two'):
        pass

    def test_query(self):
        ToolOne = TestSubclassRegistry.FakeTool.query(name='one')
        ToolTwo = TestSubclassRegistry.FakeTool.query(name='two')

        assert ToolOne is TestSubclassRegistry.ToolOne
        assert ToolTwo is TestSubclassRegistry.ToolTwo

        assert ToolOne().name() == 'ToolOne'
        assert ToolTwo().name() == 'ToolTwo'

    def test_meta(self):
        ToolOne = TestSubclassRegistry.FakeTool.query(name='one')
        assert TestSubclassRegistry.FakeTool.meta_of(ToolOne) == \
               dict(name='one', limit=9)


class TestSubclassRegistryWithMetaType:
    @dataclasses.dataclass
    class Meta:
        name: str = ''
        limit: int = 0

    class FakeTool(SubclassRegistry[Meta]):
        @classmethod
        def name(cls):
            return cls.__name__

    class ToolOne(FakeTool, name='one', limit=9):
        pass

    class ToolTwo(FakeTool, name='two'):
        pass

    def test_query(self):
        FakeTool = TestSubclassRegistryWithMetaType.FakeTool

        ToolOne = FakeTool.query(name='one')
        ToolTwo = FakeTool.query(fn=lambda m: m.name == 'two')

        assert ToolOne is TestSubclassRegistryWithMetaType.ToolOne
        assert ToolTwo is TestSubclassRegistryWithMetaType.ToolTwo

        assert ToolOne().name() == 'ToolOne'
        assert ToolTwo().name() == 'ToolTwo'

    def test_meta(self):
        FakeTool = TestSubclassRegistryWithMetaType.FakeTool

        ToolTwo = FakeTool.query(name='two')
        meta = FakeTool.meta_of(ToolTwo)
        expected_meta = TestSubclassRegistryWithMetaType.Meta(name='two')
        assert meta == expected_meta


class TestMultiLvlSubclassRegistry:
    class FakeTool(SubclassRegistry):
        @classmethod
        def name(cls):
            return cls.__name__

    class ToolOne(FakeTool, name='one', limit=9):
        pass

    class ToolTwo(FakeTool, name='two'):
        pass

    class ToolThree(ToolOne, name='three', nested=True):
        pass

    class ToolFour(ToolThree, name='four', nested=True):
        pass

    def test_query(self):
        ToolOne = TestMultiLvlSubclassRegistry.FakeTool.query(name='one')
        ToolTwo = TestMultiLvlSubclassRegistry.FakeTool.query(name='two')
        ToolThree = TestMultiLvlSubclassRegistry.FakeTool.query(name='three')
        ToolFour = TestMultiLvlSubclassRegistry.FakeTool.query(name='four')

        assert ToolOne is TestMultiLvlSubclassRegistry.ToolOne
        assert ToolTwo is TestMultiLvlSubclassRegistry.ToolTwo
        assert ToolThree is TestMultiLvlSubclassRegistry.ToolThree
        assert ToolFour is TestMultiLvlSubclassRegistry.ToolFour

        assert ToolOne().name() == 'ToolOne'
        assert ToolTwo().name() == 'ToolTwo'
        assert ToolThree().name() == 'ToolThree'
        assert ToolFour().name() == 'ToolFour'

        meta = TestMultiLvlSubclassRegistry.FakeTool.meta_of(ToolFour)
        assert meta['nested'] == True
