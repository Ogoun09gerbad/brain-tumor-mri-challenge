from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

# 1. Générer la clé privée
private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)

# 2. Sauvegarder la clé privée (A GARDER SECRET)
with open("scripts/private_key.pem", "wb") as f:
    f.write(private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    ))

# 3. Générer et sauvegarder la clé publique (A METTRE SUR GITHUB)
public_key = private_key.public_key()
with open("encryption/public_key.pem", "wb") as f:
    f.write(public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    ))

print("✅ Clés générées avec succès dans 'scripts/' et 'encryption/'")