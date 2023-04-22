import rsa

pub_key, priv_key = rsa.newkeys(1024)
p = pub_key.save_pkcs1("PEM").decode('utf-8')
print(p)

p = rsa.PublicKey.load_pkcs1(p.encode('utf-8'))

print(rsa.encrypt("TEST".encode('utf-8'), p))
