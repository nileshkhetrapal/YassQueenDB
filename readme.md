# YassQueenDB

YassQueenDB is a Python-based program designed to create and manage a vector database for sentences. It allows users to create a database, update it with new sentences, search for the nearest neighbor of a given vector, and delete vectors from the database. The database is stored as a CSV file in the same directory as the current working directory.

## Features

* Create a vector database from a set of documents
* Add vectors to the database
* Query the database for the nearest neighbor of a given vector
* Delete vectors from the database

## Dependencies

* numpy
* pandas
* textract
* tensorflow
* tensorflow_hub

## Usage

YassQueenDB is a command-line based program. Run the program with the following commands:

1. **Create** a vector database:

`python YassQueenDB.py create <tablename> --documents <document1> <document2> ...`

2. **Update** the vector database with new documents:

`python YassQueenDB.py update <tablename> --documents <document1> <document2> ...`

3. **Search** the vector database for the nearest neighbor of a given query:

`python YassQueenDB.py search <tablename> --query "Your query here"`

4. **Delete** the vector from the database that is closest to the given query:

`python YassQueenDB.py delete <tablename> --query "Your query here"`

## Example

To create a new vector database from two documents (doc1.txt and doc2.txt) and store it in a file called `my_database.csv`:

`python YassQueenDB.py create my_database.csv --documents doc1.txt doc2.txt`

To search for the nearest neighbor of the query "What is the meaning of life?" in the `my_database.csv`:

`python YassQueenDB.py search my_database.csv --query "What is the mea`

YassQueen Graph DB (yqgdb) is a lightweight, flexible, and easy-to-use sentence-based vector database that utilizes TensorFlow Keras embeddings and a custom graph data structure to enable semantic querying, updating, and deleting of entries. With yqgdb, you can perform natural language processing tasks such as searching for similar sentences, organizing text data, and more.
