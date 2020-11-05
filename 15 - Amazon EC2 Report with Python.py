"""
Nov 05 2020 - JosephYu
⛳ Create ALL EC2 instances into a CSV/Excel file
"""


import boto3
import csv


def Get_Instances():
    """
    1 - Get EC2 instance info
    """
    ec2 = boto3.client('ec2')
    response = ec2.describe_instances()

    # Locate the 1st designation of Reservations - subject to change👈
    return response['Reservations'][0]['Instances']


def CSV_Writer(content, header):
    """
    2 - Write output into CSV
    """
    with open('export.csv', 'w') as csvFile:

        # Create writer
        writer = csv.DictWriter(csvFile, fieldnames=header)
        writer.writeheader()

        # Use writer to take each row and write the file
        for row in content:
            writer.writerow(row)


# Put the glue to combine functions together
if __name__ == "__main__":

    instances = Get_Instances()

    # 🧐 Define the elements we are interested in 👈
    header = ['InstanceId', 'InstanceType', 'State', 'PublicIpAddress']

    # Initialize empty array for our content
    data = []

    # Loop through the instances we get then pass onto the writer
    for instance in instances:
        print(f"Adding instance {instance['InstanceId']} to file")
        data.append(
            {
                "InstanceId": instance['InstanceId'],
                "InstanceType": instance['InstanceType'],
                "State": instance['State']['Name'],
                "PublicIpAddress": instance['PublicIpAddress']
            }
        )

    # Finish the output
    CSV_Writer(content=data, header=header)
