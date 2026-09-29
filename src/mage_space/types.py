"""Types for every request and response body, generated from the API's OpenAPI spec.

Annotate a config with its model's TypedDict to have a type checker check it:

```python
from mage_space.types import MangoConfig

config: MangoConfig = {"prompt": "A lighthouse at dawn", "aspect_ratio": "16:9"}
```
"""

from ._generated import *  # noqa: F403
from ._generated import __all__ as __all__
