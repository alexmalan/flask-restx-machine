# Flask REST API
    1. Functionalities covered:
    -   Rest API CRUD opertaions;
    -   Validation for request data;
    -   Unit tests with pytest
    -   API docs with swagger;
    -   Code quality assured with pylint;
    -   Static Analysis assured with deepsource.io;
    2. Programming principles covered:
    -   Best practices in Flask;
    -   Geneneric response format;
    -   Custom error handling for all response types;

### Notes

- I was advised to use Flask REST framework in this case so flask-restx is the main framework

## Code quality

### Static analysis
- Static code analysis used: https://deepsource.io/gh/
![Screenshot 2022-09-23 at 19 01 33](https://user-images.githubusercontent.com/19578866/192003738-d0e83172-1fa2-482d-8b16-2588da7b028c.png)

### Pylint
- Pylint used to maintain code quality;
- Rules for code quality can be consulted in `.pylintrc`
- Current status: `Your code has been rated at 10.00/10 (previous run: 10.00/10, +0.00)`

## Requirements

It is assumed that:
-   You have Python and MySQL installed. If not, then download the latest versions from:
    * [Python](https://www.python.org/downloads/)
    * [MySql](https://dev.mysql.com/downloads/installer/)

## Installation

1. **Clone git repository**:
   ```bash
   git clone [CLONE_LINK]
   ```

2. **Create virtual environment**
    - Windows
    ```bash
    python -m venv $(pwd)/venv
    source venv/bin/activate
    ```
   
    - OS X
    ```bash
    python3 -m venv $(pwd)/venv
    source venv/bin/activate
    ```

3. **Install requirements**:
    - Windows
    ```bash
    pip install -r requirements.txt
    ```
   
    - OS X
    ```bash
    pip3 install -r requirements.txt
    ```

4. **Add environment variables**
    - Create a file named `.env` in project root directory
    - Add and fill next environment variables with your local database config:
        ```.env
        DATABASE_USERNAME=
        DATABASE_PASSWORD=
        DATABASE_NAME=
        DATABASE_PORT=
        DATABASE_HOST=
        SECRET_KEY=
        TEST_DATABASE_NAME=
        ```

## Migrate on data model changes
    
- Run fallowing commands
    - Windows
    ```bash
    python app.py db init
    python app.py db migrate
    python app.py db upgrade
    ```
    
    - OS X
    ```bash
    python3 app.py db init
    python3 app.py db migrate
    python3 app.py db upgrade
    ```

### Useful

- For any packaging issues please run:
  ```bash
  python -m pip check
  ```

## Import Postman
- Locate the file in the root repository path: Vending Machine.postman_collection.json
- Import process: Open Postman > File > Import > Upload Files > Choose from Computer > Import
- You are able to test the endpoints and different scenarios and inputs

## Run

-   Application can run directly from cmd using following commands:
    - Using python run
        - Windows
        ```bash
        python app.py run
        ```
      
        - OS X
        ```bash
        python3 app.py run
        ```

## Test

- Tests are done with pytest
- Run:
    - Method1:
        - Windows:
        ```bash
        python app.py test
        ```
        
        - OS X:
        ```bash
        python3 app.py test
        ```
    - Method2 - Using pytest:
        - For following options are available:
            - `-v` - to have verbose tests
            - `-s` - to see logging from tests
      
        - Windows:
        ```bash
        pytest tests
        ```
        
        - OS X:
        ```bash
        pytest -q tests
        ```

