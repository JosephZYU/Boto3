import boto3

# Define routine function for future usage


def CreateBucket(name):
    s3_client = boto3.client('s3')

    # Add try block to be more user-friendly
    try:
        s3_client.create_bucket(Bucket=name)
        return True

    # Add exception if bucket exists
    except s3_client.exceptions.BucketAlreadyExists:
        print(
            f"The bucket name {name} is taken, please choose a different name")
        return False


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

    # Check if the encryption already exists before Encrypting
    try:
        s3_client.get_bucket_encryption(Bucket=bucket.name)
        print("Encryption already set.")

    except s3_client.exceptions.ClientError as error:
        if "ServerSideEncryptionConfigurationNotFoundError" in str(error):
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

        # Make sure to raise ALL other errors exhaustively
        else:
            raise error


if __name__ == "__main__":
    """
    🤏 Use glue to tie all together
    """
    Name = 'testbucketforencryption-bs3-jyu'  # all lower_case, must be unique
    # Name = 'testbucketforencryption-bs3-jyu'  # all lower_case, must be unique

    # If Create Bucket is True (the new bucket name does NOT duplicate)
    if CreateBucket(Name):
        EnforceS3Encryption(Name)  # apply the Enforce function on name
    # DeleteBucket(Name)
    # print(f"Bucket - {Name} has been DELETED.")
