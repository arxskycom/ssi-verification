#!/bin/bash

# mkdir if not exist
mkdir -p example

# create keypair for root entity (e.g. Night Mocha)
python main.py generate_keypair -n "Night Mocha" -o example/root.priv.json -t organization

# create object without private key for root entity
echo '{"name": "Night Mocha", "twitter": "@nightmocha", "public_key":'`jq .public_key example/root.priv.json`'}' > example/root.pub.json

# create keypairs for Alice, Bob, and Carol
python main.py generate_keypair -n "Alice Allison" -o example/alice.priv.json
python main.py generate_keypair -n "Bobby Bobbart" -o example/bobby.priv.json
python main.py generate_keypair -n "Carol Charles" -o example/carol.priv.json

# create object without private key for Alice, Bob, Carol
echo '{"name": "Alice Allison", "twitter": "@alice", "public_key":'`jq .public_key example/alice.priv.json`'}' > example/alice.pub.json
echo '{"name": "Bobby Bobbart", "twitter": "@bobby", "public_key":'`jq .public_key example/bobby.priv.json`'}' > example/bobby.pub.json
echo '{"name": "Carol Charles", "twitter": "@carol", "public_key":'`jq .public_key example/carol.priv.json`'}' > example/carol.pub.json

# sign object with each private key
python main.py sign -i example/alice.pub.json -k example/alice.priv.json -o example/alice.signed.json
python main.py sign -i example/bobby.pub.json -k example/bobby.priv.json -o example/bobby.signed.json
python main.py sign -i example/carol.pub.json -k example/carol.priv.json -o example/carol.signed.json

# sign object with root private key
python main.py sign -i example/alice.signed.json -k example/root.priv.json -o example/alice.signed.json
python main.py sign -i example/bobby.signed.json -k example/root.priv.json -o example/bobby.signed.json
python main.py sign -i example/carol.signed.json -k example/root.priv.json -o example/carol.signed.json

# generate html files
python to_html.py -r example/root.pub.json -c example/*.signed.json