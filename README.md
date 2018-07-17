# Amancoin-cryptocurrency
This project contains the code of a crypto-currency "Amancoin" and it is implemented using python programming language.
There are three nodes in this project with the names "Aman", "Ayaan", and "Nama" respectively.

Steps to run the project:
1) Import the files in an IDE.
2) Run the 3 nodes on three seperate terminals in the IDE(refer demo folder image 1).
3) Our decentralised blockchain is up and running.
4) Open Postmaster app( download from https://www.getpostman.com/ ).
5) Create 3 tabs by clicking on the plus button in postmaster app(refer demo folder image 2).
6) Initialise all the three nodes by creating its genesis block by typing 'http://127.0.0.1:5001/get_chain',
    'http://127.0.0.1:5002/get_chain' and 'http://127.0.0.1:5003/get_chain' (refer demo folder image 3).
7) Select "POST" from drop down for all the nodes and enter http://127.0.0.1:5001/connect_node (refer demo folder image 4).
8) Click on body, then select raw. After that select JSON option in node 1 (refer demo folder image 5).
9) Type the nodes addresses(of the remaining nodes) in JSON format and hit send. You will see the confirmation
   with nodes being connected(refer demo folder image 6).
10) Repeat step 9 for all the three nodes.
11) Our Blockchain is now fully connected.
12) Now change the request type to "GET" for all the nodes.
13) Mine two blocks in node one by typing http://127.0.0.1:5001/mine_block and get the chain
    by typing http:127.0.0.1:5001/get_chain (refer demo folder images 7 and 8)
14) When we type http://127.0.0.1:5002/get_chain and http://127.0.0.1:5003/get_chain in nodes 2 and 3 respectively, 
    we see that only one block is there on the chain. This is because we did not update the chain yet
    (refer demo folder images 9 and 10).
15) Now type http://127.0.0.1:5002/replace_chain and http://127.0.0.1:5003/replace_chain in nodes 2 and 3 respectively. 
    It displays the blockchain that exists in node 2 and node 3. Now type http://127.0.0.1:5001/get_chain in node 1.
    It displays the blockchain in node 1. Observe that all the three blockchains are the same. This proves the consensus 
    algorithm or the agreement algorithm meaning that all the three nodes/users agree on the longest chain that exists.
    (refer demo folder images 11, 12 and 13).
16) After proving consensus algorithm, we will now send Amancoins from node 1 to node 2.
    For this, change the requests type to post, click on body and select file type as JSON.
    Add the data in JSON format. Also note that in real life, we add the public key of the sender and reciever.
    (refer demo folder image 14).
17) When we press enter we get the transaction notification (refer demo folder image 15).
18) Amancoin is just transferred and added to a new block. But the transfer is not yet final till the time it is mined.
    To mine the block, change the request type to "GET" and type http:127.0.0.1:5001/mine_block (refer demo folder image 16).



Note: This repository uses the blockchain from my repository https://github.com/amanali1896/Blockchain-using-Python . 


Aman Ali
