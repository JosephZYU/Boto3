import boto3

# For testing ONLY
# DRYRUN = True

# 🎯 Set GLOBAL variable DRYRUN to False to run it for real
# ONLY with False if you pre-test with DRYRUN = True
DRYRUN = False


# Rap the command into a function: Get_Image


def Get_Image(ec2_client):
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

    return AMI

# Rap the command into a function: Start_Ec2
# Place required parameter into the def()


def Start_Ec2(AMI, ec2_client):
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

        return ec2

    else:
        print('Your chosen AMI is NOT available.')

        # return None - indicate it didn't work succseefully
        return False


# 🎯 Refactor scrips into this format is great for Unit Testing and support for the long term
# 😎 Leave the deatiled logic ONLY within your functions
# If this ec2.py script is called on its own, then run through the following code
if __name__ == '__main__':
    ec2_client = boto3.client('ec2')

    # 🎯 Apply the def functions above
    AMI = Get_Image(ec2_client)
    ec2 = Start_Ec2(AMI=AMI, ec2_client=ec2_client)
    print(ec2.instance_id)

    # Wait and make sure until EC2 instance is running
    ec2.wait_until_running()
    print(f"Instance is {ec2.state['Name']}")

    # Trigger the termination
    ec2.terminate()
    ec2.wait_until_terminated()
    print(f"Instance is {ec2.state['Name']}")
