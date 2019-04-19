jason.config
===

Attempts to load values from the environment.
Values can be passed into the load function to override environment variables.

```python
from jason.config import Config, props

# define a model
class MyConfig(Config):
    MY_INT = props.Int()
    MY_FLOAT = props.Float()
    MY_STRING = props.String()
    MY_BOOL = props.Bool()
    
# we can pass in MY_STRING (in upper or lower case) to override the environment variable
# MY_INT, MY_FLOAT, MY_BOOL will be taken from env
config = MyConfig.load(my_string="something")

print(config.MY_STRING)
# 'something'

print(config.MY_FLOAT)
# 12.3
    
```

more information about models and properties can be found [here](./schema.md)
