# OpenPIV Toolkit
As the name suggests OpenPIV Toolkit is a collection of Python scripts and tools developed based on the OpenPIV project ([OpenPIV](https://github.com/OpenPIV/openpiv-python)) aimed at improving its PIV image processing work flow and also provide extra post-processing capabilities to reveal new insight into the data set. A GUI is also provided to ease the usage of the code. While currently not supporting some of the features available in OpenPIV (like 3D PIV), the features that are covered often include improvements:
-	Improvements in the main PIV processing, producing less outlier vectors and thus extracting more information from the flow field
-   Enhanced output format that contains vorticity, velocity magnitude, velocity fluctuations (Reynolds stresses) and turbulent kinetic energy. Average field parameters are also calculated
-	Improvements in the pre-process and validation process

Additional functionality includes:
-	Post-processing module to perform frequency analysis (FFT and STFT) for a specific point or globally giving spectral insight into the flow field
-	Post-processing module to perform modal analysis revealing information about the important flow structures. Two methods for POD analysis are available and Spectral-POD and DMD analysis are in the works
-	GUI framework (with all the settings exposed) for all the PIV processing and post-processing mentioned above that makes running calculations for large data sets a breeze
-	The GUI also contains a handy validation tab for quick flow visualization and adjustment of the validation parameters

## Installation
If you just want to use the library The easiest way is to use PyPI (https://pypi.org/project/OpenPIVToolkit/):

    pip install openpivtoolkit

### Build from source
But if you want to develop or modify the code it's best to have an editable installation of the package.
Download the package from [github](https://github.com/pouya-m/openpiv-toolkit) or clone using git

    git clone https://github.com/pouya-m/openpiv-toolkit.git

Then run the folowing command on the downloaded folder

    pip install -e <name of the folder>

## How to use
Usage is straightforward just run

    python -m openpivtk

on a commnd window to fire up the GUI. First, use the 'process' tab to process a small sample of your piv images, then use the
'validation' tab to import the results and adjust validation settings. Now, from the 'process' tab you can run the PIV analysis 
for the whole data set with your desired validation thresholds. Finally, for 'Frequency' and 'Modal Analysis' you can use their respective tabs.

<table>
  <tr><th colspan="2">some screenshots</th></tr>
  <tr><th>Validation Tab</th><th>Processing TB</th></tr>
  <tr>
    <td><img src="https://raw.githubusercontent.com/pouya-m/openpiv-toolkit/PIV-Code-Pouya/openpivtk/GUI/Screenshots/ValidationTab.PNG" title="Validation tab" /></td>
    <td><img src="https://raw.githubusercontent.com/pouya-m/openpiv-toolkit/PIV-Code-Pouya/openpivtk/GUI/Screenshots/ProcessTab.PNG" title="Process tab" /></td>
  </tr>
</table>

### Documentation
To learn the basics on specific parts of the code you can look into the examples/tutorials directory where some simple examples are provided.
Also some information is available from the OpenPIV library here: http://openpiv.readthedocs.org 

## Development Info
### Developer:
Pouya Mohtat (https://github.com/pouya-m, pouya.m67@gmail.com)

### Warning
OpenPIV Toolkit is in beta state which means it might contain some bugs and the API may change. Bugs are being fixed and new features are added regularly. Contribution to the code base is higly appretiated, Especially if it's towards adding new analysis capabilities.
The toolkit is written and tested on a windows environment while OpenPIV is developed on Linux. There are no confilicts that I'm aware of on windows but you can also run and test the code for yourself on linux.

### Copyright Statement
This program is published in the hope that it will be useful to the community. Special thanks goes to the original authors of the OpenPIV software for releasing their work open source, thus providing the basis for this project.

### License
> The GNU General Public License
>
> Copyright (c) 2020, Pouya Mohtat (https://github.com/pouya-m, pouya.m67@gmail.com)
>
> This program is free software: you can redistribute it and/or modify
> it under the terms of the GNU General Public License as published by
> the Free Software Foundation, either version 3 of the License, or
> (at your option) any later version.

> This program is distributed in the hope that it will be useful,
> but WITHOUT ANY WARRANTY without even the implied warranty of
> MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
> GNU General Public License for more details.

> You should receive a copy of the GNU General Public License
> along with this program.  If not, see <http://www.gnu.org/licenses/>.
