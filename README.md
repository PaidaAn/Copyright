# Copyright
## 智能合約
* ### 儲存形式
  ```Solidity
  struct File {
    string content;  // 文章內容 sign和hash
    bool registered; // 是否已註冊
  }
  ```
* ### 變數
  ```Solidity
  mapping(uint256 => File) public registeredFiles; // 已註冊的文章 map[int:File]
  uint256 public totalFiles; // 文章總數、序號
  address public owner; // 合約持有者
  ```
* ### 方法
  ```Solidity
  //把合約持有者設為部署者地址
  constructor() {
      owner = msg.sender;
      totalFiles = 0;
  }

  // 檢查是否為合約持有者
  modifier onlyOwner() {
      require(msg.sender == owner, "You are not the owner!"); 
      _;
  }

  // 註冊新文章
  function registerFile(string memory content) public onlyOwner {
      totalFiles++;
      registeredFiles[totalFiles] = File(content, true); 
  }

  // 檢查文章是否已註冊
  function isWorkRegistered(uint256 fileId) public view returns (bool) {
      return registeredFiles[fileId].registered; 
  }

  // 獲取文章的內容
  function getWorkContent(uint256 fileId) public view returns (string memory) {
      return registeredFiles[fileId].content;
  }

  // 獲取文章總數
  function getToTalFiles() public view returns (uint256) {
      return totalFiles;
  }
  ```
## Python程式
* ### 智能合約
  ```Python
  INFURA_URL_MAINNET = "" # infura 節點
  account_metamask = "" # metamask 帳號
  web3 = Web3(Web3.HTTPProvider(INFURA_URL_MAINNET))
  nonce = web3.eth.get_transaction_count(account_metamask)
  #----智能合約----
  Copyright = web3.eth.contract(
      address="", # 合約的address
      abi=json.loads() # 合約的ABI
  )
  #---------------
  print(f'connection check: {web3.is_connected()}')
  ```
* ### read_txt_file()
  主要在做讀檔  
  會產生一個global變數file_path  
  以及return content
* ### registerFile()
  將檔案上傳至IPFS及登入至智能合約
  * #### 上傳至IPFS
    ```Python
    num = str(Copyright.functions.getToTalFiles().call()+1) # 取得序號
    #-------改寫檔案---------
    with open(file_path, 'w') as file:
        file.write(num+' '+sign+'\n') # 將序號及sign加入至檔案
        file.write(content)
    #-----------------------
    file_path_list = file_path.split('/')
    print("IPFS client id", client.id)
    print(file_path_list[-1]) # 會輸出檔案名稱
    res = client.add(str(file_path_list[-1])) # 加入檔案至IPFS
    print(res)
    file_hash = str(res['Hash']) # 取得hash
    print(file_hash)
    #------將檔案還原--------
    with open(file_path, 'w') as file:
        file.write(content)
    #-----------------------
    ```
  * #### 登入至智能合約
    ```Python
    Content = sign+ '\n'+ file_hash # 取得sign及hash
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
    ```
* ### isWorkRegistered()
  查詢此序號是否已註冊
  ```Python
  fileId = int(EE4.get()) # 取得要查詢的序號
  E4message = Copyright.functions.isWorkRegistered(fileId).call() # 呼叫智能合約查詢
  print(E4message)
  return E4message
  ```
* ### getWorkContent()
  查詢此序號的內容
  ```Python
  #----檢查此序號是否已註冊-----
  iswork = isWorkRegistered()
  if iswork == False:
      E2.config(state='normal')
      E2.delete(1.0,tk.END)
      E2.insert(tk.END,"無此序號")
      E2.config(state='disabled')
      return
  #---------------------------
  fileId = int(EE4.get())
  text = Copyright.functions.getWorkContent(fileId).call() # 呼叫智能合約查詢
  text_list = text.split('\n')
  file_hash = text_list[-1] # 取得hash
  print(file_hash)
  content = client.cat(file_hash) # 查詢IPFS
  ```
