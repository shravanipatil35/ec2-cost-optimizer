import boto3
from datetime import datetime, timedelta

ec2 = boto3.client('ec2')
cloudwatch = boto3.client('cloudwatch')
dynamodb = boto3.resource('dynamodb')

table = dynamodb.Table('CostReports')


def lambda_handler(event, context):
    
    instances = ec2.describe_instances()
    
    for reservation in instances['Reservations']:
        for instance in reservation['Instances']:
            
            instance_id = instance['InstanceId']
            print(f"Checking: {instance_id}")
            
            tags = instance.get('Tags', [])
            tag_found = False
            
            for tag in tags:
                if tag['Key'] == 'AutoStop' and tag['Value'] == 'true':
                    tag_found = True
            
            if not tag_found:
                print("Skipping (no tag)")
                continue
            
            end = datetime.utcnow()
            start = end - timedelta(hours=1)
            
            metrics = cloudwatch.get_metric_statistics(
                Namespace='AWS/EC2',
                MetricName='CPUUtilization',
                Dimensions=[
                    {
                        'Name': 'InstanceId',
                        'Value': instance_id
                    }
                ],
                StartTime=start,
                EndTime=end,
                Period=300,
                Statistics=['Average']
            )
            
            datapoints = metrics['Datapoints']
            
            if datapoints:
                avg_cpu = sum(d['Average'] for d in datapoints) / len(datapoints)
                print(f"Avg CPU: {avg_cpu}")
                
                if avg_cpu < 5:
                    print("Stopping instance")
                    ec2.stop_instances(InstanceIds=[instance_id])
                    
                    table.put_item(
                        Item={
                            'resourceId': instance_id,
                            'timestamp': str(datetime.utcnow()),
                            'action': 'stopped',
                            'cpu': str(avg_cpu)
                        }
                    )
            
            current_hour = datetime.utcnow().hour
            
            if current_hour == 9:
                print("Starting instance")
                ec2.start_instances(InstanceIds=[instance_id])
                
                table.put_item(
                    Item={
                        'resourceId': instance_id,
                        'timestamp': str(datetime.utcnow()),
                        'action': 'started',
                        'cpu': 'N/A'
                    }
                )