import requests
import json
def send_fcm(message_body,User_id,DeviceToken,DT,Ntype):
    fcm_url = 'https://fcm.googleapis.com/fcm/send'
    fcm_headers = {'Authorization': 'key=AAAAIj6-LSk:APA91bFjjt_exf7tX_cLR5IpM4-pHtFcD1LUAQZJN9MJ0w1wc-U_xOdG_J5G4x77N8sYH85r82mh9iucVo3Y-lomGfBMhaSGrVUrby7Np3kLQCCPF4tS4XE3j0On_9jIL1lhIDd5Dptz', 'Content-Type': 'application/json; charset=utf-8'} 

    message_title="Beach+"

    if DT=='Android':
        payload = {"data":{"title":message_title,"message":message_body,"User_id":User_id,"type":Ntype}, "to":DeviceToken}
    else:
        payload = {"notification":{"title":message_title,"body":message_body,"User_id":User_id,"type":Ntype,"apns":{"title":message_body}},"registration_ids":[DeviceToken]}
    
    r = requests.post(fcm_url, data=json.dumps(payload), headers=fcm_headers)
    
    return True