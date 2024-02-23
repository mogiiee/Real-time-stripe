
# Zenskar Assignment: Back End Engineer Intern

This project integrates your local customer catalog with external services like Stripe and potentially Salesforce. It uses FastAPI for the web server, Celery for asynchronous task processing, Docker for containerization, and Ngrok for local webhook testing.

## Table of Contents
- [Getting Started](#getting-started)
- [Running with Docker](#running-with-docker)
- [Running Locally](#running-locally)
- [Setting Up Ngrok for Webhooks](#setting-up-ngrok-for-webhooks)
- [Environment Variables](#environment-variables)
- [API Endpoints](#api-endpoints)
- [Answers to throretical questions](#Answers-to-throretical-question-1)
- [Answers to throretical question 2](#Answers-to-throretical-question-2)

### Prerequisites

- Python 3.9+
- Docker & Docker Compose (for Docker setup)
- A Stripe account for testing Stripe integration

**Be sure to have all the environment variable set up, All the keys and auth token for the webhook**

### Tech stack
- fastapi
- sqlite
- docker
- stripe API
- Ngrok (webhook)
- Celery (worker)
- rabbitMQ (queue)


```bash
git clone https://github.com/mogiiee/Zenskar-Task.git
cd Zenskar-Task
```

Workflow Diagram

![workflow diagram](https://cdn.discordapp.com/attachments/991052554802712586/1210547286778581042/ZENSKAR_TASK.drawio.png?ex=65eaf504&is=65d88004&hm=9dc760eb277f2b95ccccd7c743d6d879237f6e7324abd67f034bda58aa1f4a13&)



## Running with Docker

This method uses Docker to run the FastAPI server, Celery worker, and RabbitMQ. It has a docker-compose up file which can start all the docker container at the same time for the ease of deployment.

### Build and Start Services

```bash
docker-compose up --build
```

This command builds the Docker images and starts the containers defined in `docker-compose.yml`. 

Please wait for about 10 seconds for the server to start up. You should see something like this 

![success docker compose up](https://cdn.discordapp.com/attachments/991052554802712586/1210497998845509643/Screenshot_2024-02-23_at_1.36.45_PM.png?ex=65eac71c&is=65d8521c&hm=9f3e8331e187353f61d78bb1f1b2f1a13a72896243147817c7dfabf1d74e3c45&)

its okay for the celery worker to try 3 or 4 times to connect to the server. 

![this is okay](https://cdn.discordapp.com/attachments/991052554802712586/1210498157696262144/Screenshot_2024-02-23_at_1.37.12_PM.png?ex=65eac742&is=65d85242&hm=2cef3485902082ec8fa2ef2121a3790122c237d789ec46e0da72662448e82166&)

![this too is okay](https://cdn.discordapp.com/attachments/991052554802712586/1210498158073876551/Screenshot_2024-02-23_at_1.37.24_PM.png?ex=65eac742&is=65d85242&hm=00e6867d432d36745e59cb8fb33bfd4a97a4728fb773d660eb628492e24c8c70&)


both of these scenarios are okay just wait for about 10 seconds.


### Accessing the Application

- FastAPI server will be accessible at http://localhost:8000/docs or http://0.0.0.0:8000/docs


- RabbitMQ management interface at http://localhost:15672 (default credentials: guest/guest)

## Running Locally

It is not recommended as you might face alot of errors. I have designed it to work with docker-compose ... you will have to change alot of paths manually. Just use docker bro

![error pic](https://cdn.discordapp.com/attachments/991052554802712586/1210509656456429568/Screenshot_2024-02-23_at_2.23.03_PM.png?ex=65ead1f8&is=65d85cf8&hm=2ac3b2142eea381d6b46f35950bfb5c1554518f14ff848639fc41a46020ea988&)

### Virtual Environment Setup

```bash
python -m venv virtualenv
source virtualenv/bin/activate  
(linux)
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Start the FastAPI Server

```bash
uvicorn app.main:app --reload
```

### Start the Celery Worker

In a new terminal session, activate the virtual environment and run: (this is handled in the docker-compose file)

```bash
celery -A app.worker.celery_worker worker --loglevel=info
```

## Setting Up Ngrok for Webhooks


Ngrok allows you to expose your local server to the internet, facilitating webhook testing.

1. Download and install Ngrok from [Ngrok's website](https://ngrok.com/download).
2. Start Ngrok to expose port 8000:

   ```bash
   ./ngrok http 8000 or ngrok http 8000
   ```

3. Copy the forwarding URL provided by Ngrok (e.g., `https://<random_string>.ngrok.io`).

4. Add this URL in the [webhook section](https://dashboard.stripe.com/test/webhooks/) in the Dashboard of stripe.

**Remember to add URL/webhooks/stripe at the end** else you would get a 400 error as it wont hit the right endpoint. Been there done that lol.

## Environment Variables

Create a `.env` file or just populate the `.env.sample` file in the root directory and add the following variables:

- STRIPE_SECRET_KEY='sk_test.... replace it here'
- STRIPE_PUBLISHABLE_KEY='pk_test_.... replace it here although this is not used in the backend'secret.

there is another .env.sample file in `app/webhook_handler/.env.sample` you can poplulate it with 

- SIGNING_SECRET="get it from the Stripe dashboard> webhook> signing secret"

### Obtaining Stripe Environment Variables

1. **API Key**: Found in your Stripe Dashboard under Developers > API keys.
2. **Endpoint Secret**: Create a webhook endpoint in Stripe Dashboard (Developers > Webhooks) using your Ngrok URL. Use the secret provided there.


## Issues Faced

- I had to spend alot of time figuring out what the logic will be for the local id and the id mentioned in Stripe

- If you see my initial commits, I tried using Kafka with a producer and consumer queue. I could not figure out how I can include it as a container and run it with docker-compose. Hence I decided to go with RabbitMQ

## API Endpoints

- **Greeting to the people of Zenskar with love**: `GET /`
- **Create Customer**: `POST /customers/`
- **Update Customer**: `PUT /customers/{customer_id}`
- **Delete Customer**: `DELETE /customers/{customer_id}`
- **Stripe Webhook**: `POST /webhooks/stripe`

## Answers to throretical question 1

How would the current setup be utilized with salesforce API. With the research I have done, this setup would work fine provided there are 3 key changes done on top of this setup.

1. Salesforce does not have a customers API like stripe but it has Account> Contact where objects like customer details can be stored. Account is where business details are stored and contact is where custormers of that business is stored. Salesforce just like Stripe has a REST API to access these and perform CRUD ops on their dashboard, but it requires secondary authentication with OAuth2, which brings me to my second point.

2. Authentication, now this would have to be implemented completely from scratch as an OAuth flow would be needed to make valid API requests.

3. As we used Stripe's webhook, salesforce also provides a service called Salesforce outbound messages. A new end point could be made or the same one could be updated so that it calls different functions, when different services hit that endpoint. I have put the sample code above the webhook endpoint in comments [here](app/webhook_handler/stripe_webhooks.py).

4. We could also implement a celery beat which hits the Salesforce API as a cron job, and syncs the local db. The functions to sync the local db wll remain the same, only another beat would have to be implemented.

5. Minor changes in the the docker-compose file to make sure that this beat is running when the entire service is up.

## Answers to throretical question 2

Since invoicing is a completely different topic from the customers, there would need to be extentions to some of the code base. The part where both of these can be linked would be where each customer_id has some invoices(status does not matter)

1. Celery workers- 
- Similarity: Just as how i have tasks for syncing customer data (update_customer_in_stripe), I can create tasks like create_invoice_in_stripe and update_invoice_status_in_local_db.

- Improvement: Implement task routing in Celery to separate customer-related tasks from invoice-related tasks, improving task management and scalability.

2. Data Model Expansion

- Similarity: Just as i have a customer model that includes Stripe-specific information (stripe_customer_id), i will need an invoice model that might include fields like stripe_invoice_id, amount, status, and a relationship to the customer model.

3. Webhook Handling

- Similarity: The existing webhook endpoint (@app.post("/webhooks/stripe")) uses payload validation and event type checking. Similar logic will apply to invoice events, identifying them through event['type'] (e.g., invoice.paid, invoice.payment_failed). This can be checked when creating the webhook on the dashboard.

4. API and Authentication

- Since I am using the same stripe API's there would be no issues to get the Stripe's Invoices API. New functions would have to be created to make changes to the invoice, update its status and preprocess it to get important information.


With a few changes to the code, we can implement new functions which write the same to the local db and show all the invoice information which the stripe API is giving in a new table.





## Screenshots
- main dashboard of all the endpoints using swagger UI. Can also use Postman if that's more up your alley.

![main dashboard](https://cdn.discordapp.com/attachments/991052554802712586/1210499211716722748/Screenshot_2024-02-23_at_1.41.33_PM.png?ex=65eac83e&is=65d8533e&hm=5a6ed17bfeafcf7b69c49ef2b8dc42bd985bb0f99d91cf7293e8ec7c4800fd0a&)

- Be sure to check these events while creating the webhook

![webhook opts](https://cdn.discordapp.com/attachments/991052554802712586/1210502706339385364/Screenshot_2024-02-23_at_1.55.28_PM.png?ex=65eacb7f&is=65d8567f&hm=98eea36fb327e9de9777b59b4d57f9e0138eaad4402a8421541db8517fe0525d&)

- My first customer Christopher Nolan when made directly on the dashboard, will be reflected in app/data/database.db

![customer](https://cdn.discordapp.com/attachments/991052554802712586/1210503185710579738/Screenshot_2024-02-23_at_1.57.22_PM.png?ex=65eacbf1&is=65d856f1&hm=62f8ce65b8da6cd12c957df632805425dc9c7b2d636dae69465452933f671a53&)

- all the customers can be created, updated and deleted from the dashboard and everything will reflect in the local database

![all customers](https://cdn.discordapp.com/attachments/991052554802712586/1210504283984891955/Screenshot_2024-02-23_at_2.01.42_PM.png?ex=65eaccf7&is=65d857f7&hm=c1c6e5472e99e5ae9721c620ce476d3fe2afb658a60696a0779fd33186a839a8&)

- creation endpoint

![creation](https://cdn.discordapp.com/attachments/991052554802712586/1210504649157644348/Screenshot_2024-02-23_at_2.03.07_PM.png?ex=65eacd4e&is=65d8584e&hm=f2acb360c7ec4e3978fb58adca43760aee1509f3e54c991de895517af5986278&)

- update endpoint

![update](https://cdn.discordapp.com/attachments/991052554802712586/1210504913172434984/Screenshot_2024-02-23_at_2.04.13_PM.png?ex=65eacd8d&is=65d8588d&hm=01afdaa8905199c91546854dc37f54c0b4854ae3fd272c091e3639978ea90e00&)

- delete endpoint
![delete](https://cdn.discordapp.com/attachments/991052554802712586/1210505176230662164/Screenshot_2024-02-23_at_2.05.17_PM.png?ex=65eacdcc&is=65d858cc&hm=47a234f7e88c467e49b684e3437a964d32497a6ebdf5541cd27dafcc18372ed3&)

- local database

![localdb](https://cdn.discordapp.com/attachments/991052554802712586/1210505292329132112/Screenshot_2024-02-23_at_2.05.45_PM.png?ex=65eacde7&is=65d858e7&hm=2e015386549695b942562a8fa1fc4517e5a42089fdb09bae9e70f4a525f54941&)

