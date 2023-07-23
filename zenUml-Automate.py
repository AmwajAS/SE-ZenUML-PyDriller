import pyautogui
import time
import cv2 as cv
import numpy as np
import re
import pandas as pd

class ZenUMLAuto:
    def __init__(self):
        """Initialize counter to track iterations."""
        self.counter = 0

    @staticmethod
    def automate_code(code, file_name):
        """
        Automate ZenUML desktop Windows app using pyautogui.

        Parameters:
        - code (str): The code to be written in ZenUML.
        - file_name (str): The name of the file where the screenshot will be saved.
        """
        time.sleep(5)
        pyautogui.dragTo(500, 500, duration=1)
        pyautogui.click()
        pyautogui.hotkey("ctrl", "a")
        pyautogui.hotkey("backspace")
        pyautogui.write(code)
        pyautogui.screenshot(f"{file_name}.png")

    @staticmethod
    def detection(img_file_name):
        """
        Detect template images within another image.

        Parameters:
        - img_file_name (str): The name of the image file to process.

        Returns:
        - int: The total count of detected templates in the image.
        """
        img_file = f"{img_file_name}.png"
        img_rgb = cv.imread(img_file)
        if img_rgb is None:
            raise ValueError(f"File {img_file} could not be read.")
        
        img_gray = cv.cvtColor(img_rgb, cv.COLOR_BGR2GRAY)
        
        # Templates to be matched
        template1 = cv.imread('template1.jpg', cv.IMREAD_GRAYSCALE)
        template2 = cv.imread('template2.jpg', cv.IMREAD_GRAYSCALE)
        
        for template in [template1, template2]:
            if template is None:
                raise ValueError("One of the template files could not be read.")
        
        w1, h1 = template1.shape[::-1]
        w2, h2 = template2.shape[::-1]

        def process_template(template, w, h):
            """Internal helper function to process each template."""
            nonlocal img_gray, img_rgb, img_file_name
            res = cv.matchTemplate(img_gray, template, cv.TM_CCOEFF_NORMED)
            threshold = 0.8
            loc = np.where(res >= threshold)
            counter = 0
            before_y, before_x = 0, 0
            
            for pt in zip(*loc[::-1]):
                cv.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
                if before_y == pt[1] or before_x == pt[0]:
                    continue
                before_y, before_x = pt[1], pt[0]
                counter += 1
            
            return counter
        
        total_count = process_template(template1, w1, h1)
        total_count += process_template(template2, w2, h2)
        
        cv.imwrite(f"{img_file_name}_res.png", img_rgb)
        
        return total_count

    @staticmethod
    def convert(function):
        """
        Convert a Java function into ZenUML Syntax.

        Parameters:
        - function (str): The Java function to be converted.

        Returns:
        - str: The ZenUML formatted function.
        """
        lines = function.split("\n")
        converted_lines = []
        remove_first_brace = True  
        counter_brace = 0
        
        for line in lines: 
            if "for" in line:
                loop_variable = line.split(" ")[1].strip("(")
                loop_condition = line.split(";")[1].strip() if ";" in line else ""
                converted_lines.append(f"for({loop_condition})")
            elif re.search(r'(int|String|boolean|float|ArrayList|List)', line):
                match = re.search(r'(\b[a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*([\w\W]+)', line)
                if match:
                    variable_name, value = match.group(1), match.group(2)
                    if "new" not in value:
                        converted_lines.append(f"{variable_name}={value}")
            elif "{" in line:
                counter_brace += 1
                if remove_first_brace:
                    line = line.replace("{", "", 1)
                    remove_first_brace = False
                converted_lines.append(line)
            elif "}" in line:
                counter_brace -= 1
                if counter_brace == 0:
                    line = line.replace("}", "", 1)
                converted_lines.append(line)
            else:
                converted_lines.append(line)
        
        return "\n".join(converted_lines)

    def convertor_run(self, methods_file_name ):
        """
        Convert Java methods in a CSV to ZenUML Syntax.

        Parameters:
        - methods_file_name (str): The name of the CSV containing Java methods.
        """
        code_name= f"{methods_file_name}.csv"
        df = pd.read_csv(code_name)
        df['DSL'] = df['Method code'].apply(self.convert)
        new_file_name = f"{methods_file_name}_dsl.csv"
        df.to_csv(new_file_name, index=False)

    def single_run(self, code, fileName):
        """
        Automate ZenUML for a single run.

        Parameters:
        - code (str): The code to be written in ZenUML.
        - fileName (str): The name of the file to save the result.

        Returns:
        - int: The count of detected templates.
        """
        self.automate_code(code, fileName)
        return self.detection(fileName)

    def single_run_counter(self, code):
        """
        Automate ZenUML for a single run and update the counter.

        Parameters:
        - code (str): The code to be written in ZenUML.
        """
        self.counter += 1
        return self.single_run(code, str(self.counter))

    def automate_msg_run(self, fileName):
        """
        Automate the entire process: Convert to ZenUML Syntax, run ZenUML, and detect templates.

        Parameters:
        - fileName (str): The name of the CSV containing ZenUML syntax.
        """
        code_name= f"{fileName}_dsl.csv"
        df = pd.read_csv(code_name)
        df['counter'] = df['DSL'].apply(self.single_run_counter)
        new_file_name = f"{fileName}_result.csv"
        df.to_csv(new_file_name, index=False)


if __name__ == "__main__":
    z = ZenUMLAuto()
    fileName = 'methods_first'
    z.convertor_run(fileName)
    z.automate_msg_run(fileName)
