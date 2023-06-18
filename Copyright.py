import json
from tkinter import filedialog
from web3 import Web3
import web3
import tkinter as tk
import ipfshttpclient

# 創建視窗
window = tk.Tk()
window.title("hw")
window.geometry("800x600")

def read_txt_file():
    global E1,E2,E3,E4,file_path
    try:
        file_path = filedialog.askopenfilename()
        print(file_path)
        with open(file_path, 'r') as file:
            content = file.read()
            print(content)
            E2.config(state='normal')
            E2.delete(1.0,tk.END)
            E2.insert(tk.END,content)
            E2.config(state='disabled')
            E1message = "讀檔成功"
            E1.configure(text=E1message)
            return content
    except FileNotFoundError:
        print("找不到指定的檔案！")
        E1message = "找不到指定的檔案！"
        E1.configure(text=E1message)
        return ""
    except Exception as e:
        print(f"讀取檔案時發生錯誤：{str(e)}")
        E1message = "讀取檔案時發生錯誤："+str(e)
        E1.configure(text=E1message)
        return ""

INFURA_URL_MAINNET = "https://goerli.infura.io/v3/930c21de2cab4421acaa8853eda5746d" # infura 節點
account_metamask = "" # metamask 帳號


web3 = Web3(Web3.HTTPProvider(INFURA_URL_MAINNET))
nonce = web3.eth.get_transaction_count(account_metamask)
Copyright = web3.eth.contract(
    address="0x6200B949a0B8bF5f65e33240B821e1084c3BD5DC", # 合約的address
    # 合約的ABI
    abi=json.loads('[{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[],"name":"getToTalFiles","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"fileId","type":"uint256"}],"name":"getWorkContent","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"fileId","type":"uint256"}],"name":"isWorkRegistered","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"string","name":"content","type":"string"}],"name":"registerFile","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"registeredFiles","outputs":[{"internalType":"string","name":"content","type":"string"},{"internalType":"bool","name":"registered","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalFiles","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}]')
)
print(f'connection check: {web3.is_connected()}')

global E3message,E4message,E1message
E1message = ""
E3message = ""
E4message = ""
fileId = 0
client = ipfshttpclient.connect('/ip4/127.0.0.1/tcp/5001')

def getTxt():
    global content
    content = read_txt_file()
    E3message = ""
    E3.configure(text=E3message)

def registerFile():
    if file_path == '':
        E3message = "請選擇檔案"
        E3.configure(text=E3message)
        return
    sign = EE3.get()
    if sign == '':
        E3message = "請加入簽名"
        E3.configure(text=E3message)
        return
    try:
        num = str(Copyright.functions.getToTalFiles().call()+1)
        with open(file_path, 'w') as file:
            file.write(num+' '+sign+'\n')
            file.write(content)
        file_path_list = file_path.split('/')
        print("IPFS client id", client.id)
        print(file_path_list[-1])
        res = client.add(str(file_path_list[-1]))
        print(res)
        file_hash = str(res['Hash'])
        print(file_hash)
        with open(file_path, 'w') as file:
            file.write(content)
    except:
        E3message = "add IPFS fail"
        E3.configure(text=E3message)
        return
    try:
        Content = sign+ '\n'+ file_hash
        # 建構交易
        tx = Copyright.functions.registerFile(Content).build_transaction({
            'from': account_metamask, # 發送交易的帳戶地址
            'nonce': nonce, # 計數器
            'gas': 200000 # gas limit
        })

        # 私鑰對交易簽名
        signed_tx = web3.eth.account.sign_transaction(tx, private_key = "")  # 使用合约所有者的私鑰

        # 將已簽名的交易發送出去
        tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        print(f'Transaction hash: {web3.to_hex(tx_hash)}')

        # 等待交易確認
        receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
        print(f'Transaction receipt: {receipt}')
        E3message = "add copyright success"
    except:
        E3message = "add copyright fail"
    E3.configure(text=E3message)

# 檢查Copyright
def isWorkRegistered():
    fileId = int(EE4.get())
    E4message = Copyright.functions.isWorkRegistered(fileId).call()
    print(E4message)
    E4.configure(text=str(E4message))
    return E4message

# 取得文章
def getWorkContent():
    iswork = isWorkRegistered()
    if iswork == False:
        E2.config(state='normal')
        E2.delete(1.0,tk.END)
        E2.insert(tk.END,"無此序號")
        E2.config(state='disabled')
        return
    fileId = int(EE4.get())
    text = Copyright.functions.getWorkContent(fileId).call()
    text_list = text.split('\n')
    file_hash = text_list[-1]
    print(file_hash)
    content = client.cat(file_hash)
    E2.config(state='normal')
    E2.delete(1.0,tk.END)
    E2.insert(tk.END,content)
    E2.config(state='disabled')

# 創建按鈕
B1 = tk.Button(text= "讀檔", command = getTxt)
B1.place(x = 50, y = 50)
B2 = tk.Button(text= "下載文章", command = getWorkContent)
B2.place(x = 50, y = 350)
B3 = tk.Button(text= "上傳&添加版權", command = registerFile)
B3.place(x = 50, y = 150)
B4 = tk.Button(text= "檢查版權", command = isWorkRegistered)
B4.place(x = 50, y = 250)

global E1,E2,E3,E4,EE3
E1 = tk.Label(text=E1message)
E1.place(x=50, y=100)

#v=tk.Scrollbar(orient='vertical')
E2 = tk.Text(#state='disabled',
             height=35,)
             #yscrollcommand=v.set)

E2.place(x=200, y=50)

E3 = tk.Label(text=E3message)
E3.place(x=50, y=200)
EE3 = tk.Entry()
EE3.place(x=50, y=175)

E4 = tk.Label(text=E4message)
E4.place(x=50, y=300)
EE4 = tk.Entry()
EE4.place(x=50, y=225)

# 啟動視窗主迴圈
window.mainloop()
