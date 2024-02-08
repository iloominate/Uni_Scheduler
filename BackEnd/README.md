## Run backend on local server

1. Check if Python is installed: 

    ```
    python --version
    ```

2. Create virtual environment, if isn't cerated:

    ```
    python -m venv .venv
    ```

3. Activate virtual environment:

    ```
    .venv\Scripts\activate
    ```

4. Install all required packages:

    ```
    pip install -r requirements.txt
    ```

5. Initialize database:

    ```
    python manage.py migrate
    ```

6. Generate test data:

    ```
    python manage.py loaddata data.json
    ```

7. Run server on localhost:

    ```
    python manage.py runserver
    ```