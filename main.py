import subprocess


def handler(event, context):
    try:
        subprocess.run(['scrapy', 'crawl', 'bank_indonesia_transaction_rate'], check=True)
    except Exception as e:
        return {
            'statusCode': 500,
            'message': f'Lambda function encountered an error: {str(e)}',
        }
    
    return {
        'statusCode': 200,
        'message': f'Lambda function invoked successfully.',
    }