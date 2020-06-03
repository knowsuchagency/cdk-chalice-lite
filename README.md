# cdk-chalice-lite

![](https://github.com/knowsuchagency/cdk-chalice-lite/workflows/black/badge.svg)
![](https://github.com/knowsuchagency/cdk-chalice-lite/workflows/unit%20tests/badge.svg)

Like `cdk-chalice`, but different.

# Usage

```python
from aws_cdk import core

from cdk_chalice_lite import Chalice


class MyStack(core.Stack):

    def __init__(self, scope, id, chalice_app_id, directory, **kwargs):
        super().__init__(scope, id, **kwargs)

        # note, the directory parameter can be either the root directory
        # of your chalice app i.e. where app.py is
        # or it can be the directory of the output of `chalice package`

        # if you choose the former, you can override the values in
        # .chalice/config.json via the stage_config and lambdas_config
        # parameters to the Chalice constructor

        self.chalice = Chalice(self, chalice_app_id, directory)




app = core.App()

my_stack = MyStack(app, 'my-stack')

app.synth()
```
