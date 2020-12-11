import boto3
import csv


def Get_Instances():
    ec2 = boto3.client('ec2')
    paginator = ec2.get_paginator('describe_instances')
    page_iterator = paginator.paginate()
    response = []
    for page in page_iterator:
        for instance in page['Reservations'][0]['Instances']:
            response.append(instance)
    return response


def CSV_Writer(content, header):
    with open('export.csv', 'w') as csvFile:
        writer = csv.DictWriter(csvFile, fieldnames=header)
        writer.writeheader()
        for row in content:
            writer.writerow(row)


if __name__ == "__main__":
    instances = Get_Instances()
    header = ['InstanceId', 'InstanceType', 'State', 'PublicIpAddress']
    data = []
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
    CSV_Writer(content=data, header=header)
