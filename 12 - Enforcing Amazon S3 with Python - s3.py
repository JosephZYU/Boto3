import boto3

# Define routine function for future usage


def CreateBucket(name):
    s3_client = boto3.client('s3')
    s3_client.create_bucket(Bucket=name)
    return True


def DeleteBucket(name):
    s3_client = boto3.client('s3')
    s3_client.delete_bucket(Bucket=name)
    return True


def EnforceS3Encryption(name):

    # Start with S3 resource
    s3 = boto3.resource('s3')
    s3_client = boto3.client('s3')

    # Create our bucket object
    bucket = s3.Bucket(name)
    print(f"Encrypting {bucket.name} at S3 bucket creation by JYU")

    # Perform the Encryption
    response = s3_client.put_bucket_encryption(
        # leverage bucket object, grab the name
        Bucket=bucket.name,

        # Put the Encryption config
        ServerSideEncryptionConfiguration={
            'Rules': [
                {
                    'ApplyServerSideEncryptionByDefault': {
                        'SSEAlgorithm': 'AES256'
                    }
                }
            ]
        }
    )
    print(response)


if __name__ == "__main__":
    """
    🤏 Use glue to tie all together
    """
    Name = 'testbucketforencryption-bs3-jyu'  # all lower_case, must be unique
    CreateBucket(Name)  # apply the CreateBucket function
    EnforceS3Encryption(Name)  # apply the Enforce function on name
    # DeleteBucket(Name)

