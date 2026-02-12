WithaVision – Interactive 3D Physics Visualization Lab

Project Title : WithaVision – Interactive 3D Physics Visualization Lab

Description:
WithaVision is an interactive physics learning application that converts physics word problems into real-time motion simulations.
Instead of focusing only on equations, the application visually demonstrates how motion takes place using animations and graphs.

The system reads a problem statement, identifies the type of motion involved, and generates the corresponding simulation along with graphical analysis.
It also allows students to verify their answers and track their performance while practicing problems.

The application runs completely offline.

Tech Stack Used:
* Python
* Streamlit (User Interface)
* NumPy (Physics calculations)
* Plotly (2D and 3D visualization)
* Pillow (Image handling)
* Pytesseract (OCR for extracting text from images)

How to Run the Project:
Step 1: Install required libraries
Open terminal or command prompt and run:
"pip install streamlit numpy plotly pillow pytesseract"
if you want to use the image input feature, make sure **Tesseract OCR** is installed on your system.


Step 2: Run the application
"streamlit run app.py"
After running this command, open the local URL shown in the terminal in your browser.

Dependencies:
The project requires the following Python libraries:
* streamlit
* numpy
* plotly
* pillow
* pytesseract
If OCR functionality is used, **Tesseract OCR software** must be installed separately.

Important Instructions:
* Ensure Python is installed before running the project.
* If Tesseract OCR is not installed, image-based input will not work.
* The project runs locally and does not require an internet connection.

Use clear problem statements such as:
* A ball is projected at 40 m/s at 45 degrees
* A ball is dropped from 20 m
* A particle moves in circular motion at 15 m/s

Demo Images of MVP:
Screenshots can be found here:  
https://drive.google.com/drive/folders/1981c1OopO8bFz4atSYI-ogcp7s10kg9F

License:
This project is developed for educational and academic purposes only.



