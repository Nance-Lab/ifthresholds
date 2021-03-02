# ifthresholds
## score ranking the standard threshold methods based on manually labeled images and images produced by various threshold
* The threshold ranking will be based on manually labelled images and images produced by applying the standard threshold methods. IfThreshold guides researchers on which threshold method is the best one for their images:
  * 3 Scoring methods:  count method, overlap method, region prop method which includes area, aspect ratio, and circularity comparison.
  * All the scores calculated with images from IGD study is written to a score ranking table and saved as a CSV file.
  * Terminal operation: input your own images and get ranking table and a visual comparison image.

#### Repository Structure
```
  |- README.md
  |- ifthresholds/
      |- __init__.py
      |- main.py
      |- score_method.py
      |- write_csv.py
      |- tests/
        |- __init__.py
        |- test_main.py
        |- __pycache__/
      |- data/
        |- ogd.tif
      |- __pycache__/
  |- doc/
      |- README.md
      |- functionality.md
      |- usage_cases.md
  |- examples/
      |- README.md
      |- workbook.ipynb
  |- setup.py
  |- .travis.yml
  |- environment.yml
  |- .pylintrc (for pylint conflict with opencv)
  |- .gitignore
  |- LICENSE

```

#### Activating the virtual environment
* Included within the root of the repository is a virtual environment
pre-suited to run `ifthresholds`
  * The virtual environment is located within environment.yml
  * To create the virtual environment from the .yml file:
  `conda env create -f environment.yml`
  * To activate the virtual environment:
  `conda activate flashing_lights_env`
  * The environment contains:
    * Python 3.7
    * numpy
    * scikit-image
    * scikit-learn

### Using flashing_lights
* ifThresholds can be executed through a jupyter notebook or terminal.
  * It is recommended to run the code within the included
  virtual environment to avoid dependency hell
  * Examples included in jupyter notebooks
  within `ifThresholds/examples/workbook.ipynb` that demonstrate how to use the code.
  To access these notebooks, enter the following into the command line:
  `jupyter notebook ifThresholds/examples/workbook.ipynb`

### Example Output

### Miscellaneous Notes
