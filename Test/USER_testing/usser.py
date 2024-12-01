import requests

email = "gandugamer___@gmail.com"
    
# Kickbox API details
api_key = "live_7197e2b6770723cce57486f2517b4ef3d7b7e0b4064c358ee2a265d2566c35f1" 
url = f"https://api.kickbox.com/v2/verify?email={email}&apikey={api_key}"
# Make the API request
response = requests.get(url).json()
# Check the response from Kickbox
if response['result'] not in ['deliverable', 'risky']:
    print("The provided email address is not valid or deliverable.")

else:
    print("The provided email address is valid and deliverable.")
    
