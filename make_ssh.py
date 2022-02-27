import os

rsa_key = os.getenv("RSA_KEY")
print(rsa_key)
print("wget")
os.system(f"wget {rsa_key} -O /home/runner/Kur0bot/id_rsa")
print("chmod")
os.system("chmod 400 /home/runner/Kur0bot/id_rsa")
try:
    os.mkdir("/home/runner/.ssh/")
except:
    pass
print("moving")
os.system("mv /home/runner/Kur0bot/id_rsa /home/runner/.ssh/id_rsa -f")
