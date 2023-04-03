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

def generate_keypair(output, name):
    # Generate a new signing keypair
    signing_key = nacl.signing.SigningKey.generate()
    verify_key = signing_key.verify_key

    # Serialize the keypair to JSON
    serialized_keypair = {
        "generated_date": datetime.datetime.now().isoformat(),
        "private_key": to_base58(signing_key.encode()),
        "public_key": to_base58(verify_key.encode()),
    }
    if name:
        serialized_keypair['name'] = name
    save_object_to_file(output, serialized_keypair)
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
    signed_payload = signing_key.sign(payload_encoded)
    serialized_signed_payload = {
        "payload": payload,
        "signature": to_base58(signed_payload.signature),
        "public_key": serialized_keypair["public_key"],
    }
    save_object_to_file(output_path, serialized_signed_payload)
    return serialized_signed_payload


def verify_object(path):
    serialized_signed_payload_json = load_object_from_file(path)
    # Extract the public key from the signed payload
    public_key_bytes = from_base58(serialized_signed_payload_json["public_key"])
    verify_key = nacl.signing.VerifyKey(public_key_bytes)

    # Serialize the payload and verify the signature
    payload_encoded = json.dumps(serialized_signed_payload_json["payload"], sort_keys=True).encode()
    signature_bytes = from_base58(serialized_signed_payload_json["signature"])
    try:
        verify_key.verify(payload_encoded, signature_bytes)
        return True
    except nacl.exceptions.BadSignatureError:
        return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='main.py',
        description='Script for generating ed25519 keypair, ' +
        'signing objects, and verifying signed objects. ' +
        'All bytes are encoded as base58.')
    sp = parser.add_subparsers(dest="command")

    generate_parser = sp.add_parser("generate_keypair",
                                    help="Generate a keypair (ed25519).")
    generate_parser.add_argument("-n", "--name", type=str,
                                 help="The name of the keypair")
    generate_parser.add_argument("-o", "--output", type=str,
                                 help="Path to save the keypair",
                                 required=True)

    sign_parser = sp.add_parser("sign",
                                help="Sign an object with a private key.")
    sign_parser.add_argument("-k", "--key-path", type=str,
                             help="The path of private key",
                             required=True)
    sign_parser.add_argument("-ts", "--to-sign-path", type=str,
                             help="Path of object to sign",
                             required=True)
    sign_parser.add_argument("-o", "--output", type=str,
                             help="Path to save the output",
                             required=True)

    verify_parser = sp.add_parser("verify",
                                  help="Verify a signed object.")
    verify_parser.add_argument("-f", "--object-to-verify", type=str,
                               help="The path of signed object")

    args = parser.parse_args()

    if args.command == "generate_keypair":
        serialized_keypair = generate_keypair(args.output, args.name)
        print(json.dumps(serialized_keypair, indent=4))
    # elif args.command == "prepare_public_cert":
    #     serialized_prepared_public_cert = prepare_public_cert(args.name)
    #     print(json.dumps(serialized_prepared_public_cert, indent=4))
    elif args.command == "sign":
        serialized_signed_payload_json = sign_object(args.key_path, args.to_sign_path, args.output)
        print(json.dumps(serialized_signed_payload_json, indent=4))
    elif args.command == "verify":
        if verify_object(args.object_to_verify):
            print("Signature is valid.")
        else:
            print("Signature is invalid.")
