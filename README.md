### Database integration

Download docker-compose to run multiple dockers simultaneously
install - "sudo curl -L "https://github.com/docker/compose/release/download/v2.29.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose"
Give user permissions - "sudo chmod +x /usr/local/bin/docker-compose"

Write docker-compose code to run postgreSQL and MongoDB

include all the sensitive information in .env file [Secrets]. This in real world should not be pushed to github. 
This should be manually uploaded to the required the virtual machine or uploaded as secrets in the required cloud.

build the docker - "sudo docker-compose up --build"

Integrate main.py with storing of model realted data. and request related logging in PostgreSQL and MongoDB respectively.

To check if PostgreSQL is storing data or not, use the following docker command to access PostgreSQL commandline- 
"sudo docker exec -it postgres psql -U postgres -d sentiment_db"
From here you can access the commandline
- \dt  show tables
- SELECT * FROM prediction;


To check if Mongo is storing logs use the following docker command - "sudo docker exec -it mongo mongosh"
From here you can access the mongo commandline

- use sentiment_logs
- show collections
- db.api_logs.find()
- db.api_logs.find().sort({ _id: -1 }).limit(1) just the last or lates record