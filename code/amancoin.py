# Amancoin-cryptocurrency
# Install Flask version 0.12.2 by using pip install Flask==0.12.2
# Install Postman HTTP client: https://www.getpostman.com/
# Install requests using pip install requests == 2.19.1

# Importing libraries
import datetime  # since each block will have its own time
import hashlib  # to hash the block
import json  # encode the blocks before hashing
# Flask is used to create an object which will be the web-app
# jsonify is used to return the response of the requests
from flask import Flask, jsonify, request #request is for having decentralisation
import requests
from uuid import uuid4 #used to assign unique addresses
from urllib.parse import urlparse #used to parse the url

# Part 1-defining the blockchain class
class Blockchain:  # Helps to create blocks

    def __init__(self):  # Constructor method
        self.chain = []  # empty list. supposed to contain the list of blocks
        self.transactions = [] # transactions must be created here, 
                         # not after below function, Since we first have transactions and then add it to a block
        self.create_block(proof=1, previous_hash='0')
        # proof of work is initialised to 1 and previous hash is initialised to 0.
        # As hash is encoded we initialised it with single quotes
        # This is the genesis block
        self.node = set() #nodes are in a set

    def create_block(self, proof, previous_hash):  # this is used to create a block and append it to blockchain
        block = {'index': len(self.chain) + 1,
                 'timestamp': str(datetime.datetime.now()),
                 'proof': proof, 'previous_hash': previous_hash,
                 'transactions':self.transactions}
        # 'index':chain+1 since we are creating a new block
        # 'timestamp': string because it will give no issues while using JSON.
        #  'proof': from proof of work function we pass proof as parameter
        # and that is what is equated to the key(proof)
        # transactions are equated to the transactions list
        self.transactions = [] #emptying the list since new transactions are added to a new block
        self.chain.append(block)  # add the blocks to the chain(list).
        return block  # return the parameters of the dictionary as it can be used to mine further blocks

    def get_previous_block(self):
        return self.chain[-1]
        # returns the last block in the chain.

    def proof_of_work(self, previous_proof):
        new_proof = 1

        # every nonce/proof of work must start with 1. It is then incremented to satisfy the target requirement
        check_proof = False
        while check_proof is False:
            hash_operation = hashlib.sha256(str(new_proof ** 2 - previous_proof ** 2).encode()).hexdigest()
            # we have '-' operation  because it is asymmetrical i.e a-b!=b-a.
            # we are squaring it just to increase the difficulty
            # encode() is added so that sha256 accepts the encoded format. It adds 'b' to the result of a-b
            if hash_operation[:4] == '0000': # setting the target
                check_proof = True #exit the loop
            else:
                new_proof += 1 #increase the new_proof and try to recalculate the hash
                               #til the target is met.
        return new_proof

    def hash(self, block): #this function returns the cryptographic hash of the function
        encoded_block = json.dumps(block, sort_keys = True).encode() 
        #JSON.dumps: we have to use dumps since we have to convert it to Json format. 
        #'sort_keys': JSON may have several keys and in order to view them you might 
        #want to have the keys sorted in ascending order so that 
        #you can find the key you are looking easily for in the JSON file. 

        #encode(): We encode the block.
        return hashlib.sha256(encoded_block).hexdigest() #retuns hash in hexadecimal format 
   
    def is_chain_valid(self, chain):
        previous_block = chain[0] #initialise the block||genesis block
        block_index = 1
        while block_index<len(chain):
            block = chain[block_index]
            if block['previous_hash'] != self.hash(previous_block):
                return False #if the hashes don't match, then it is not a valid chain
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(str(proof ** 2 - previous_proof ** 2).encode()).hexdigest()
            if hash_operation[:4]!='0000':
                return False #fails if it doesn't meet the target kept by the problem
            previous_block = block #points previous block to the current block
            block_index +=1

        return True #if it wasn't false til now then it is valid, and hence true

    def add_transaction(self, sender, receiver, amount):
        self.transactions.append({'sender': sender,
                                   'receiver':receiver,
                                   'amount':amount}) # we create a dictionary and append it to the list
        previous_block = self.get_previous_block() #gets the previous block using the method defined above
        return previous_block['index'] + 1 #updates the block index by 1.This new block will have the transactions in it.  

    def add_node(self, address):
        parsed_url = urlparse(address) #parsing the address, we get a dictionary with scheme, netloc, path, param, query & fragment 
        self.nodes.add(parsed_url.netloc) # netloc key has the address so we return that along with port number

    def replace_chain(self): #used to find the longest chain. 
        #since in a specific node only this function would be called, we have self as a parameter.
        network = self.nodes #set of nodes all around the world
        longest_chain = None #initialise it to none as we don't have any idea of the length now
        max_length = len(self.chain) #initialise the variable to the length of the chain
        for node in network:
            response = requests.get(f'http://{node}/get_chain')#f-string syntax introduced in python 3.6. prints the  ip address
            if response.status_code == 200: #Success code for http. only for positive executions of requests we will consider
                length = response.json()['length']
                chain = response.json()['chain']
                if length > max_length and self.is_chain_valid(chain): # if this node's length is greater than the max length & 
                    max_length = length                                # if the chain is valid in the node
                    longest_chain = chain                         # the longest chain becomes the current node's chain(very important)

        if longest_chain: #if the longest_chain has changed 
            self.chain = longest_chain #update the chain to the longest chain
            return True
        return False #if there is no change in the longest_chain. i.e its value is still null.
# Part2-Mining the blockchain class. 

# creating the Web App
app = Flask(__name__) # creating the app

#creating an address for the node on Port 5000
    #created to give a miner incentives & to have an unique address
node_address = str(uuid4()).replace('-',' ') #this is the address of the node on port 5000
                                             # replaces - with a blank.


# mining the blockchain
blockchain = Blockchain() #creating our first blockchain
#mining a new block
@app.route('/mine_block',methods=['GET']) #Flask syntax,mine_block is the function that calls app, 
                                          # routing address and the type of method.

def mine_block():
    previous_block = blockchain.get_previous_block() #gets the last block of the chain
    previous_proof = previous_block['proof']#gets the proof of work of the previous block
    proof = blockchain.proof_of_work(previous_proof) #proof of new block is calculated based on the previous block's proof of work
    previous_hash = blockchain.hash(previous_block) #calculates the hexadecimal hash
    blockchain.add_transaction(sender = node_address, receiver = 'Aman', amount = 5) #5 coins as incentive to the miner
    block = blockchain.create_block(proof,previous_hash) #new block is created based on the information that's given.
                                                         #information is Proof of work and the hash of the previous block
    response = {'message':'The block was sucessfully mined.',
                'index':block['index'],
                'timestamp': block['timestamp'],
                'proof':block['proof'],
                'previous_hash':block['previous_hash'],
                'transactions':block['transactions']}  #respose is the message we type if the block is mined                                                       

    return jsonify(response), 200 #jsonify returns the response in json format, 200 is the 'OK' HTTP status code

#getting the full blockchain

@app.route('/get_chain',methods=['GET'])

def get_chain():
    response = {'chain':blockchain.chain,
                'length':len(blockchain.chain)} #response has two keys chain and length

    return jsonify(response), 200

#checking if the blockchain is valid
@app.route('/is_valid',methods=['GET'])
def is_valid():
    is_valid = blockchain.is_chain_valid(blockchain.chain)
    if is_valid:
        response = {'message':'The blockchain is valid.'}
    else:
        response = {'message':'There is an error.'}
    return jsonify(response), 200

#adding a new transaction to the blockchain
@app.route('/add_transaction',methods=['POST']) #post modifies some data and then retrieves it 
def add_transaction():
    json = request.get_json() #posts json file in postman
    transaction_keys = ['sender', 'receiver', 'amount']
    if not all (key in json for key in transaction_keys):
        return 'There are some elements that are missing', 400 #400 is the error code
    index = blockchain.add_transaction(json['sender'], json['receiver'], json['amount']) # accessing the values of json
    response = {'message':f'This transaction will be added to Block {index}'}  #(which is a dictionary), and send it to the method   
    return jsonify(response), 201 #success status code for post request.

#Part 3 - Decentralizing our Blockchain

# connecting new nodes
@app.route('/connect_node',methods=['POST'])
def connect_node():
      json = request.get_json() 
      nodes = json.get('nodes') # nodes in the json file
      if nodes is None:
        return "No node",400 #if there are no nodes, return error
      for node in nodes:
        blockchain.add_node(node)

      response = {'message':'All the nodes are now connected. Amancoin now has nodes:',
                   'total_nodes':list(blockchain.nodes)}
      return jsonify(response), 201

# Replacing the chain by the longest chain if needed
@app.route('/replace_chain',methods=['GET'])
def replace_chain():
    is_chain_replaced = blockchain.replace_chain() # method returns true/false and replaces the chain variable of the object
    if is_chain_replaced:
        response = {'message':'Yes the nodes had different chains, so the chain was replaced by the longest one',
                    'new_chain':blockchain.chain} # displaying the chain which is updated by the replace chain method
    else:
        response = {'message':'All good. The chain is the largest one.',
                    'actual_chain':blockchain.chain}
    return jsonify(response), 200

#running the app
app.run(host = '0.0.0.0', port = 5000 )



