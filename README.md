# ZenUMLAuto README

This script contains the `ZenUMLAuto` class, which provides functionalities to interact with the ZenUML desktop Windows application, convert Java functions into ZenUML syntax, and detect certain templates within an image.

## Dependencies
- `pyautogui`
- `time`
- `cv2` from `opencv-python`
- `numpy`
- `re`
- `pandas`

## Class ZenUMLAuto

### Methods:
#### 1. `__init__(self)`
Initializes an instance of ZenUMLAuto. Keeps track of a counter to count iterations.

#### 2. `automate_code(code: str, file_name: str)`
Automate ZenUML desktop Windows app using `pyautogui` to input the code and then capture a screenshot of the resultant diagram.

#### 3. `detection(img_file_name: str) -> int`
Detect specific template images (`template1.jpg` and `template2.jpg`) within the given image and returns the total count of detected templates.

#### 4. `convert(function: str) -> str`
Converts a given Java function into ZenUML Syntax and returns the ZenUML formatted function.

#### 5. `convertor_run(methods_file_name: str)`
Converts Java methods provided in a CSV file into ZenUML Syntax and saves the output in a new CSV.

#### 6. `single_run(code: str, fileName: str) -> int`
Automates the process of entering code into ZenUML, capturing a screenshot, and then detecting templates in the resultant image.

#### 7. `single_run_counter(code: str)`
Automates the ZenUML process for a single run and updates the internal counter.

#### 8. `automate_msg_run(fileName: str)`
Automates the entire process: Convert Java methods in a CSV to ZenUML Syntax, run ZenUML, and detect templates in the resultant images.

### Usage:
To use this script and its functionalities:

```python
z = ZenUMLAuto()
fileName = 'methods_first'
z.convertor_run(fileName)
z.automate_msg_run(fileName)
