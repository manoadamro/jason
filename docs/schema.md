jason.schema
===

## Model

```python
from jason import schema

class MyModel(schema.Model):
    uuid = schema.Uuid(min_length=3, default=10)
    name = schema.String(min_length=3, default=10)
    email = schema.Email()
    
```

---

## Property:

```python


```

#### Types

`Property`

`Array`

`Nested`

`Inline`

`Combine`

`Bool`

`Number`

`Int`

`Float`

`String`

`Regex`

`Uuid`

`Date`

`Datetime`

`Password`

`Email`


#### Checks

`RangeCheck`

`SizeRangeCheck`

`DateTimeRangeCheck`


#### Rules

`AnyOf`


#### Decorator

```python


```

---
