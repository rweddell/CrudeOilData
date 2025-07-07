# Crude Oil Import API
This project enables analysis and manipulation of a [US Crude Oil Imports](https://www.kaggle.com/datasets/alistairking/u-s-crude-oil-imports) dataset.
The project includes scripts for loading data into a postgres table, and exposes crud operations through an API. 

## Installation and Setup:
### Requirements
1. [Python](https://www.python.org/downloads/)
    - Version 3.13 used for development
2. [Postgres](https://www.postgresql.org/download/)  
    - Version 17 used during development
    - Recommended to follow standard installation steps
    - [Installation tutorial](https://www.youtube.com/watch?v=GpqJzWCcQXY&t=568s)
3. [Pipenv](https://pipenv.pypa.io/en/latest/)
    - Used to create virtual environments and manage dependencies  
4. Choice of HTTP Tool
    - [Postman](https://www.postman.com/downloads/)
    - [Insomnia](https://insomnia.rest/download)

### Setup steps
1. Install Postgres  
    - Follow standard installation steps.  
    - No need for additional features installed with Stack Builder  
    - Save the password created during installation  
        - It will be added to your .env file  
2. Install or check version of Python  
3. Create your .env file
    - Rename [skeleton.env](skeleton.env) to simply .env
    - Remove defaults if necessary and populate values that you have created
        - DB_HOST
        - DB_PORT
        - DB_NAME
        - DB_USER
        - DB_PASSWORD
4. Create a [virtual environment](#creating-a-virtual-environment-with-pipenv)
    - Pipenv was used for development, but other managers exist
5. Install required libraries into virtual environment
6. Download data and create table
    - Use the files detailed in the [scripts section](#scripts)
6. Start the API server
    - Navigate to top directory of repository
    ```python
    >>> python server.py
    ```
7. API documentation can be accessed once the server is running
    - http://localhost:8000/docs

## Data description
- Currently hard-coded to use the US Crude Oil Imports dataset [link in sources](#sources)
- The dataset has over 483,000 rows

### Input Record Schema
```
{
    "year": integer,
    "month": integer,
    "originName": string,
    "originTypeName": string,
    "destinationName": string,
    "destinationTypeName": string,
    "gradeName": string,
    "quantity": integer
}
```

### Response Record Schema
- Same as input, but with a generated 'id' attribute
```
{
    "id": integer,
    "year": integer,
    "month": integer,
    "originName": integer,
    "originTypeName": string,
    "destinationName": string,
    "destinationTypeName": string,
    "gradeName": string,
    "quantity": integer
}
```

## Endpoints
#### GET /imports
- Summary:
    - Paginates over the dataset
    - Retreives records according to provided filters
- Query args:  
    - country: string, optional
    - limit: integer, defaults to 100
    - offset: integer, defaults to 0
- Response:
    - Array of [response records](#response-record-schema) of length "limit"

#### POST /imports
- Summary:
    - Endpoint to create a new record.  
- Request body
    - [input record](#input-record-schema): all attributes required
- Response:
    - [response record](#response-record-schema): newly created record

#### GET /imports/find/<record_id>
- Summary:
    - Retrieve the record associated with the provided record_id
- Path params:
    - record_id: integer, required
- Response is in the format of [response record](#response-record-schema)

#### PUT /imports/update/<record_id>
- Summary:
    - Update an existing record associated with the given record_id
- Path params:
    - record_id: integer, required
- Request body:
    - [input record](#input-record-schema): at least one attribute is required
- Response: 
    - [response record](#response-record-schema): existing record with updated values

#### DELETE /imports/delete/<record_id>
- Summary: 
    - Attempt to delete an existing record matching to the provided record_id
- Path params:
    - record_id: integer, required
- Response:
    - [response record](#response-record-schema): complete record that was deleted


## Creating a virtual environment with pipenv
- After installing python, install pipenv
    ```python
    >>> pip install pipenv
    ```
- Navigate to the top directory of the repository and create a pipenv shell
    ```python
    >>> pipenv shell
    ```
- Install required libraries for the project from requirements.txt or Pipfile
    ```
    # Pipfile
    >>> pipenv install
    ```
    ```
    # Requirements.txt
    >>> pipenv install -r requirements.txt
    ```

## Scripts
At the top directory structure is a folder named [scripts](scripts).  
This folder contains some useful setup automation including:
- dataset download
- table creation
- data population

### data_and_table.py
This script automatically downloads data, infers its structure, and creates a table in postgres.
- It can be found here [data_and_table.py](scripts/data_and_table.py)
- Run this script from command line *before* starting the server
    ```python
    >>> python scripts/data_and_table.py
    ```
- The server expects the table to exist in order to function

### send_data_to_api.py
This script reads the file downloaded by data_and_table.py and sends single records to the API. Inefficient for large files, but useful for small CSVs.
- It can be found here [send_data_to_api.py](scripts/send_data_to_api.py)
- Run this script *after* the table has already been created
    ```python
    >>> python scripts/send_data_to_api.py
    ```

### project_setup.py
This script is full automation for data preparation.
- It can be found here [project_setup.py](scripts/project_setup.py)
- It automates:
    - dataset download
    - table creation
    - data population into the new table
- Run this script from commmand line
```python
>>> python scripts/project_setup.py
```


## Sources

[US Crude Oil Imports](https://www.kaggle.com/datasets/alistairking/u-s-crude-oil-imports)

[Python .git_ignore](https://github.com/github/gitignore/blob/main/Python.gitignore)
