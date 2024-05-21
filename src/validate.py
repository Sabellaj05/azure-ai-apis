import re

def is_endpoint_valid(endpoint) -> bool:
    if len(endpoint) == 0:
        print("wrong")
        return False

    ### [fix] ###
    # if re.search(r"^https://\S+\.cognitiveservices\.azure\.com/?$", endpoint):
    #     print("passed")
    #     return True

    # else:
    #     print(f"Invalid value for endpoint: {endpoint}")
    #     print("Should hava this form: https://<vision-resource-name>.cognitiveservices.azure.com")
    #     return False
    return True

def is_key_valid(key) -> bool:
    if len(key) == 0:
        print("Missing vision key")
        return False
    
    if len(key) != 32 or not all(c in "0123456789abcdefABCDEF" for c in key): # check if all values are hex compliant
        print(f"Invalid value for key: {key}")
        print("Should be a 32-character HEX number.")
        return False

    return True
