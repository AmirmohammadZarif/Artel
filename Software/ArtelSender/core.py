'''
Copyright 2021 Amirmohammad Zarif
Created @ 13 Jul 2021
'''
import DeltaRobotKinemtics
from collections import namedtuple

class control:
    pass 

class robot:
    def __init__(self):
        self.current_speed = 0

        self.theta1 = 0
        self.theta2 = 0
        self.theta3 = 0

        self.x = 0
        self.y = 0
        self.z = 0

        self.kinematic = DeltaRobotKinemtics.kinemtics()
        
    class Properties:
        def __init_subclass__(cls):
            cls._property_list = [attr for attr in vars(cls).values()
                                if isinstance(attr, Property)]
            
            names = [prop.name for prop in cls._property_list]
            properties_type = namedtuple(cls.__name__ + "Properties", names)
            cls._properties_type = properties_type

        def __init__(self):
            property_list = self.__class__._property_list
            properties_type = self.__class__._properties_type
            properties = [Property.Instance(prop) for prop in property_list]
            self._properties = properties_type._make(properties)

        def _get_property(self, name):
            return getattr(self._properties, name)

        @property
        def properties(self):
            return self._properties

    class Property:
        __slots__ = ('name', 'default', 'units', '__doc__',)

        def __init__(self, default, units, doc):
            self.default = default
            self.units = units
            self.__doc__ = doc

        def __set_name__(self, owner, name):
            self.name = name

        def __get__(self, instance, owner=None):
            if instance is None:
                return self
            
            prop = instance._get_property(self.name)
            return prop.value

        def __set__(self, instance, value):
            prop = instance._get_property(self.name)
            prop.value = value

        class Instance:

            __slots__ = ('value', '_fast', '_property')

            def __init__(self, prop):
                self._property = prop
                self.value = prop.default
                self._fast = True

            @property
            def name(self):
                return self._property.name

            @property
            def params(self):
                return self._property.params

            @property
            def fast(self):
                return self._fast

            @fast.setter
            def fast(self, value):
                self._fast = bool(value)

            def __repr__(self):
                return f"Prop[{self.name} {self.value} {self.params} {self.fast}]"

    class pos:
        x = 0
        y = 0
        z = -200
        
    def getCurrentPosition(self):
        return self.pos()

if __name__ == "__main__":
    robot = robot()
    # print(cont.getCurrentPosition().head.x)
    # print(robot.getCurrentPosition().x)
    robot.Properties.fast = True
    print(robot.Properties.fast)