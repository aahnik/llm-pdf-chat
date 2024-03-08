# PriyQb

FastAPI + Streamlit + Langchain!

## Running Locally

Make sure to have [`poetry` package manger](https://python-poetry.org/)
installed locally.

Configure the `.env` file as per the `.env.template`

- Install all the dependancies locally:

    ```shell
    poetry install
    poetry shell # activate the virtual environment
    ```

- To start the FastAPI backend server:

    ```shell
    # first make sure you have a mongo db server up and running
    # and that you have set the connection string in your .env file
    cd server
    uvicorn main:app --reload
    # --reload if you are developing and changing the source files
    ```

    This would start running the API on your [`localhost:8000`](http://localhost:8000)
    and
    you can access the Swagger Docs at [`/docs`](http://localhost:8000/docs) endpoint.

- To start the streamlit web-interface:

    ```shell
    cd client
    streamlit run app.py
    ```

    This would start the streamlit app at [`localhost:8501`](http://localhost:8501).
