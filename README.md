# FigureSampleV4

__Scientific figure/trace data extraction software__ `<br>`
*VERSION: 0.1*
`<br>`

FigureSampelV4 allows to "sample" a given (scientific) data visualization aka. a "plot" and converts the image back to a dataset containing numbers.
I started this project as part of my work as a research assistant with version 1 and soon after 2.
Although version 2 was quite popular with my colleagues, version 3 was discontinued by my boss.
Therefore I started version 4 as a hobby project, I work on in my free time.
To avoid legal problems version 4 does not use any code used by previous version!

Right now it is my plan to progress further and surpass the work I did in the past.
At the moment there is no roadmap I follow, but I plan to soon write one and add it to this repository.
Further it is my plan to write a short user manual in LaTeX.

I am highly interested in feedback and open for new ideas and any advice you want to give me!
Feel free to use the scripts for your own work!


## Documentation

A propper documentation is planned with future versions.
The software consists of two essential parts, the sampling library and the gui script.
The gui script utilizes the tools provided in the library besides the python standart library to increase the usability.

For the xtraction of data every pixel inside a selected are called the _sampling frame_ is compared with a reference color.
This compairson is done by comparing RGBA vectors via a *probability metric*.
The smaller the result is the closer the color is to the reference.

Further the pixel with the smalles value across a x-collumn in the image will be selected if its value is within the given *metric boundaries*.
The onlything left now is to save the aquired data or to inspect them and improve the supplied parameters further.

## Roadmap

### 1.1 - (planned)

### 1.0 - (planned)

### 0.9 - (planned)

### 0.8 - (planned)

### 0.7 "The console" - (planned)

Developement of integrated "console" inside the gui.
Printing of information will be done there also the ability to type in cmd commands besides additional FSV4 commands are planned.

### 0.6 "Projects" - (planned)

Improvements of data savaing methods.
Utilizing config files to allow lodaing of projects and saving of entire projects with one button.
Loading of previous opened/saved projects.
Developement of project structure to avoid overwriting.

### 0.5 "Better sampling algorithms" - (planned)

Adding the ability to select between different sampling methods.
Planned sampling methods: "weightet mean", "largest delta", "multi pixel selection"

### 0.4 "Configuration files" - (planned)

Implementation of the ability to load json files als settings/configuration to potentially speed up human interactions and increase usability.

### 0.3 "QoL and bug fixes" - (planned)

With this version the projects surpases its predecessors.
Further the fixing of (potential) bugs and performance improvements are planned.
Data inspection abilities: reading single values directly in the software.

### 0.2 "Data coordinate transformation and interpolation" - (planned)

Adding the ability to transform the extracted trace coordinates from pixels to data coordinates.
When this is achieved the ability to interpolate the date will be added.
Further small patches of the gui are planned.

### 0.1 "Base functionalities" - (22.08.2023)

The fundamentals needed to load, save and process images and extract the pixel coordinates of a given tgrace.
With version 0.1 it is planed to make the software availbale on github.

## Developement Team

* JMW42 (Project Lead)
