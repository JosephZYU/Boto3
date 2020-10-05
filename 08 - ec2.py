import boto3

# For testing ONLY
# DRYRUN = True

# 🎯 Set GLOBAL variable DRYRUN to False to run it for real
# ONLY with False if you pre-test with DRYRUN = True
DRYRUN = False

ec2_client = boto3.client('ec2')

images = ec2_client.describe_images(
    Filters=[
        {
            'Name': 'name',
            'Values': [
                'amzn2-ami-hvm*',
            ]
        },
        {
            'Name': 'owner-alias',
            'Values': [
                'amazon',
            ]
        },
    ],
)

# Create a resource first
ec2_image = boto3.resource('ec2')

# Assign AMI with Image ID
# Recall: imageId = images['Images'][0]['ImageId']
AMI = ec2_image.Image(images['Images'][0]['ImageId'])

# 👀 Make sure the word available is spelled correct
if AMI.state == 'available':
    # Leverage the AMI attributes
    print(AMI.image_id)
    instance = ec2_client.run_instances(
        # ImageId='ami-0947d2ba12ee1ff75', # This is NOT a good practice to put static ID (expiration)
        ImageId=AMI.image_id,
        InstanceType='t2.micro',
        MaxCount=1,
        MinCount=1,
        DryRun=DRYRUN  # from our GLOBAL variable
    )

    # Create Boto3 resources for EC2
    ec2_instance = boto3.resource('ec2')

    # 🎯 Assign instance with instance ID to talk to
    # This will pull the InstanceId from the above run_instances() command
    ec2 = ec2_instance.Instance(instance['Instances'][0]['InstanceId'])
    print(ec2.instance_id)

    # Wait and make sure until EC2 instance is running
    # 👀 sometimes it may take longer than expected: Do NOT exit - simply wait
    ec2.wait_until_running()
    # Find out and pinrt what is the Name of the state
    print(f"Instance is {ec2.state['Name']}")

    # 🎯🎯🎯
    # 👉👉👉 The WHOLE point is to launhc instance and perform work here before termination 👈👈👈

    # Trigger the termination
    ec2.terminate()
    # Make sure it's terminated
    ec2.wait_until_terminated()
    # After the termination, we should expect a NEW state for the instance
    print(f"Instance is {ec2.state['Name']}")

else:
    print('Your chosen AMI is NOT available.')

"""
print(images) # to much info focus on the 1st ImageId 👇

Locate our ImageID dynamically: ami-00068cd7555f543d5
print(images['Images'][0]['ImageId'])
"""

"""# Define our Image ID
callable_iterator

# Print out AMI ID
print(imageId)

# Make sure it is run_instances with an s
instance = ec2_client.run_instances(
    # ImageId='ami-0947d2ba12ee1ff75', # This is NOT a good practice to put static ID (expiration)
    ImageId=imageId,
    InstanceType='t2.micro',
    MaxCount=1,
    MinCount=1,
    DryRun=DRYRUN
)

print(instance)"""
