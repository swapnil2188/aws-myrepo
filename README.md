#Scripts
Check the different AWS Python Scripts available

#Running Scripts

This Package requires Python 3 and the requests Package.

First, Install Pipenv.Then:

```
pipenv install
pipenv run python files/hello-world.py 
```  

# AWS Boto3 

# About
This Project is for self-learning, and uses boto3 to manage AWS EC2 instance snapshots.

# Configuring
swap2188 uses the configuration file created by the AWS cli. e.g.

`aws configure --profile swap2188`

# Running
`pipenv run python scripts/list-ec2-instances.py`

# Help
```pipenv run python scripts/aws-ec2-instances-click.py --help
Usage: aws-ec2-instances-click.py [OPTIONS]

  List all EC2 Instances

```
