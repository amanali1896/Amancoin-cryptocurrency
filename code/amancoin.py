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
from uuid import uuid4
from urllib.parse import urlparse

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
        self.node = set{} #nodes are in a set

    def create_block(self, proof, previous_hash):  # this is used to create a block and append it to blockchain
        block = {'index': len(self.chain) + 1,
                 'timestamp': str(datetime.datetime.now()),
                 'proof': proof, 'previous_hash': previous_hash
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

    def add_transactions(self, sender, receiver, amount):
        self.transactions.append({'sender': sender,
                                   'receiver':receiver,
                                   'amount':amount}) # we create a dictionary and append it to the list
        previous_block = self.get_previous_block() #gets the previous block using the method defined above
        return previous_block['index'] + 1 #updates the block index by 1.This new block will have the transactions in it.  

    def add_node(self, address):
        parsed_url = urlparse(address) #parsing the address, we get a dictionary with scheme, netloc, path, param, query & fragment 
        self.nodes.add(parsed_url.netloc) # netloc key has the address so we return that along with port number

    def replace_chain(self): #since in a specific node only this function would be called, we have self as a parameter.
        network = self.nodes #set of nodes all around the world
        longest_chain = None #initialise it to none as we don't have any idea of the length now
        

# Part2-Mining the blockchain class. 

# creating the Web App
app = Flask(__name__) # creating the app

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
    block = blockchain.create_block(proof,previous_hash) #new block is created based on the information that's given.
                                                         #information is Proof of work and the hash of the previous block
    response = {'message':'The block was sucessfully mined.',
                'index':block['index'],
                'timestamp': block['timestamp'],
                'proof':block['proof'],
                'previous_hash':block['previous_hash']}  #respose is the message we type if the block is mined                                                       

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
#running the app
app.run(host = '0.0.0.0', port = 5000 )


#Part 3 - Decentralizing our Blockchain
