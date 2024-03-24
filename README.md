# llm-pdf-chat

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

## Files Directory

> **Note**: Files are shared between the streamlit and FastAPI code.

- It is expected that both the processes are running on the same machine.
- The environment variable, `FILES_STORAGE_DIR`
is used by both the streamlit and FastAPI code.
- The files uploaded from the streamlit interface are stored in this directory,
and are accessed by langchain running in the server code of FastAPI.
- Either write an absolute path,
or the path must be wrt the parent of the client or server dirs. like `../uploaded_files/`
