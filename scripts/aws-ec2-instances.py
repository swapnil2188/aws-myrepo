import boto3
import sys

session = boto3.Session(profile_name='swap2188')
ec2 = session.resource('ec2')

def list_instances():               #Function to list EC2 Instances
    for i in ec2.instances.all():
        print(i)

if __name__ == '__main__':
    print(sys.argv)
    list_instances()                #Calling Function from Main
    
