from pinata_python import pinning
import os

apikey = "818cb551fe2da3894059"
apisecret = "81a6ab9d04f869f9cacf6dc21eb3aced6634e5d02f0861764560b36b3e96f2e3"
jwt = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySW5mb3JtYXRpb24iOnsiaWQiOiJlOWE4ZTYwZS02MDc4LTRlNGItYWNhZS00YWNlNDQwYjM4MzMiLCJlbWFpbCI6Im9iZXJvaWFyanVuMjAwOSs5OTlAZ21haWwuY29tIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsInBpbl9wb2xpY3kiOnsicmVnaW9ucyI6W3siaWQiOiJGUkExIiwiZGVzaXJlZFJlcGxpY2F0aW9uQ291bnQiOjF9LHsiaWQiOiJOWUMxIiwiZGVzaXJlZFJlcGxpY2F0aW9uQ291bnQiOjF9XSwidmVyc2lvbiI6MX0sIm1mYV9lbmFibGVkIjpmYWxzZSwic3RhdHVzIjoiQUNUSVZFIn0sImF1dGhlbnRpY2F0aW9uVHlwZSI6InNjb3BlZEtleSIsInNjb3BlZEtleUtleSI6IjgxOGNiNTUxZmUyZGEzODk0MDU5Iiwic2NvcGVkS2V5U2VjcmV0IjoiODFhNmFiOWQwNGY4NjlmOWNhY2Y2ZGMyMWViM2FjZWQ2NjM0ZTVkMDJmMDg2MTc2NDU2MGIzNmIzZTk2ZjJlMyIsImlhdCI6MTY3NjcyNTk5OX0.6EmlALGXxAOxdx6vnjNrKdMgLXF3k6az_lOQEASZGgk"




pinningobj = pinning.Pinning(apikey, apisecret, jwt)

def uploadToIPFS(filepath):
    global pinningobj
    try:
        output = pinningobj.pin_file_to_ipfs(filepath)['IpfsHash']
        print("Successfully uploaded to IPFS with hash "+output)
        return output
    except:
        print("Failure to upload for some reason")
        return ""



if __name__ == "__main__":
    print(uploadToIPFS(os.getcwd()+"/aptos_connection/aptos_testing.py"))
    print(os.getcwd())
    #print(pinningobj.pin_file_to_ipfs(os.getcwd()+"/aptos_connection/aptos_testing.py"))

"""
PINATA API
API Key: 818cb551fe2da3894059
 API Secret: 81a6ab9d04f869f9cacf6dc21eb3aced6634e5d02f0861764560b36b3e96f2e3
 JWT: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySW5mb3JtYXRpb24iOnsiaWQiOiJlOWE4ZTYwZS02MDc4LTRlNGItYWNhZS00YWNlNDQwYjM4MzMiLCJlbWFpbCI6Im9iZXJvaWFyanVuMjAwOSs5OTlAZ21haWwuY29tIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsInBpbl9wb2xpY3kiOnsicmVnaW9ucyI6W3siaWQiOiJGUkExIiwiZGVzaXJlZFJlcGxpY2F0aW9uQ291bnQiOjF9LHsiaWQiOiJOWUMxIiwiZGVzaXJlZFJlcGxpY2F0aW9uQ291bnQiOjF9XSwidmVyc2lvbiI6MX0sIm1mYV9lbmFibGVkIjpmYWxzZSwic3RhdHVzIjoiQUNUSVZFIn0sImF1dGhlbnRpY2F0aW9uVHlwZSI6InNjb3BlZEtleSIsInNjb3BlZEtleUtleSI6IjgxOGNiNTUxZmUyZGEzODk0MDU5Iiwic2NvcGVkS2V5U2VjcmV0IjoiODFhNmFiOWQwNGY4NjlmOWNhY2Y2ZGMyMWViM2FjZWQ2NjM0ZTVkMDJmMDg2MTc2NDU2MGIzNmIzZTk2ZjJlMyIsImlhdCI6MTY3NjcyNTk5OX0.6EmlALGXxAOxdx6vnjNrKdMgLXF3k6az_lOQEASZGgk
"""