import argparse
import json
import os

from jinja2 import Environment, FileSystemLoader

DIST_DIR = 'dist'
TEMPLATE_DIR = 'templates'
# make sure the dist directory exists


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='to_html.py',
        description='Accept a root public key and a list of ' +
        'signed objects and generate several HTML files based on templates.')
    parser.add_argument("-r", "--root-public-key", type=str,
                        help="The root public key", required=True)
    parser.add_argument("-c", "--certs", type=str, nargs='+',
                        help="The list of signed objects", required=True)
    
    args = parser.parse_args()

    root = json.loads(open(args.root_public_key, 'r').read())
    certs = [json.loads(open(c, 'r').read()) for c in args.certs]
    
    if not os.path.exists(DIST_DIR):
        os.makedirs(DIST_DIR)

    # generate single cert pages for root, and certs
    # generate a list page including link to root, and link to list of certs
    env = Environment( loader = FileSystemLoader(TEMPLATE_DIR))

    # generate root pages
    root_template = env.get_template('single.html')
    root_html = root_template.render(payload=root, signatures=[])
    with open(os.path.join(DIST_DIR, 'root.html'), 'w') as f:
        f.write(root_html)
    with open(os.path.join(DIST_DIR, root['public_key'] + '.html'), 'w') as f:
        f.write(root_html)
    with open(os.path.join(DIST_DIR, 'root.json'), 'w') as f:
        f.write(json.dumps(root, indent=4))
    with open(os.path.join(DIST_DIR, root['public_key'] + '.json'), 'w') as f:
        f.write(json.dumps(root, indent=4))

    # generate cert pages
    cert_template = env.get_template('single.html')
    for cert in certs:
        payload = json.loads(cert['payload'])
        cert_html = cert_template.render(payload=payload, signatures=cert['signatures'])
        with open(os.path.join(DIST_DIR, payload['public_key'] + '.html'), 'w') as f:
            f.write(cert_html)
        with open(os.path.join(DIST_DIR, payload['public_key'] + '.json'), 'w') as f:
            f.write(json.dumps(cert, indent=4))

    # generate list page
    list_template = env.get_template('list.html')
    list_html = list_template.render(
        root=root,
        certs=[json.loads(c['payload']) for c in certs])
    with open(os.path.join(DIST_DIR, 'index.html'), 'w') as f:
        f.write(list_html)