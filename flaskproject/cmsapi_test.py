import requests

headers={
    "Authorization":"Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcwMTkxODM4MCwianRpIjoiMWRhODk0YjctZmMxMC00YTMzLWI1OWEtMmU3ZWZiM2NjZTM0IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjlkNXNLcGJmcnJ1NTZBckh3c0p0MksiLCJuYmYiOjE3MDE5MTgzODAsImV4cCI6MTcwMTkxOTI4MH0.a6AuJzkqMRpp5LAOa6JFdN69P1JYOJBgHbicko1BmrE"
}
resp = requests.get("http://127.0.0.1:5000/cmsapi/",headers=headers)
print(resp.text)