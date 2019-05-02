# jason.props

[back to jason docs](./jason.md)

---

### Table Of Contents:

- [Models](#Models)
- [Config Objects](#Config-Objects)
- [Property Decorator](#Property-Decorator)
- [Custom Properties](#Custom-Properties)
- [Property Types](#Property-Types)
- [Property Rules](#Property-Rules)

---

## Models

Models are used to define a structure.

```python
from jason import props


class MySchema(props.Model):
    x = props.Int()
    y = props.String()

```

Models are strict by default. To disable this and allow extra keys to be ignored during validation:

```python
from jason import props


class MySchema(props.Model):
    __strict__ = False
    x = props.Int()
    y = props.String()
```

---

## Config Objects

`ConfigObject` is an extension of [Models](#Models).
Fields are defined, just as with the model (usually upper case).

Fields defined as environment variables will use the environment variables value (unless overridden in constructor),
If no environment variable is defined, the default is used. 
If no default is used and the value is not nullable, an error is raised

values can be defined in the constructor, they can be passes in any case and will be converted to upper case.

```python
from jason import props

class MyConfig(props.ConfigObject):
    SOME_VARIABLE = props.String(default="something")
    ANOTHER_VARIABLE = props.Int()
    NULLABLE_VARIABLE = props.Int(nullable=True)


config = MyConfig.load(another_variable=123)

print(config.SOME_VARIABLE)
# 'something'

print(config.ANOTHER_VARIABLE)
# 123

print(config.NULLABLE_VARIABLE)
# None
```

variables can be accessed either using dot notation: `config.MY_VARIABLE`
or with an indexer `config["MY_VARIABLE:"]`

---

## Property Decorator

All properties can be used as a decorator
this allows you to extend the validation.

```python

```

---

## Custom Properties

You can create your own property types by sub-classing `Property`

```python
from jason import props

class MyProperty(props.Prfrom jason import props

class MySchema(props.Model):

    my_prop = props.Int(default=15, min_value=10, max_value=20)
    
    @props.Int(default=15, min_value=10, max_value=20)
    def my_prop(self, value):
        return value * 2operty):

    def _validate(self, value):
        ...  # custom validation.

```

---

## Property Types

All properties are sub classes of `Property`.

- [Array](#Array)
- [Bool](#Bool)
- [Choice](#Choice)
- [Compound](#Compound)
- [Date](#Date)
- [Datetime](#Datetime)
- [Email](#Email)
- [Float](#Float)
- [Inline](#Inline)
- [Int](#Int)
- [Nested](#Nested)
- [Number](#Number)
- [Password](#Password)
- [Regex](#Regex)
- [String](#String)
- [Uuid](#Uuid)

### Array

A property to validate an array against.

```python
from jason import props

arr = props.Array(
    prop=props.Int(min_value=1, max_value=10),
    min_length=1,
    max_length=10,
)
```

##### `prop` (required)

An instance of property to validate each array item against.

##### `min_length` (default None)

The minimum length of the array. Can be a callable returning a value

##### `max_length` (default None)

The maximum length of the array. Can be a callable returning a value

##### `nullable` (default False)

Will `None` be accepted in place of an array?

##### `default` (default None)

The default value to use if the array is `None`.  Can be a callable returning a value


### Bool

A property to validate a boolean against.
by default, booleans can be loaded from strings like `"true""` or `"false"`.
To disable this, use `allow_strings` to false in property constructor

```python
from jason import props

boolean = props.Bool()
```

##### `nullable` (default False)

Will `None` be accepted in place of boolean?

##### `default` (default None)

The default value to use if the boolean is `None`.  Can be a callable returning a value

##### `allow_strings` (default True)

If `True`, string values `true` and `false` will be accepted and converted to the relevant bool value.

### Choice

A property containing a collection of values.
When validating, the value must be one of these values (or `None` if nullable)

```python
from jason import props

boolean = props.Choice(choices=[1,2,3,4,5], nullable=True)
```

##### `choices` (required)

A list or tuple of values that any validating value must be one of.

##### `nullable` (default False)

Will `None` be accepted in place of value?

##### `default` (default None)

The default to use if the value is `None`.  Can be a callable returning a value

### Compound

merges multiple objects into one.

```python
from jason import props

class ModelA(props.Model):
    a = props.Int()
    b = props.Int()

class ModeB(props.Model):
    c = props.Int()
    d = props.Int()

prop = props.Compound(ModelA, ModeB)
```

##### `*objects` (required)

instances of `Model`, `Inline`, `Nested`, `Dict[str, Property]` or `Compound` to merge into one.

##### `nullable` (default False)

Will `None` be accepted in place of value?

##### `default` (default None)

The default to use if the value is `None`.  Can be a callable returning a value

### Date

A property to validate a date against.

```python
from jason import props

d = props.Date(min_value="1970-01-01")
```

##### `min_value` (default None)

minimum date, can also be iso8601 string or callable returning date

##### `max_value` (default None)

maximum date, can also be iso8601 string or callable returning date

##### `nullable` (default False)

Will `None` be accepted in place of value?

##### `default` (default None)

The default to use if the value is `None`.  Can be a callable returning a value

##### `allow_strings` (default True)

allow date to be loaded from iso8601 strings

### Datetime

A property to validate a datetime against.

```python
from jason import props

d = props.Datetime(min_value="1970-01-01T00:00:00.000Z")
```

##### `min_value` (default None)

minimum datetime, can also be iso8601 string or callable returning datetime

##### `max_value` (default None)

maximum datetime, can also be iso8601 string or callable returning datetime

##### `nullable` (default False)

Will `None` be accepted in place of value?

##### `default` (default None)

The default to use if the value is `None`.  Can be a callable returning a value

##### `allow_strings` (default True)

allow datetime to be loaded from iso8601 strings

### Email

validates strings against the following regex:
```regexp
^[^@]+@[^@]+\\.[^@]+$
```

```python
from jason import props

d = props.Email()
```

##### `nullable` (default False)

Will `None` be accepted in place of value?

##### `default` (default None)

The default to use if the value is `None`.  Can be a callable returning a value

### Float

A property to validate a float value.
It will accept `int` values, but will convert them to float. eg `12` -> `12.0`
by default, floats can be loaded from strings like `"12""` or `"12.0"`.
To disable this, use `allow_strings` to false in property constructor

```python
from jason import props

d = props.Float()
```

##### `min_value` (default None)

minimum date, can also be a callable returning value

##### `max_value` (default None)

maximum date, can also be a callable returning value

##### `nullable` (default False)

Will `None` be accepted in place of value?

##### `default` (default None)

The default to use if the value is `None`.  Can be a callable returning a value

##### `allow_strings` (default True)

allow datetime to be loaded from strings such as `"12.0""`

### Inline

allows the definition of models using a simple constructor.

```python
from jason import props

d = props.Inline(props=dict(x=props.Int(), y=props.Int()))

```

##### `nullable` (default False)

Will `None` be accepted in place of value?

##### `default` (default None)

The default to use if the value is `None`.  Can be a callable returning a value

### Int

A property to validate a int value.
It will not accept `float` values.
by default, ints can be loaded from strings like `"12""`.
To disable this, use `allow_strings` to false in property constructor

```python
from jason import props

d = props.Int()
```

##### `min_value` (default None)

minimum date, can also be a callable returning value

##### `max_value` (default None)

maximum date, can also be a callable returning value

##### `nullable` (default False)

Will `None` be accepted in place of value?

##### `default` (default None)

The default to use if the value is `None`.  Can be a callable returning a value

##### `allow_strings` (default True)

allow datetime to be loaded from strings such as `"12""`

##### `strict` (default True)

should the resulting model be `strict`?

### Nested

Allows the nesting of models.

```python
from jason import props

class MyNestedModel(props.Model):
    ...

class MySchema(props.Model):
    nested = props.Nested(MyNestedModel, default=None)
    other_nested = props.Nested(props.Inline(props=dict(x=props.Int(), y=props.Int())))   
```

##### `default` (default None)

The default to use if the value is `None`.  Can be a callable returning a value

##### `allow_strings` (default True)

allow datetime to be loaded from strings such as `"12""`

##### `strict` (default True)

should the resulting model be `strict`?

### Number

A property to validate a numeric value.
It will accept `int` or `float` values.
by default, numbers can be loaded from strings like `"12""` or `"12.0"`.
To disable this, use `allow_strings` to false in property constructor

```python
from jason import props

d = props.Number()
```

##### `min_value` (default None)

minimum date, can also be a callable returning value

##### `max_value` (default None)

maximum date, can also be a callable returning value

##### `nullable` (default False)

Will `None` be accepted in place of value?

##### `default` (default None)

The default to use if the value is `None`.  Can be a callable returning a value

##### `allow_strings` (default True)

allow datetime to be loaded from strings such as `"12.0""`

### Password

TODO

### Regex

TODO

### String

TODO

### Uuid

TODO

---

## Property Rules

- [AnyOf](#AnyOf)

### AnyOf

TODO

---