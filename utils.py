import csv

# Infura Project ID
infura_project_id = '59ad23946a7b4d57977e0ebe476348db'  # Gantilah dengan Project ID Anda

def select_network(choice, send_token):
    if choice == '1':
        return 'https://bsc-dataseed.binance.org/', 56, send_token
    elif choice == '2':
        return f'https://mainnet.infura.io/v3/{infura_project_id}', 1, send_token
    elif choice == '3':
        return f'https://polygon-mainnet.infura.io/v3/{infura_project_id}', 137, send_token
    elif choice == '4':
        return f'https://base-mainnet.infura.io/v3/{infura_project_id}', 8453, send_token
    else:
        return f'https://mainnet.infura.io/v3/{infura_project_id}', 1, False

def read_recipients_from_file(file):
    recipients = []
    if file.filename.endswith('.txt'):
        recipients = file.read().decode('utf-8').splitlines()
    elif file.filename.endswith('.csv'):
        csv_reader = csv.reader(file.read().decode('utf-8').splitlines())
        for row in csv_reader:
            recipients.extend(row)
    # Membersihkan alamat dari karakter whitespace tambahan
    recipients = [address.strip() for address in recipients if address.strip()]
    return recipients
