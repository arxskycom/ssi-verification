# Verification Prototype

This repo is meant to demonstrate how trusted relationship (verification) can be established without relying on platforms / third parties.
The driving principle is public key cryptography, specifically signatures.

## How it Works

Let’s say Alice is on Twitter and wants to prove to Bob that she is a NY Times reporter.

1. The NY Times will create a signing key pair, and publish their public key on their website.
1. Alice will also create a key pair.
1. Alice will create a document that includes her public key, name, twitter handle, position at the NYTimes and any other information (i.e. “claims”), Alice will self sign this document.
1. Alice will send this to the NY Times, where the NY Times will verify the validity of Alice’s relationship, if valid the NY Times will sign this document.
1. The NY Times will publish this signed document or send it back to Alice to publish
1. Alice will then link to the signed document from her Twitter bio.
1. Bob can now verify that Alice works at the NY Times by following the links and verifying the signatures and information in the signed document.

The final signed object can be used to verify a relationship between the Times and the journalist.

# Using this Repo

## Environment Setup

1. Install python virtuelenv of choice (only first time):

```
pip3 install virtualenv
virtualenv -p python3 venv
source venv/bin/activate && pip3 install -r requirements.txt
```

2. Initialize the virtual environment (everytime you visit this project):
```
source venv/bin/activate
```

*Note: `jq` is used for one of the steps below and in the `example.sh` script*

## Running the Code

```
python main.py --help

# generate keypairs for NY Times and Alice
python main.py generate_keypair -n "NY Times" -o nytimes.priv.json -t organization
python main.py generate_keypair -n "Alice Allison" -o alice.priv.json

# Create object with Alice's public key and twitter handle
# Note: if you don't have `jq` installed, you can just copy the public key from the file
echo '{
    "name": "Alice Allison",
    "twitter": "@aliceTheReporter",
    "position": "Reporter",
    "public_key": '`jq .public_key alice.priv.json`'
}' > alice.to.sign.json

# Sign the object with Alice's private key
python main.py sign -k alice.priv.json -i alice.to.sign.json -o alice.signed.json

# Sign the object with NY Times' private key
python main.py sign -k nytimes.priv.json -i alice.signed.json -o alice.signed.json

# Verify signature(s)
python main.py verify -i alice.signed.json
```

## End to End Example

The following will generate keypairs, create objects to be signed, sign them, and verify the signatures.
Then it will build some html pages to demonstrate how the signatures can be verified in a browser.


`dist/` - directory with published example html files to traverse

`example/` - directory with genereated keypairs, pre-signed public objects, and the final signed object

Once generated, can navigate to `dist/index.html` to see the example in action. (run a local server for proper JS function).

```
./example.sh  # will overwrite data in example/ and dist/
cd dist
python -m http.server
```
