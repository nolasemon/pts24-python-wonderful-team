# Stone Age

This is the Python version of the semestral project from Principles of Software Design (1) course on FMFI UK, 2024/25. 

## Usage

0. Set up venv (optional)  
    `python -m venv venv`  
    Then
    - bash `source venv/bin/activate`
    - cmd `venv\Scripts\activate.bat` 

    See [How to create a Python venv](https://python.land/virtual-environments/virtualenv#How_to_create_a_Python_venv) for more information.
1. Install dependencies  
    `pip install -r requirements.txt`
1. Then you can use
    ```
    make check_and_test
    make lint
    make format
    ```
    to check and test, lint and format respectively.
    Or just
    ```
    make
    ```
    for all 3 combined.
    `make` doesn't come preinstalled on Windows. Nmake, MinGW can be used instead.