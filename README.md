# OpenPIV Toolkit

As the name suggests OpenPIV Toolkit is a collection of Python scripts and tools developed based on the OpenPIV project (link) aimed at improving its’ PIV image processing and also provide extra post-processing capabilities to reveal new insight into the data set. A GUI is also provided to ease the usage of the code. While currently not supporting some of the features available in OpenPIV (like 3D PIV), the features that are covered often include improvements:
-	Improvements in the main PIV processing, producing less outlier vectors and thus extracting more information from the flow field
-   Enhanced output format that contains vorticity, velocity magnitude, velocity fluctuations (Reynolds stresses) and turbulent kinetic energy. Average field parameters are also calculated
-	Small improvements in the pre-process and validation process

Additional functionality includes:
-	Post-processing module to perform frequency analysis (FFT and STFT) for a specific point or globally giving spectral insight into the flow field
-	Post-processing module to perform modal analysis revealing information about the important flow structures. Two methods for POD analysis are available and Spectral-POD and DMD analysis are in the works
-	GUI framework (with all the settings exposed) for all the PIV processing and post-processing mentioned above that enables running calculations for large data sets contained in different folders
-	The GUI also contains a handy validation tab for quick flow visualization and adjustment of the validation parameters


## Warning
OpenPIV Toolkit is in beta state meaning it still might contain some bugs and the API may change. Bugs are being fixed and new features are added regularly. Contribution to the code base is higly appretiated, Especially if it's towards adding new features and capabilities.
The toolkit is written and tested on a windows environment while OpenPIV is developed on Linux. There are no confilicts that I'm aware of on windows and you can run and test the code for yourself on linux.


## Installing

Use PyPI: <https://pypi.python.org/pypi/OpenPIV>:

    pip install cython numpy 
    pip install openpiv --pre

`--pre` because sometimes we push pre-releases

## Or `conda` 

    conda install -c conda-forge openpiv
    
    
### To build from source

Download the package from the Github: https://github.com/OpenPIV/openpiv-python/archive/master.zip
or clone using git

    git clone https://github.com/OpenPIV/openpiv-python.git

Using distutils create a local (in the same directory) compilation of the Cython files:

    python setup.py build_ext --inplace

Or for the global installation, use:

    python setup.py install 


### Latest developments

Latest developments go into @alexlib repository <https://github.com/alexlib/openpiv-python>

## Documentation

The OpenPIV documentation is available on the project web page at <http://openpiv.readthedocs.org>

## Demo notebooks 

1. [Tutorial Notebook 1](https://nbviewer.jupyter.org/github/OpenPIV/openpiv-python/blob/master/openpiv/examples/notebooks/tutorial1.ipynb)
2. [Tutorial notebook 2](https://nbviewer.jupyter.org/github/OpenPIV/openpiv-python/blob/master/openpiv/examples/notebooks/tutorial2.ipynb)
3. [Dynamic masking tutorial](https://nbviewer.jupyter.org/github/OpenPIV/openpiv-python/blob/master/openpiv/examples/notebooks/masking_tutorial.ipynb)
4. [Multipass tutorial with WiDiM](https://nbviewer.jupyter.org/github/OpenPIV/openpiv-python/blob/master/openpiv/examples/notebooks/tutorial_multipass.ipynb)
5. [Multipass with Windows Deformation](https://nbviewer.jupyter.org/github/OpenPIV/openpiv-python/blob/master/openpiv/examples/notebooks/window_deformation_comparison.ipynb)
6. [Multiple sets in one notebook](https://nbviewer.jupyter.org/github/OpenPIV/openpiv-python/blob/master/openpiv/examples/notebooks/all_test_cases_sample.ipynb)


## Contributors

1. [Alex Liberzon](http://github.com/alexlib)
2. [Roi Gurka](http://github.com/roigurka)
3. [Zachary J. Taylor](http://github.com/zjtaylor)
4. [David Lasagna](http://github.com/gasagna)
5. [Mathias Aubert](http://github.com/MathiasAubert)
6. [Pete Bachant](http://github.com/petebachant)
7. [Cameron Dallas](http://github.com/CameronDallas5000)
8. [Cecyl Curry](http://github.com/leycec)
9. [Theo Käufer](http://github.com/TKaeufer) 


Copyright statement: `smoothn.py` is a Python version of `smoothn.m` originally created by D. Garcia [https://de.mathworks.com/matlabcentral/fileexchange/25634-smoothn], written by Prof. Lewis and available on Github [https://github.com/profLewis/geogg122/blob/master/Chapter5_Interpolation/python/smoothn.py]. We include a version of it in the `openpiv` folder for convenience and preservation. We are thankful to the original authors for releasing their work as an open source. OpenPIV license does not relate to this code. Please communicate with the authors regarding their license. 

## How to cite this work
OpenPIV/openpiv-python:  http://doi.org/10.5281/zenodo.3566451


