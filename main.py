import argparse
import json
import os
import base58
import datetime

import nacl.encoding
import nacl.signing


to_base58 = lambda data: base58.b58encode(data).decode('utf-8')
from_base58 = lambda data: base58.b58decode(data.encode('utf-8'))

def save_object_to_file(filename, obj):
    with open(filename, 'w') as f:
        f.write(json.dumps(obj, indent=4))

def load_object_from_file(filename):
    with open(filename, 'r') as f:
        return json.loads(f.read())

def generate_keypair(output_path, name):
    # Generate a new signing keypair
    signing_key = nacl.signing.SigningKey.generate()
    verify_key = signing_key.verify_key

    # Serialize the keypair to JSON
    serialized_keypair = {
        "name": name,
        "generated_date": datetime.datetime.now().isoformat(),
        "private_key": to_base58(signing_key.encode()),
        "public_key": to_base58(verify_key.encode()),
    }
    save_object_to_file(output_path, serialized_keypair)
    return serialized_keypair


# def prepare_public_cert(name):
#     serialized_keypair = load_object_from_file(f'{name}.private.json')
#     del serialized_keypair['private_key']
#     save_object_to_file(f'{name}.public.json', serialized_keypair)
#     return serialized_keypair


def sign_object(key_path, object_to_sign_path, output_path):
    payload = load_object_from_file(object_to_sign_path)
    # Deserialize the JSON private key
    serialized_keypair = load_object_from_file(key_path)

    # Extract the signing key from the keypair
    signing_key_bytes = from_base58(serialized_keypair["private_key"])
    signing_key = nacl.signing.SigningKey(signing_key_bytes)

    # Sign the payload and serialize the result to JSON
    payload_encoded = json.dumps(payload, sort_keys=True).encode()
    signed_payload = signing_key.sign(
        payload_encoded,
        encoder=nacl.encoding.Base64Encoder)
    serialized_signed_payload = {
        "payload": payload,
        "signature": to_base58(signed_payload.signature),
        "public_key": serialized_keypair["public_key"],
    }
    save_object_to_file(output_path, serialized_signed_payload)
    return serialized_signed_payload


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command")

    generate_parser = subparsers.add_parser("generate_keypair")
    generate_parser.add_argument("output_path", help="Path to save the keypair")
    generate_parser.add_argument("name", help="The name of the keypair")

    # prepare_parser = subparsers.add_parser("prepare_public_cert")
    # prepare_parser.add_argument("output", help="The JSON serialized with no private key")

    sign_parser = subparsers.add_parser("sign_object")
    sign_parser.add_argument("key_path", help="The path of private key")
    sign_parser.add_argument("object_to_sign_path", help="Path of object to sign")
    sign_parser.add_argument("output_path", help="Path to save the output")

    args = parser.parse_args()

    if args.command == "generate_keypair":
        serialized_keypair = generate_keypair(args.output_path, args.name)
        print(json.dumps(serialized_keypair, indent=4))
    # elif args.command == "prepare_public_cert":
    #     serialized_prepared_public_cert = prepare_public_cert(args.name)
    #     print(json.dumps(serialized_prepared_public_cert, indent=4))
    elif args.command == "sign_object":
        serialized_signed_payload_json = sign_object(args.key_path, args.object_to_sign_path, args.output_path)
        print(json.dumps(serialized_signed_payload_json, indent=4))

