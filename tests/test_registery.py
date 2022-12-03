from registry.subclass_registry import SubclassRegistry
from registry.registry import Registry


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
