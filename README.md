# __Software Seminar__
ZenUML & PyDriller

## Project Desc.
### Research Question:
In the field of chess games in JAVA, how the amount of commits is expressed in the size of the move method, as it is reflected
In the sequence diagram?

Size = the complexity of the sequence diagram, i.e. the amount of messages in the diagram.
### Hypothesis:
We hypothesize that there is a correlation between the number of commits and the size of the sequence diagram. That is, the more commits there are, the more complex the method will be.

In order to answer our research question we had to integregate both tools (Pydriller & ZenUML).

## Technology 
- ZenUML
- PyDriller
- OpenCV
- PyAutoGUI
- Google Colaboratory
- Pandas
- Python
  
## Requirements.
invetigate our research question by the help of these tools.

## WorkFolw.
The input we enter at the beginning of the process into the PyDriller tool will be a list of urls of GitHub folders of projects dealing with needlework and written in the java language. 
Using PyDriller we will extract from each of the projects the methods named move and the number of commits made on the file in which the method appears, and save in a csv file.
We will filter the csv file so that we remain with the longest move method in each project (in projects where there is more than one move method). In addition, in order to receive the highest quality projects, we chose in the initial screening to sort the projects in descending order according to the number of Stars for that project.
After that, we will translate, with the help of a translator we developed, the methods from the java language into the syntax of the ZenUML tool.
We will save the translation in the csv file. In the next step, with the help of PyAutoGUI (a Python package that allows you to imitate keyboard and mouse movements),
we will copy each of the translated methods to ZenUML and save the sequence diagram we received as an image in a png file.
In the final part of the process, we will use a Python code that we developed with the help of the OpenCV library,
in order to count the amount of arrows (that is, the number of messages) that appears in each of the sequence diagrams that we saved as png files. We will also save the amount of messages in the csv file next to the details of the corresponding method.
The final output of the process will be a csv file in which a link to the folder on GitHub appears, the name of the method, the method in java, the amount of commits, the translated method and the amount of messages in the sequence diagram.
