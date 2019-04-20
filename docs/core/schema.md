jason.schema
===

## Model

used to validate dictionaries

```python
from jason import schema

class MyModel(schema.Model):
    uuid = schema.Uuid()
    name = schema.String(min_length=3, default=10)
    email = schema.Email()
    
```

---

## Property:

```python
from jason import schema

prop = schema.Property()
prop.load("some thing")
```

---

#### Decorator

use any property as a decorator

```python
from jason import schema

@schema.Int(default=10)
def some_int(value):
    return value * 2

some_int.load(5)
# 10
```

---

#### Rules

```python
from jason import schema

prop = schema.AnyOf(schema.Int, schema.String)
prop.load("some thing")
```

#### `AnyOf`

validate against at least one property or rule in a defined list

parameters:

- __*rules__: 
list of rules or properties

---

#### Types


#### `Property`

base class for all properties, can be subclassed to create custom ones

parameters:

- __default__: 
a value or callable (no args) to be used if a value is `None` (default: `None`)

- __nullable__: 
if `False`, `None` values will cause `PropertyValidationError` to be raised (default `False`)

- __types__: 
a tuple of types that a value must be an instance or subclass of. if `None` any type will be accepted (default: `None`)


#### `Array`

validate a list or tuple

parameters:

- __prop__: (required) 
a property or rule to validate each item of the list against

- __default__: 
a value or callable (no args) to be used if a value is `None` (default: `None`)

- __nullable__: 
if `False`, `None` values will cause `PropertyValidationError` to be raised (default `False`)

- __min_length__: 
minimum length of the array, if `None` any length will be accepted (default: None)

- __max_length__: 
maximum length of the array, if `None` any length will be accepted (default: None)


#### `Nested`

create a property from a model

parameters:

- __model__: (required)
a subclass of `Model` to load properties from

- __default__: 
a value or callable (no args) to be used if a value is `None` (default: `None`)

- __nullable__: 
if `False`, `None` values will cause `PropertyValidationError` to be raised (default `False`)

- __strict__: 
if `True` any value found in the subject dict will cause `PropertyValidationError` to be raised.
if `None`, the value will be taken from the model.  (default: None)


#### `Inline`

create a nested property from a dictionary of property

parameters:

- __props__: (required)
a list or tuples or rules to make a nested object from

- __default__: 
a value or callable (no args) to be used if a value is `None` (default: `None`)

- __nullable__: 
if `False`, `None` values will cause `PropertyValidationError` to be raised (default `False`)


#### `Combine`

combine two or more models, inline properties or nested properties into one nested property

parameters:

- __*objects__: (required)
two or more objects to get properties from and merge into a single object. and duplicates will cause `PropertyValidationError` to be raised

- __default__: 
a value or callable (no args) to be used if a value is `None` (default: `None`)

- __nullable__: 
if `False`, `None` values will cause `PropertyValidationError` to be raised (default `False`)


#### `Bool`

validate a boolean

parameters:

- __allow_strings__: 
if `True` the property will attempt to create a bool from a string like "true" or "false" (default: `True`)

- __default__: 
a value or callable (no args) to be used if a value is `None` (default: `None`)

- __nullable__: 
if `False`, `None` values will cause `PropertyValidationError` to be raised (default `False`)


#### `Number`

validate an int or float

parameters:

- __allow_strings__: 
if `True` the property will attempt to create an int or float from a string like "12" or "12.3" (default: `True`)

- __min_value__: 
minimum value accepted, if `None` any value will be accepted (default: None)

- __max_value__: 
maximum value accepted, if `None` any value will be accepted (default: None)

- __default__: 
a value or callable (no args) to be used if a value is `None` (default: `None`)

- __nullable__: 
if `False`, `None` values will cause `PropertyValidationError` to be raised (default `False`)


#### `Int`

validate an int

parameters:

- __allow_strings__: 
if `True` the property will attempt to create an int or float from a string like "12" or "12.3" (default: `True`)

- __min_value__: 
minimum value accepted, if `None` any value will be accepted (default: None)

- __max_value__: 
maximum value accepted, if `None` any value will be accepted (default: None)

- __default__: 
a value or callable (no args) to be used if a value is `None` (default: `None`)

- __nullable__: 
if `False`, `None` values will cause `PropertyValidationError` to be raised (default `False`)


#### `Float`

validate a float. (ints will be converted to floats)

parameters:

- __allow_strings__: 
if `True` the property will attempt to create an int or float from a string like "12" or "12.3" (default: `True`)

- __min_value__: 
minimum value accepted, if `None` any value will be accepted (default: None)

- __max_value__: 
maximum value accepted, if `None` any value will be accepted (default: None)

- __default__: 
a value or callable (no args) to be used if a value is `None` (default: `None`)

- __nullable__: 
if `False`, `None` values will cause `PropertyValidationError` to be raised (default `False`)


#### `String`

validate a string

parameters:

- __default__: 
a value or callable (no args) to be used if a value is `None` (default: `None`)

- __nullable__: 
if `False`, `None` values will cause `PropertyValidationError` to be raised (default `False`)

- __min_length__: 
minimum length of the string, if `None` any length will be accepted (default: None)

- __max_length__: 
maximum length of the string, if `None` any length will be accepted (default: None)


#### `Regex`

validate a string against a regex matcher

parameters:

- __matcher__: (required)
either a regex string or compiled regex pattern to match a value against

- __default__: 
a value or callable (no args) to be used if a value is `None` (default: `None`)

- __nullable__: 
if `False`, `None` values will cause `PropertyValidationError` to be raised (default `False`)

- __min_length__: 
minimum length of the string, if `None` any length will be accepted (default: None)

- __max_length__: 
maximum length of the string, if `None` any length will be accepted (default: None)


#### `Uuid`

validate a string against the uuid4 standard

parameters:

 - None!


#### `Date`

validate a date or iso8601 date

parameters:

- __allow_strings__: 
if `True` the property will attempt to create an datetime from an iso8601 string like (default: `True`)

- __min_value__: 
minimum value accepted, if `None` any datetime will be accepted (default: None)

- __max_value__: 
maximum value accepted, if `None` any datetime will be accepted (default: None)

- __default__: 
a value or callable (no args) to be used if a value is `None` (default: `None`)

- __nullable__: 
if `False`, `None` values will cause `PropertyValidationError` to be raised (default `False`)


#### `Datetime`

validate a datetime or iso8601 datetime

parameters:

- __allow_strings__: 
if `True` the property will attempt to create an int or float from a string like "12" or "12.3" (default: `True`)

- __min_value__: 
minimum value accepted, if `None` any date will be accepted (default: None)

- __max_value__: 
maximum value accepted, if `None` any date will be accepted (default: None)

- __default__: 
a value or callable (no args) to be used if a value is `None` (default: `None`)

- __nullable__: 
if `False`, `None` values will cause `PropertyValidationError` to be raised (default `False`)


#### `Password`

validate a string against password rules

parameters:

- __uppercase__: 
if `True`, value must contain at least one upper case character, if `False`, value must not contain upper case characters (default: `None`)

- __numbers__: 
if `True`, value must contain at least one number, if `False`, value must not contain numberss (default: `None`)

- __symbols__: 
if `True`, value must contain at least one symbol, if `False`, value must not contain symbols (default: `None`)

- __min_score__: 
for each positive check a score count is incremented by 1, at the end `PropertyValidationError` if it is lower then min_score (default: `0`)

- __default__: 
a value or callable (no args) to be used if a value is `None` (default: `None`)

- __nullable__: 
if `False`, `None` values will cause `PropertyValidationError` to be raised (default `False`)


#### `Email`

validate a string against email rules

parameters:

- __default__: 
a value or callable (no args) to be used if a value is `None` (default: `None`)

- __nullable__: 
if `False`, `None` values will cause `PropertyValidationError` to be raised (default `False`)

---

#### Checks

#### `RangeCheck`

parameters:

- __min_value__: 
minimum value accepted, if `None` any value will be accepted (default: None)

- __max_value__: 
maximum value accepted, if `None` any value will be accepted (default: None)


#### `SizeRangeCheck`

parameters:

- __min_value__: 
minimum length accepted, if `None` any length will be accepted (default: None)

- __max_value__: 
maximum length accepted, if `None` any length will be accepted (default: None)


#### `DateTimeRangeCheck`

parameters:

- __min_value__: 
minimum value accepted, if `None` any value will be accepted (default: None)

- __max_value__: 
maximum value accepted, if `None` any value will be accepted (default: None)

---
