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

TODO

---

## Custom Properties

TODO

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

TODO

### Bool

TODO

### Choice

TODO

### Compound

TODO

### Date

TODO

### Datetime

TODO

### Email

TODO

### Float

TODO

### Inline

TODO

### Int

TODO

### Nested

TODO

### Number

TODO

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