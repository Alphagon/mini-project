### API Database Integration Documentation

#### Overview
This documentation outlines the setup process for integrating MongoDB and PostgreSQL with your FastAPI application. It includes instructions for setting up the databases, configuring the environment, and accessing and querying the data.

#### Setup Process
##### 1. Environment Variables
First, create a `.env` file in the root directory of your project and include all sensitive information related to your databases. This file should never be pushed to GitHub or any public repository. Instead, it should be manually uploaded to the required virtual machine or added as secrets in your cloud environment.

**Example `.env` file content:**
```
MONGO_URL=mongodb://mongo:27017
MONGO_INITDB_ROOT_USERNAME=your_mongo_root_username
MONGO_INITDB_ROOT_PASSWORD=your_mongo_root_password
MONGO_DATABASE_NAME=sentiment_logs
MONGO_COLLECTION_NAME=api_logs
POSTGRES_USERNAME=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
POSTGRES_DATABASE_NAME=sentiment_db
```

##### 2. Dockerfile Update
Ensure that your Dockerfile copies the .env file while building the application. This allows the application to access the required environment variables at runtime.

##### 3. Using Docker Images for Databases
Rather than installing PostgreSQL and MongoDB on your local machine, you can use Docker images to simplify the setup.

###### Installing Docker Compose
To run multiple Docker containers simultaneously, install Docker Compose with the following command:

`sudo curl -L "https://github.com/docker/compose/releases/download/v2.29.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose`

Grant permissions to the Docker Compose binary:

`sudo chmod +x /usr/local/bin/docker-compose`

##### 4. Docker Compose Configuration

Use the provided docker-compose.yml file to run PostgreSQL and MongoDB as services.

```
version: '3.8'

services:
  mongodb:
    image: mongo:latest
    container_name: mongo
    ports:
      - "27017:27017"
    volumes:
      - mongo_data:/data/db

  postgres:
    image: postgres:latest
    container_name: postgres
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      - POSTGRES_USERNAME=${POSTGRES_USER}
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
      - POSTGRES_DB=${POSTGRESS_DB}

  api:
    build: .
    ports:
      - "8000:8000"
    depends_on:
      - mongodb
      - postgres

volumes:
  mongo_data:
  postgres_data:
```

##### 5. Building and Running the Containers
Build and run the Docker containers using the following command:

`sudo docker-compose up --build`

##### 6. Database Functionality Implementation
Create two new files named sql.py and mongo.py inside the db folder. Implement the necessary functions to create databases, establish connections, and log predictions and requests.

##### 7. Integration with FastAPI
Integrate the functions created in sql.py and mongo.py into main.py. Ensure that your API logs requests to MongoDB and stores predictions in PostgreSQL.
Database Access and Querying


##### 8. Accessing Databases
###### PostgreSQL Access
To check if PostgreSQL is storing data correctly, use the following command to access the PostgreSQL command line:

`sudo docker exec -it postgres psql -U postgres -d sentiment_db`

From the PostgreSQL command line, you can:
- List tables: `\dt`
- Query predictions: `SELECT * FROM prediction;`

###### MongoDB Access
To verify that MongoDB is logging data, access the MongoDB command line with:

`sudo docker exec -it mongo mongosh`

From the MongoDB command line, you can:
- Switch to the logging database: `use sentiment_logs`
- Show collections: `show collections`
- Retrieve all logs: `db.api_logs.find()`
- Retrieve the latest log entry: `db.api_logs.find().sort({ _id: -1 }).limit(1)`