def web_sushiswap(privatekey, gasLimit, to_token_address, to_symbol):
    """
    SushiSwap swap function
    """
    amountOutMin = 0
    path = [NATIVE_TOKEN_ADDRESS, to_token_address]
    deadline = int(time.time()) + 15 * 60
    value = 0
    gasPrice = 5000000000
    amountIn = 1000000000000000000
    to = '0x6B3595068778DD592e39A122f4f5a5cF09C90fe2'
    nonce = web3.eth.getTransactionCount(SUSHISWAP_ROUTER_ADDRESS)

    # Create the sushi swap contract
    sushi_swap_contract = web3.eth.contract(
        address=SUSHISWAP_ROUTER_ADDRESS,
        abi=SUSHISWAP_ROUTER_ABI,
    )

    # Create the transaction
    txn = sushi_swap_contract.functions.swapExactETHForTokens(
        amountOutMin,
        path,
        to,
        deadline,
    ).buildTransaction({
        'chainId': 1,
        'gas': gasLimit,
        'gasPrice': gasPrice,
        'nonce': nonce,
        'value': value,
    })

    # Sign the transaction
    signed_txn = web3.eth.account.sign_transaction(txn, private_key=privatekey)

    # Send the transaction
    tx_hash = web3.eth.sendRawTransaction(signed_txn.rawTransaction)

    # Wait for the transaction to be mined
    receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

    print(f"Transaction receipt: {receipt}")
    print(f"Swapped {amountIn} NATIVE_TOKEN for {receipt['logs'][0]['data']}")

    return receipt

