#!/bin/bash

# mkdir if not exist
mkdir -p example

# create keypair for root entity (e.g. Night Mocha)
python main.py generate_keypair -n "Night Mocha" -o example/root.json -t organization

# create object without private key for root entity
echo '{"name": "Night Mocha", "twitter": "@nightmocha", "public_key":'`jq .public_key example/root.json`'}' > example/root.pub.json

# create keypairs for Alice, Bob, and Carol
python main.py generate_keypair -n "Alice Allison" -o example/alice.json
python main.py generate_keypair -n "Bobby Bobbart" -o example/bobby.json
python main.py generate_keypair -n "Carol Charles" -o example/carol.json

# create object without private key for Alice, Bob, Carol
echo '{"name": "Alice Allison", "twitter": "@alice", "public_key":'`jq .public_key example/alice.json`'}' > example/alice.pub.json
echo '{"name": "Bobby Bobbart", "twitter": "@bobby", "public_key":'`jq .public_key example/bobby.json`'}' > example/bobby.pub.json
echo '{"name": "Carol Charles", "twitter": "@carol", "public_key":'`jq .public_key example/carol.json`'}' > example/carol.pub.json

# sign object with each private key
python main.py sign -i example/alice.pub.json -k example/alice.json -o example/alice.signed.json
python main.py sign -i example/bobby.pub.json -k example/bobby.json -o example/bobby.signed.json
python main.py sign -i example/carol.pub.json -k example/carol.json -o example/carol.signed.json

# sign object with root private key
python main.py sign -i example/alice.signed.json -k example/root.json -o example/alice.signed.json
python main.py sign -i example/bobby.signed.json -k example/root.json -o example/bobby.signed.json
python main.py sign -i example/carol.signed.json -k example/root.json -o example/carol.signed.json

# verify signatures
python main.py verify -i example/alice.signed.json
python main.py verify -i example/bobby.signed.json
python main.py verify -i example/carol.signed.json

# generate html files
python to_dist.py -r example/root.pub.json -c example/*.signed.json
cp verifier.html dist/verifier.html
cp -r js dist/