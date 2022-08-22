from solana.keypair import Keypair
from solana.publickey import PublicKey
from solana.rpc.api import Client
from solana.transaction import Transaction
from solana.system_program import TransferParams, transfer
import json
import hikari

solana_client = Client("https://api.devnet.solana.com")

def create_account(sender_username):
    try:
        kp = Keypair.generate()
        public_key = str(kp.public_key)
        secret_key = kp.secret_key

        data = {
            'public_key': public_key,
            'secret_key': secret_key.decode("latin-1"),
        }

        file_name = f'./tf_backend/discord_bot/wallets/{sender_username}.txt'
        with open(file_name, 'w') as outfile:
            json.dump(data, outfile)

        if public_key is not None:
            message = "Solana wallet created successfully!"
            emb_crt_suc = (
                hikari.Embed(
                    title="**Toasty Friends**",
                    color="#996515",
                )

                .set_footer(
                    text=f"Toast or DIE",
                )
                .add_field(
                    name="Status",
                    value=message,
                )
                .add_field(
                    name="Public Key: ",
                    value=format(public_key)
                )
            )
            return emb_crt_suc

    except Exception as e:
        print(e)
        message = "Failed to create account."
        emb_crt_fail = (
            hikari.Embed(
                title="**Toasty Friends**",
                color="#996515",
            )

            .set_footer(
                text=f"Toast or DIE",
            )
            .add_field(
                name="Status",
                value=message,
            )
        )
        return emb_crt_fail 


#add response and ephemeril message
def load_wallet(sender_username):
    try:
        file_name = f'./tf_backend/discord_bot/wallets/{sender_username}.txt'
        with open(file_name) as json_file:
            account = json.load(json_file)
            account['secret_key'] = account['secret_key'].encode("latin-1")
            return account

    except Exception as e:
        print(e)
        return None  


def fund_account(sender_username, amount):
    if amount > 2:
            message = f"Requesting {amount-2} SOL over."
            emb_over_sol = (
                hikari.Embed(
                    title="**Toasty Friends**",
                    color="#996515",
                )

                .set_footer(
                    text=f"Toast or DIE",
                )
                .add_field(
                    name="Status",
                    value=message,
                )
            )
            return emb_over_sol
    else:
        try:
            amount = int(1000000000 * amount)
            account = load_wallet(sender_username)

            resp = solana_client.request_airdrop(
                account['public_key'], amount)   
            print(resp)    

            transaction_id = resp['result']
            if transaction_id != None:
                message = f'You have successfully requested {amount / 1000000000} SOL'
                emb_rqst_suc = (
                    hikari.Embed(
                        title="**Toasty Friends**",
                        color="#996515",
                    )

                    .set_footer(
                        text=f"Toast or DIE",
                    )
                    .add_field(
                        name="Status",
                        value=message,
                    )
                    .add_field(
                        name="Transaction ID: ",
                        value=format(transaction_id),
                    )
                )

                return emb_rqst_suc
            else:
                return None

        except Exception as e:
            print('error:', e)
            message = "Failed to fund your Solana account"
            emb_rqst_fail = (
                hikari.Embed(
                    title="**Toasty Friends**",
                    color="#996515",
                )

                .set_footer(
                    text=f"Toast or DIE",
                )
                .add_field(
                    name="Status",
                    value=message,
                )
            )
            return emb_rqst_fail

def get_balance(sender_username):
    try:
        account = load_wallet(sender_username)
        resp = solana_client.get_balance(account['public_key'])
        print(resp)
        balance = resp['result']['value']/1000000000

        data = {
            "publicKey": account['public_key'],
            "balance": str(balance),
        }

        public_key = data['publicKey']
        balance = data['balance']
        
        emb_bal_suc = (
            hikari.Embed(
                title="**Toasty Friends**",
                color="#996515",
            )

            .set_footer(
                text=f"Toast or DIE",
            )
            .add_field(
                name="Account: ",
                value=format(public_key),
            )
            .add_field(
                name="Balance: ",
                value=format(balance),
            )
        )
        return emb_bal_suc

    except Exception as e:
        print('Error:', e)
        message = "Failed to retrieve balance"
        emb_bal_not = (
            hikari.Embed(
                title="**Toasty Friends**",
                color="#996515",
            )

            .set_footer(
                text=f"Toast or DIE",
            )
            .add_field(
                name="Status",
                value=message
            )
        )
        return emb_bal_not

def send_sol(sender_username, amount, receiver):
    message = "Transaction Failed"
    emb_trx_fail = (
        hikari.Embed(
            title="**Toasty Friends**",
            color="#996515",
        )
        .set_footer(
            text=f"Toast or DIE",
        )
        .add_field(
            name="Status",
            value=message
        )
    )
    try:
        account = load_wallet(sender_username)
        sender = Keypair.from_secret_key(account['secret_key'])
        amount = int(1000000000 * amount)

        txn = Transaction().add(
            transfer(
                TransferParams(
                    from_pubkey=sender.public_key,
                    to_pubkey=PublicKey(receiver),
                    lamports=amount
        )))
        resp = solana_client.send_transaction(txn, sender)
        print(resp)

        transaction_id = resp['result']
        if transaction_id != None:
            emb_trx_suc = (
                hikari.Embed(
                    title="**Toasty Friends**",
                    color="#996515",
                )
                .set_footer(
                    text=f"Toast or DIE",
                )
                .add_field(
                    name="Success",
                    value="Your transaction has completed!",
                )
                .add_field(
                    name="Amount: ",
                    value=f"{amount/1000000000} SOL" ,
                )
                .add_field(
                    name="Reciever: ",
                    value=receiver,
                )
                .add_field(
                    name="Transaction ID: ",
                    value=format(transaction_id),
                )
            )
            return emb_trx_suc
        else:
            return emb_trx_fail

    except Exception as e:
        print('Error:', e)
        return emb_trx_fail
