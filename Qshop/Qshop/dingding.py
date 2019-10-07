import json,requests
# 添加机器人的webhook地址
url="https://oapi.dingtalk.com/robot/send?access_token=f36bbba055c8cc9cd5cfad6ef4caf5a8cc54975ce61c29be6979fdfe9a5efc5f"
headers={
    "Content-Type":"application/json",
    "Charset":"utf-8"    #编码方式
}
requests_data={
    "msgtype":"text",
    "text":{
        "content":"相信人类的世界，相信人类自己"   #回复内容
    },
    "at":{
        "atMobiles":[],
    },
    "isAtAll":True
}
sendData=json.dumps(requests_data)
response=requests.post(url=url,headers=headers,data=sendData)
content=response.json()
print(content)

