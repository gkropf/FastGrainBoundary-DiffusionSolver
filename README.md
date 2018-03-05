# Oxygen Isotope Diffusion Solver

This python code solves the Fast Grain Boundary (FGB) model for isotope diffusion. It provides a GUI interface for inputing all mineral parameters and provides several graphing options along with the option to export the model solution data to a .csv file. Search menus are provided for convenient referencing of diffusion parameters and fractionation factors.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine and walk you through an example set up of the model parameters.  

### Prerequisites

For this code to run you will need to have python 3 installed on your computer along with the following packages for it: tkinter, numpy, and matplotlib. A brief tutorial for installing python on various operating systems can be found on the wiki page: https://en.wikibooks.org/wiki/A_Beginner%27s_Python_Tutorial/Installing_Python.

### Installing

First download the files DiffusionSolver.py, FractionationFactorsR.csv, and ODiffusionR.csv. Make sure to place all files in the same folder. Additionally, you can download FGB_03S1T1_Params.txt as it contains an example of saved model parameters and will allow you to check that the code is running correctly.

Next we need to open a live terminal and navigate to the folder containing DiffusionSolver.py. On Mac and Linux this is done by simply typing in 'Terminal" into the application search bar. On windows search for 'cmd.' The command cd can be used to change your current folder and ls (Linux, Mac) or dir (Windows) can be used to list the available subfolders to navigate to. Once your in the folder containing DiffusionSolver.py run the code by using the commmand python3, as this will ensure the code is run with the appropriate version.

```
usr>: cd Documents
usr>/Documents: cd OxygenDiffusionSolver
usr>/Documents/OxygenDiffusionSolver: python3 DiffusionSolver.py
```
This should open the following pop-up:
![image](https://{photos.google.com/photo/AF1QipOJ8RPtTIL3a-4_saRoI4KnqHkNpb1IqYe03WPA})
![alt text](http://photos.google.com/photo/AF1QipOJ8RPtTIL3a-4_saRoI4KnqHkNpb1IqYe03WPA)






A step by step series of examples that tell you have to get a development env running

Say what the step will be

```
Give the example
```

And repeat

```
until finished
```

End with an example of getting some data out of the system or using it for a little demo

## Running the tests

Explain how to run the automated tests for this system

### Break down into end to end tests

Explain what these tests test and why

```
Give an example
```

### And coding style tests

Explain what these tests test and why

```
Give an example
```

## Deployment

Add additional notes about how to deploy this on a live system

## Built With

* [Dropwizard](http://www.dropwizard.io/1.0.2/docs/) - The web framework used
* [Maven](https://maven.apache.org/) - Dependency Management
* [ROME](https://rometools.github.io/rome/) - Used to generate RSS Feeds

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags). 

## Authors

* **Billie Thompson** - *Initial work* - [PurpleBooth](https://github.com/PurpleBooth)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hat tip to anyone who's code was used
* Inspiration
* etc
