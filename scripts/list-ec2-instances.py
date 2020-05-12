import boto3                                    #Import boto3 Package

if __name__ == '__main__':
    session = boto3.Session(profile_name='swap2188') #Create a session with Profile(aws configure)
    ec2 = session.resource('ec2')                   # Add AWS resource Name

    for i in ec2.instances.all():                   # List all Ec2 Instances - Instance Id's
        print (i)
