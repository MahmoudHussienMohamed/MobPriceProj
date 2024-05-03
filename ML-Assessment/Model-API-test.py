import requests

# Send a GET request to a URL
payload = {'key1': 'value1', 'key2': 'value2'}
response = requests.get('https://local:5000/predict_price_range', params=payload)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Print the response content
    print(response.text)
else:
    # Print an error message
    print("Error:", response.status_code)
