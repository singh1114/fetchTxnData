import requests
from chain_constants import ChainConstants

TOTAL_TXNS_BATCHES = 115

def get_max_ancestors():
    final_ancestor_dict = fetch_parent_ancestors()
    print(get_largest_length(final_ancestor_dict))

def fetch_parent_ancestors():
    # FIXME Issue in this function.
    final_ancestor_dict = dict()
    txn_data_dict = get_all_tx_data()
    for txid in txn_data_dict.keys():
        for input_tx in txn_data_dict[txid]:
            if txn_data_dict.get(input_tx):
                if final_ancestor_dict.get(txid):
                    final_ancestor_dict[txid] = final_ancestor_dict[txid].append(input_tx)
                else:
                    final_ancestor_dict[txid] = [input_tx]
    return final_ancestor_dict

def get_all_tx_data():
    block_hash = get_block_hash()
    endpoint = get_txn_data_endpoint(block_hash, 0)
    response = requests.get(endpoint)
    return prepare_txn_data_list(response, block_hash)

def prepare_txn_data_list(response, block_hash):
    txn_data_dict = dict()
    current_index = 1
    while True:
        txn_data = response.json()
        for txn in txn_data:
            current_txn_id = txn.get('txid')
            inputs = [a.get('txid') for a in txn.get('vin')]
            txn_data_dict[current_txn_id] = inputs
        if current_index is TOTAL_TXNS_BATCHES:
            break
        current_index = current_index + 1
        txn_data = get_tx_data_using_start_index(block_hash, current_index * 25)
    return txn_data_dict

def get_tx_data_using_start_index(block_hash, start_index):
    endpoint = get_txn_data_endpoint(block_hash, start_index)
    response = requests.get(endpoint)

def get_first_tx_id():
    block_hash = get_block_hash()
    endpoint = get_first_txn_endpoint(block_hash)
    response = requests.get(endpoint)
    if response.status_code is ChainConstants.VALID_STATUS_CODE:
        return response.text, block_hash
    else:
        # TODO raise an exception
        print("Unable to fetch data")

def get_block_hash():
    endpoint = get_block_data_using_height_endpoint()
    response = requests.get(endpoint)
    if response.status_code is ChainConstants.VALID_STATUS_CODE:
        return response.text
    else:
        # TODO raise an exception
        print("Unable to fetch data")

def get_first_txn_endpoint(block_hash):
    endpoint = ChainConstants.BASE_DNS + ChainConstants.FETCH_TXN_ENDPOINT
    return endpoint.format(block_hash)

def get_block_data_using_height_endpoint():
    endpoint = ChainConstants.BASE_DNS + ChainConstants.BLOCK_HEIGHT_ENDPOINT
    return endpoint.format(ChainConstants.BLOCK_HEIGHT)

def get_txn_data_endpoint(block_hash, start_tx_id):
    endpoint = ChainConstants.BASE_DNS + ChainConstants.FETCH_TXNS_DATA
    return endpoint.format(block_hash, start_tx_id)

def get_largest_length(x):
    return sorted(test_dict, key = lambda key: len(test_dict[key]))[0:10]

get_max_ancestors()