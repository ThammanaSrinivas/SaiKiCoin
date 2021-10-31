from django.shortcuts import render

from time import time
import hashlib
import json
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
class SaiKiCoinBlockChain:
    def __init__(self):
        self.chain = []
        self.pending_transactions = []

        self.create_block(nonce=1,previous_hash='SaiKi.K')

    def add_transaction(self,sender,receiver,amount):
        transaction = {
            "sender": sender,
            "receiver": receiver,
            "amount": amount
        }
        self.pending_transactions.append(transaction)

        return len(self.chain)

    def create_block(self,nonce=0,previous_hash=None):
        block = {
            'index': len(self.chain),
            'timestamp': time(),
            'transactions': self.pending_transactions,
            'nonce': nonce,
            'previous_hash': previous_hash or self.get_previous_block_hash()
        }
        self.pending_transactions = []
        self.chain.append(block)

        return block

    def hash_(self,block):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    def get_previous_block_hash(self):
        return self.hash_(self.chain[-1])

    def no_pending_transactions(self):
        return len(self.pending_transactions)==0

    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if block['previous_hash'] != self.hash_(previous_block):
                return False
            previous_nonce = previous_block['nonce']
            nonce = block['nonce']
            hash_value = hashlib.sha256(str(nonce ** 2 - previous_nonce ** 2).encode()).hexdigest()
            if hash_value[:2] != '00':
                return False
            previous_block = block
            block_index += 1
        return True

    def proof_of_work(self,previous_nonce):
        new_nonce = 1
        check_nonce = False
        while check_nonce is False:
            hash_operation = hashlib.sha256(str(new_nonce ** 2 - previous_nonce ** 2).encode()).hexdigest()
            if hash_operation[:2] == '00':
                check_nonce = True
            else:
                new_nonce += 1
        return new_nonce

    def get_previous_nonce(self):
        return self.chain[-1]['nonce']


block_chain = SaiKiCoinBlockChain()

def mine_block(request):
    if request.method == 'GET':
        if(block_chain.no_pending_transactions()):
            response_no_pending_transactions = {'message': 'There are no pending transactions'}
            return JsonResponse(response_no_pending_transactions)
        previous_hash = block_chain.get_previous_block_hash()
        previous_nonce = block_chain.get_previous_nonce()
        nonce = block_chain.proof_of_work(previous_nonce)
        block = block_chain.create_block(nonce,previous_hash)
        response = {'message': 'Congratulations, you just mined a block!',
                    'index': block['index'],
                    'timestamp': block['timestamp'],
                    'nonce': block['nonce'],
                    'previous_hash': block['previous_hash']}
    return JsonResponse(response)

def get_chain(request):
    if request.method == 'GET':
        response = {'chain': block_chain.chain,
                    'length': len(block_chain.chain)}
    return JsonResponse(response)

@csrf_exempt
def add_transaction(request): #New
    if request.method == 'POST':
        received_json = json.loads(request.body)
        transaction_keys = ['sender', 'receiver', 'amount']
        if not all(key in received_json for key in transaction_keys):
            return 'Some elements of the the transaction are missing', HttpResponse(status=400)
        index = block_chain.add_transaction(received_json['sender'], received_json['receiver'], received_json['amount'])
        response = {'message': f'This transaction will be added to Block {index}'}
    return JsonResponse(response)

def is_valid(request):
    if request.method == 'GET':
        is_valid = block_chain.is_chain_valid(block_chain.chain)
        if is_valid:
            response = {'message': 'All good. The Blockchain is valid.'}
        else:
            response = {'message': 'Houston, we have a problem. The Blockchain is not valid.'}
    return JsonResponse(response)