import boto3
import botocore
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

#Function to check for Pending Snapshot
def has_pending_snapshot(volume):
    snapshots = list(volume.snapshots.all())
    return snapshots and snapshots[0].state == 'pending'

@click.group()                                  #Main group
def cli():                                      #Function for Sub group-CLI
    """Script manages Instances and Snapshots"""

@cli.group('snapshots')
def snapshots():
    """Commands for snapshots"""

@snapshots.command('list')
@click.option('--project', help="Only snapshots for Project (tag Project:<name>)")
#This Option for list_all will list every snapshot for every volume if specify it
@click.option('--all', 'list_all', default=False, is_flag=True,
        help="List all snapshots for each volume not just the recent one")

def list_snapshots(project, list_all):
    "List EC2 Snapshots"

    instances = filter_instances(project)

    for i in instances:
        for v in i.volumes.all():
            for s in v.snapshots.all():
                print(", ".join((               #Join and return a Tuple of Params
                    s.id,                       #snapshot id
                    v.id,                       #volume id
                    i.id,                       #instance id
                    s.state,                    #snapshot state
                    s.progress,                 #snapshot progress
                    s.start_time.strftime("%c") #snapshot starttime formatted
                )))
#Only show recent Snapshot when State is completed and not list_all
#Hence break when both conditions satisfied else print all of them
                if s.state == 'completed' and not list_all: break

    return

@cli.group('volumes')                           #Defining Volumes CLI Group
def volumes():                                  #Function for Volumes
    """Commands for volumes"""

@volumes.command('list')
@click.option('--project', default=None, help="Only Volumes for Project (tag Project:<name>)")

def list_volumes(project):
    "List all Volumes"

    instances = filter_instances(project)

    for i in instances:
        for v in i.volumes.all():
            print(", ".join((
                v.id,
                i.id,
                v.state,
                str(v.size) + "GiB",
                v.encrypted and "Encrypted" or "Not Encrypted"
            )))

    return

@cli.group('instances')                         #Defining Instances CLI Group
def instances():                                #Function for Instances
    """Commands for instances"""

@instances.command('snapshot', help="Create Snapshots of all volumes for EC2 instances")
@click.option('--project', default=None, help="Only instances for Project (tag Project:<name>)")
def create_snapshots(project):
    "Create snapshots for EC2 instances"

    instances = filter_instances(project)

    for i in instances:
        print("Stopping {0}...".format(i.id))

        i.stop()                               #Calling Stop function
        i.wait_until_stopped()                 #Boto3 Check-wait until instances are stopped

        for v in i.volumes.all():
            if has_pending_snapshot(v):
                print(" Skipping {0}, snapshot already in Progress".format(v.id))
                continue

            print("  Creating snapshot of {0}". format(v.id))
            v.create_snapshot(Description="Created by our Script for snapshots")

        print("Starting {0}...".format(i.id))

        i.start()          #Start right after snapshot is initiated, No need to wait - Until the snapshot is completed
        i.wait_until_running          #Boto3 Check-wait until instances are started

    print("All jobs done!")

    return

@instances.command('list')                      #Command 'List' for Instances
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
        try:                                        #Error Check with try and Except
            i.stop()
        except botocore.exceptions.ClientError as e: #Check for the specific error using botocore
            print(" Could not stop {0}. ".format(i.id) + str(e)) #Print the error and the original error string
            continue                                  #continue with loop after error

    return

#Start EC2 Instances
@instances.command('start')
@click.option('--project', default=None, help='Only instances for project')

def start_instances(project):
    "Start EC2 instances"

    instances = filter_instances(project)           #Calling the filter Instances Function

    for i in instances:
        print("Starting {0}...".format(i.id))
        try:                                        #Error Check with try and Except
            i.start()
        except botocore.exceptions.ClientError as e: #Check for the specific error using botocore
            print(" Could not start {0}. ".format(i.id) + str(e)) #Print the error and the original error string
            continue                                  #continue with loop after error

    return

if __name__ == '__main__':
    cli()                         #Call the Sub Group and not Main group as before
