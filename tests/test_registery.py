import dataclasses
import random

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

    def test_override_make_meta(self):
        fake_arg = random.randint(10, 20)
        fake_increase = random.randint(20, 30)

        class ToolOverrideMakeMeta(Registry):
            # noinspection PyMethodOverriding
            @classmethod
            def make_meta(cls, registered, *, arg: int, name: str):
                assert registered.__name__ == name
                return {
                    'arg': arg + fake_increase
                }

        @ToolOverrideMakeMeta.register(arg=fake_arg, name='SubTool')
        class SubTool:
            pass

        meta = ToolOverrideMakeMeta.meta_of(SubTool)
        assert meta['arg'] == fake_arg + fake_increase

    def test_override_check_meta(self):
        fake_default_meta = dict(name='anonymous')

        class ToolOverrideMakeMeta(Registry):
            @classmethod
            def check_meta(cls, meta: dict):
                return meta or fake_default_meta

        @ToolOverrideMakeMeta.register()
        class SubTool:
            pass

        registered_meta = ToolOverrideMakeMeta.meta_of(SubTool)
        assert registered_meta is fake_default_meta


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
        expected_meta = dict(name='one', limit=9)

        # query meta by BaseClass.meta_of
        meta = TestSubclassRegistry.FakeTool.meta_of(ToolOne)
        assert expected_meta == meta

        # query meta by DerivedClass.meta
        meta = ToolOne.meta()
        assert expected_meta == meta

    def test_override_make_meta(self):
        fake_arg = random.randint(10, 20)
        fake_increase = random.randint(20, 30)

        class ToolOverrideMakeMeta(SubclassRegistry):
            # noinspection PyMethodOverriding
            @classmethod
            def make_meta(cls, registered, *, arg: int, name: str):
                assert registered.__name__ == name
                return {
                    'arg': arg + fake_increase
                }

        class SubTool(ToolOverrideMakeMeta, arg=fake_arg,
                      name='SubTool'):
            pass

        meta = ToolOverrideMakeMeta.meta_of(SubTool)
        assert meta['arg'] == fake_arg + fake_increase

    def test_override_check_meta(self):
        fake_default_meta = dict(name='anonymous')

        class ToolOverrideMakeMeta(SubclassRegistry):
            @classmethod
            def check_meta(cls, meta: dict):
                return meta or fake_default_meta

        class SubTool(ToolOverrideMakeMeta):
            pass

        registered_meta = ToolOverrideMakeMeta.meta_of(SubTool)
        assert registered_meta is fake_default_meta


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

        # query meta by BaseClass.meta_of
        meta = FakeTool.meta_of(ToolTwo)
        expected_meta = TestSubclassRegistryWithMetaType.Meta(name='two')
        assert meta == expected_meta

        # query meta by DerivedClass.meta
        meta = ToolTwo.meta()
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
