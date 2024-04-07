# chatgpt-without-login

# Installing

```
pip install git+https://github.com/maguroshouta/chatgpt-without-login
```

# Example

```python
from freegpt import FreeGPT

gpt = FreeGPT()

for response in gpt.generate("What is a pen?"):
    print(response["message"]["content"]["parts"][0])
```
