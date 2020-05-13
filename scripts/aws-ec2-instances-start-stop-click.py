import boto3
import click

session = boto3.Session(profile_name='swap2188')
ec2 = session.resource('ec2')

def filter_instances(project):    #Define a Filter Instances Function - Gives list of All EC2 Instances
    instances = []

    if project:
        filters = [{'Name':'tag:Project', 'Values':[project]}]
        instances = ec2.instances.filter(Filters=filters)
    else:
        instances = ec2.instances.all()

    return instances

@click.group()                                      #Defining Instances Group
def instances():                                    # Function for Instances
    """Commands for instances"""

@instances.command('list')                          #Command 'List' for Instances
@click.option('--project', default=None, help="Only instances for Project (tag Project:<name>)")

def list_instances(project):
	"List all EC2 Instances"

	instances = filter_instances(project)          #Calling the filter Instances Function

	for i in instances:
		tags = { t['Key']: t['Value'] for t in i.tags or [] }
		print(', '.join((
			i.id,
			i.instance_type,
			i.placement['AvailabilityZone'],
			i.state['Name'],
			i.public_dns_name,
			tags.get('Project', '<no project>')
			)))
	return

#Stop EC2 Instances
@instances.command('stop')
@click.option('--project', default=None, help='Only instances for project')

def stop_instances(project):
    "Stop EC2 instances"

    instances = filter_instances(project)           #Calling the filter Instances Function

    for i in instances:
        print("Stopping {0}...".format(i.id))
        i.stop()

    return

#Start EC2 Instances
@instances.command('start')
@click.option('--project', default=None, help='Only instances for project')

def start_instances(project):
    "Start EC2 instances"

    instances = filter_instances(project)           #Calling the filter Instances Function

    for i in instances:
        print("Starting {0}...".format(i.id))
        i.start()

    return

if __name__ == '__main__':
    instances()                         #Call the Group and not Function as before
