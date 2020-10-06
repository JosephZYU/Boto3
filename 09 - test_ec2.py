from unittest import mock
from ec2 import Get_Image, Start_Ec2
import boto3

# Create Mock responses


class MockResponse:
    """
    Class to mock urllib3 response
    """

    def __init__(self, status_code, body):
        self.status_code = status_code
        self.body = body

    def __iter__(self) -> any:
        """
        Need to implement iterable in order to be representable
        """
        for value in [self, self.body]:
            yield value


# Create class for Unit Test

class TestEc2:
    # 🛑 Add a patch first to intercept
    # Instead of going out to the Internet, use this infomration here
    @mock.patch('botocore.client.BaseClient._make_request')
    def test_get_image(self, mock_api):
        """
        Test the Get Image function
        MockResponse() from class above
        200: Success
        """
        mock_api.return_value = MockResponse(
            200,
            {
                'Images': [
                    {
                        'Architecture': 'i386',
                        'CreationDate': 'string',
                        'ImageId': 'string',
                        'ImageLocation': 'string',
                        'ImageType': 'machine',
                        'Public': True,
                        'KernelId': 'string',
                        'OwnerId': 'string',
                        'Platform': 'Windows',
                        'ProductCodes': [
                            {
                                    'ProductCodeId': 'string',
                                    'ProductCodeType': 'devpay'
                            },
                        ],
                        'RamdiskId': 'string',
                        'State': 'available',
                        'BlockDeviceMappings': [
                            {
                                'DeviceName': 'string',
                                'VirtualName': 'string',
                                'Ebs': {
                                    'DeleteOnTermination': True,
                                    'Iops': 123,
                                    'SnapshotId': 'string',
                                    'VolumeSize': 123,
                                    'VolumeType': 'standard',
                                    'Encrypted': True,
                                    'KmsKeyId': 'string'
                                },
                                'NoDevice': 'string'
                            },
                        ],
                        'Description': 'string',
                        'EnaSupport': True,
                        'Hypervisor': 'ovm',
                        'ImageOwnerAlias': 'string',
                        'Name': 'string',
                        'RootDeviceName': 'string',
                        'RootDeviceType': 'ebs',
                        'SriovNetSupport': 'string',
                        'StateReason': {
                                'Code': 'string',
                                'Message': 'string'
                        },
                        'Tags': [
                            {
                                'Key': 'string',
                                'Value': 'string'
                            },
                        ],
                        'VirtualizationType': 'hvm'
                    },
                ]
            }
        )

        ec2_client = boto3.client('ec2')
        assert Get_Image(ec2_client)
