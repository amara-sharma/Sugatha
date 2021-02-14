import requests
url = "https://www.fast2sms.com/dev/bulk"
payload = "sender_id=FSTSMS&message=test&language=english&route=p&numbers=8297060268,8886106173"
headers = {
'authorization': "aIqhB6PvgRMZoV0TmQf9KNzXWlSxk2JpCAO1yHju7EFnwrtc5DwOdzSYUnEuGhb38rtMe02lfTjgXDs5",
'Content-Type': "application/x-www-form-urlencoded",
'Cache-Control': "no-cache",
}
response = requests.request("POST", url, data=payload, headers=headers)
print(response.text)

