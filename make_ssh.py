import os
rsa_key = os.getenv('RSA_KEY')
print(rsa_key)
os.system(f'wget {rsa_key} -O /home/runner/Kur0bot/id_rsa')
os.system("chmod 400 /home/runner/Kur0bot/id_rsa")
os.system("mv /home/runner/Kur0bot/id_rsa /home/runner/.ssh/id_rsa -f")