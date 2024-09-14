import requests, json
import pandas as pd
import configparser, config_enum

config_object = configparser.ConfigParser()
with open("config.ini","r") as file_object:
    config_object.read_file(file_object)
    
page_id = config_object['DEFAULT'][config_enum.default_config.page_id.value]
post_id = config_object['DEFAULT'][config_enum.default_config.post_id.value]
access_token = config_object['DEFAULT'][config_enum.default_config.access_token.value]

url = f'https://graph.facebook.com/v20.0/{page_id}_{post_id}/comments?access_token={access_token}'

response = requests.request("GET", url)

# save name, time, message in excel file
data = json.loads(response.text)

# create object with only name, time, message
def get_comment(comment):
    return {
        'name': comment['from']['name'],
        'time': comment['created_time'],
        'message': comment['message']
    }

excel_data = list(map(get_comment, data['data']))
df = pd.DataFrame(excel_data)
print(df)
# df.to_excel('comments.xlsx', index=False)