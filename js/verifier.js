const to_b58 = function(B,A='123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'){var d=[],s="",i,j,c,n;for(i in B){j=0,c=B[i];s+=c||s.length^i?"":1;while(j in d||c){n=d[j];n=n?n*256+c:c;c=n/58|0;d[j]=n%58;j++}}while(j--)s+=A[d[j]];return s};
const from_b58 = function(S,A='123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'){var d=[],b=[],i,j,c,n;for(i in S){j=0,c=A.indexOf(S[i]);if(c<0)return undefined;c||b.length^i?i:b.push(0);while(j in d||c){n=d[j];n=n?n*58+c:c;c=n>>8;d[j]=n%256;j++}}while(j--)b.push(d[j]);return new Uint8Array(b)};
const toHexString= function(a) {
  return Array.from(a, function(byte) {
    return ('0' + (byte & 0xFF).toString(16)).slice(-2);
  }).join('')
}

async function verifyAndTraverse(link, visited = []) {
  try {
    const response = await fetch(link);
    const json = await response.json();

    const { signatures, payload } = json;
    // Verify the signature using the signer's public key
    for(let i = 0; i < signatures.length; i++) {
      const { signature, signer_public_key, signer_name, signer_type } = signatures[i];
      const encoder = new TextEncoder();
      const signatureBytes = from_b58(signature);
      const publicKeyBytes = from_b58(signer_public_key);
      const payloadEncoded = encoder.encode(payload)
      const verified = nacl.sign.detached.verify(payloadEncoded, signatureBytes, publicKeyBytes);
      visited.push({
        link,
        signer_name,
        signer_public_key,
        signer_type,
        verified,
      });
    }

    // if (parent) { // Traverse upstream to the parent object
    //   await verifyAndTraverse(parent, visited);
    // }
    return {payload, visited};
  } catch (error) {
    console.error(error);
    return {payload, visited};
  }
}
