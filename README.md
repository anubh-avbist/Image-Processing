# Image Processing Command-Line Interface
A simple CLI written in python to assist in rapidly developing and testing different image-processing filters/effects. Currently includes gradient-edge detection filter and textify effect as example Effects.

## Usage
Run ```python impro.py -h ``` and ```python impro.py -l``` for help and list of filters. You can append as many filters using ```-f``` to apply the filters in order. Example usage:
```console
$ impro.py process path/to/image/picture.png output/directory -f textify 'monospace' 6 6 -f edge
```

## Project Structure
The CLI is built using argparse in the impro.py file. The image effects are all applied with PyGame Surfaces, and can be found in the effects folder. The effect.py file contains the Abstract Base Class for building the image effects/filters that can be added to the project.

### Creating Your Own Effect/Filter
1. Create a python script, my_effect.py, including a class that inherits from Effect abstract base class.
2. Write the required apply method with this signature:
```python
class MyEffect(Effect):
  @staticmethod
  def apply(image: pygame.Surface, *parameters) -> pygame.Surface:
    # Implementation
```
3. Update impro.py to include the new MyEffect class in EFFECTS:
```python
from effects import edge, textify, my_effect

EFFECTS = {
    "edge": edge.Edge,
    "textify": textify.Textify
    "effect_name": my_effect.MyEffect # Include a reference to the class
}
  
```
4. Run your new effect:

```terminal
$ impro.py process path/to/image/picture.png output/directory -f effect_name <parameters>
```
