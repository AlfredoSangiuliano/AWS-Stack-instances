import boto3
from pprint import pprint

def collect_cloudformation_stacks():
    # Create a CloudFormation client
    cf_client = boto3.client('cloudformation')

    try:
        # Initialize the paginator for describe_stacks
        paginator = cf_client.get_paginator('describe_stacks')
        page_iterator = paginator.paginate()

        # Initialize an empty dictionary to store stack details
        stacks_dict = {}

        # Iterate through each page of stacks
        for page in page_iterator:
            for stack in page['Stacks']:
                stack_name = stack['StackName']
                stack_details = {
                    'StackId': stack['StackId'],
                    'StackStatus': stack['StackStatus'],
                    'CreationTime': stack['CreationTime'].isoformat(),
                    'LastUpdatedTime': stack.get('LastUpdatedTime', '').isoformat() if stack.get('LastUpdatedTime') else None,
                    'Description': stack.get('Description', ''),
                    'Parameters': {param['ParameterKey']: param['ParameterValue'] for param in stack.get('Parameters', [])},
                    'Outputs': {output['OutputKey']: output['OutputValue'] for output in stack.get('Outputs', [])},
                    'Tags': {tag['Key']: tag['Value'] for tag in stack.get('Tags', [])}
                }
                stacks_dict[stack_name] = stack_details

        return stacks_dict

    except boto3.exceptions.Boto3Error as e:
        print(f"Error collecting CloudFormation stacks: {e}")
        return None

if __name__ == "__main__":
    stacks = collect_cloudformation_stacks()
    allowed_instances = ['g4dn.2xlarge','']

for stack,values in stacks.items():
    try:
        if values['Parameters']['InstanceType'] in allowed_instances:
            print(f"Allowed instance: {values['Parameters']['InstanceType']} - Stack:{stack} - Created:{values['CreationTime'][0:19]}")
        else:
            print(f"!!! Not allowed instance !!!: {values['Parameters']['InstanceType']} - Stack:{stack} - Created:{values['CreationTime'][0:19]}")
    except:
        pass
