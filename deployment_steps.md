**Packaging the Model for Deployment**

import pickle
with open('model.pkl', 'wb') as f:
    pickle.dump(model, f)
with open('model.pkl', 'rb') as f:
    loaded_model = pickle.load(f)

**Containerization**

#create a dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
CMD ["python", "app.py"]

#build the docker image
docker build -t churn-prediction-app .

#Run the container
docker run -p 5000:5000 churn-prediction-app


**Setting up Infrastructure on AWS EC2**
1.Use AWS EC2 for deployment
2.Launch an EC2 instance with an Python environment (Ubuntu)

3.Install Python and required dependencies:
sudo apt update
sudo apt install python3-pip -y
pip install flask pandas scikit-learn

4.Configure security groups to allow ports 22 (SSH) and 5000 (application).
5.Upload project files to the instance using scp or SFTP.


**Deployment Testing**

import unittest
from app import app

class TestChurnAPI(unittest.TestCase):
    def test_home(self):
        tester = app.test_client(self)
        response = tester.get('/')
        self.assertEqual(response.status_code, 200)

    def test_predict(self):
        tester = app.test_client(self)
        response = tester.post('/predict', json={
            "gender": "Female",
            "SeniorCitizen": 0,
            "Partner": "Yes",
            # Add other necessary inputs...
        })
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()



**Monitoring and Logging Setup**

#Integrate logging into the application for better debugging
import logging
logging.basicConfig(level=logging.INFO)
logging.info("Server started successfully.")

Use AWS CloudWatch for monitoring and managing logs:
1.Install the CloudWatch agent on the EC2 instance.
sudo yum install amazon-cloudwatch-agent
2.Configure log files for CloudWatch monitoring.



**Scalability Assessment and Planning**

#Enable Load Balancer for EC2:
1.Go to the EC2 Dashboard.
2.Create an Application Load Balancer.
3.Register your EC2 instance under the load balancer.


**Security Considerations**
1.Use HTTPS for secure communication by setting up SSL certificates with services like AWS Certificate Manager.
2.Restrict access via EC2 security group rules to specific IP ranges.
3.Implement user authentication for API endpoints if necessary.

from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to a secure API!"

if __name__ == '__main__':
    app.run(ssl_context=('cert.pem', 'key.pem'))


#Generate cert.pem and key.pem using Let's Encrypt or OpenSSL:
openssl req -new -x509 -keyout key.pem -out cert.pem -days 365 -nodes



**Continuous Integration/Continuous Deployment (CI/CD) Pipeline Setup**

#Set up a pipeline using AWS CodePipeline or GitHub Actions:
1.Push code to a GitHub repository.
2.Automate the deployment process with AWS CodePipeline or a CI/CD workflow.
3.Test deployments in staging before production.

name: CI/CD Pipeline

on: [push]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.9
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run tests
        run: pytest
      - name: Deploy
        run: python deploy_script.py


**Version Control for Models**
Track model versions with a versioning system:
Use Git to track changes in the project files.

dvc init
dvc add model.pkl
git add model.pkl.dvc
git commit -m "Added model version 1.0"



**Documentation for End Users and Developers**

#Create a README.md with:
   1.Overview of the project.
   2.API usage instructions.
   3.Sample inputs and outputs.
   4.Document dependencies in requirements.txt.
   5.Maintain a changelog for updates.

# Customer Churn Prediction API

## Features
- Predicts whether a customer will churn based on input features.

## API Endpoints
1. **GET /**: Home route.
2. **POST /predict**: Accepts customer data and returns churn prediction.

## Running Locally
1. Install dependencies: `pip install -r requirements.txt`.
2. Start the app: `python app.py`.

## Deployment
Deployed on AWS EC2 with monitoring via CloudWatch.
