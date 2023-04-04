# Verification Prototype

This repo is meant to demonstrate how digital trusted relationship can be established.
The driving principle is public key cryptography, specifically signatures.

## Example Flow

1. NY Times creates a key pair (public and private).
1. It publishes the public key on its website, e.g. nytimes.com/publickey.txt.
1. A journalist that works for the Times creates a key pair (public and private).
1. The journalist creates an object with their public key, and any other information they wish to share (e.g. twitter handle)
1. The journalist signs this object with their private key.
1. The journalist sends this object to the Times.
1. The Times signs this object with their private key.

The final signed object can be used to verify that the Times trusts the journalist.

## Using the Repo

### Environment Setup

1. Install python virtuelenv of choice (only first time):

```
pip install virtualenv
virtuelenv -p python3 venv
source venv/bin/activate && pip install -r requirements.txt
```

2. Initialize the virtual environment (everytime you visit this project):
```
source venv/bin/activate
```

### Running the Code

```
python main.py --help

# generate keypairs for NY Times and Alice
python main.py generate_keypair -n "NY Times" -o nytimes.priv.json
python main.py generate_keypair -n "Alice Roberts" -o alice.priv.json

# Create object with Alice's public key and twitter handle
# Note: if you don't have `jq` installed, you can just copy the public key from the file
echo '{"name": "Alice Allison", "twitter": "@alice", "public_key": '`jq .public_key alice.priv.json`'}' > alice.to.sign.json

# Sign the object with Alice's private key
python main.py sign -k alice.priv.json -i alice.to.sign.json -o alice.signed.json

# Sign the object with NY Times' private key
python main.py sign -k nytimes.priv.json -i alice.signed.json -o alice.signed.json

# Verify signature?
python main.py verify -i alice.signed.json
```