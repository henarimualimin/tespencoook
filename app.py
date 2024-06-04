from flask import Flask, request, render_template, redirect, url_for, flash
from web3 import Web3
import os
from .utils import select_network, read_recipients_from_file

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Gantilah dengan secret key yang lebih aman

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send', methods=['POST'])
def send():
    network_choice = request.form['network']
    private_key = request.form.get('private_key')
    wallet_address = request.form.get('wallet_address')
    amount_input = request.form['amount']
    token_contract_address = request.form.get('token_contract')

    send_token = network_choice == '5'
    if send_token:
        token_network_choice = request.form['token_network']
        network_url, chain_id, _ = select_network(token_network_choice, send_token)
    else:
        network_url, chain_id, _ = select_network(network_choice, send_token)

    if not network_url:
        flash('Invalid network selected.', 'danger')
        return redirect(url_for('index'))

    file = request.files['recipients_file']
    recipients = read_recipients_from_file(file)

    w3 = Web3(Web3.HTTPProvider(network_url))

    if not w3.isConnected():
        flash('Failed to connect to the network.', 'danger')
        return redirect(url_for('index'))

    if private_key:
        account = w3.eth.account.from_key(private_key)
        sender_address = account.address
    else:
        sender_address = wallet_address

    if send_token and token_contract_address:
        token_abi = '[{"constant":false,"inputs":[{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transfer","outputs":[{"name":"","type":"bool"}],"type":"function"},{"constant":true,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint8"}],"type":"function"}]'
        token_contract = w3.eth.contract(address=token_contract_address, abi=token_abi)
        decimals = token_contract.functions.decimals().call()
        amount_wei = int(float(amount_input) * (10 ** decimals))
    else:
        amount_wei = w3.toWei(amount_input, 'ether')

    nonce = w3.eth.getTransactionCount(sender_address)
    gas_price = w3.eth.gasPrice

    # Validasi saldo sebelum mengirim transaksi
    balance = w3.eth.getBalance(sender_address)
    if send_token:
        total_gas_cost = gas_price * 70000 * len(recipients)
    else:
        total_gas_cost = gas_price * 21000 * len(recipients)

    if balance < total_gas_cost:
        flash('Insufficient funds for gas fees.', 'danger')
        return redirect(url_for('index'))

    tx_hashes = []

    for address in recipients:
        if send_token:
            transaction = token_contract.functions.transfer(
                address, amount_wei
            ).buildTransaction({
                'chainId': chain_id,
                'gas': 70000,
                'gasPrice': gas_price,
                'nonce': nonce,
            })
        else:
            transaction = {
                'to': address,
                'value': amount_wei,
                'gas': 21000,
                'gasPrice': gas_price,
                'nonce': nonce,
                'chainId': chain_id
            }

        if private_key:
            signed_tx = w3.eth.account.signTransaction(transaction, private_key)
            tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
        else:
            # Jika menggunakan wallet connect, masukkan logika penandatanganan transaksi di sini
            flash('Wallet connect transaction signing not implemented yet.', 'danger')
            return redirect(url_for('index'))

        tx_hashes.append(tx_hash.hex())
        nonce += 1

    flash(f'Transactions sent: {", ".join(tx_hashes)}', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)