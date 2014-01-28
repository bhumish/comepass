import sys, random, struct, commands, os
from hashlib import md5
from time import strftime

def encrypt_file(key, in_filename, out_filename=None, chunksize=64*1024):
 if not out_filename:
  out_filename = in_filename + '.enc'
 iv = ''.join(chr(random.randint(0, 0xFF)) for i in range(16))
 encryptor = AES.new(key, AES.MODE_CBC, iv)
 filesize = os.path.getsize(in_filename)
 with open(in_filename, 'rb') as infile:
  with open(out_filename, 'wb') as outfile:
   outfile.write(struct.pack('<Q', filesize))
   outfile.write(iv)
   while True:
    chunk = infile.read(chunksize)
    if len(chunk) == 0:
     break
    elif len(chunk) % 16 != 0:
     chunk += ' ' * (16 - len(chunk) % 16)
    outfile.write(encryptor.encrypt(chunk))

def decrypt_file(key, in_filename, out_filename=None, chunksize=24*1024):
 if not out_filename:
  out_filename = os.path.splitext(in_filename)[0]
 with open(in_filename, 'rb') as infile:
  origsize = struct.unpack('<Q', infile.read(struct.calcsize('Q')))[0]
  iv = infile.read(16)
  decryptor = AES.new(key, AES.MODE_CBC, iv)
  with open(out_filename, 'wb') as outfile:
   while True:
    chunk = infile.read(chunksize)
    if len(chunk) == 0:
     break
    outfile.write(decryptor.decrypt(chunk))
   outfile.truncate(origsize)

def gen(key):
 """The gen() function generates a random password of the user provided length by choosing from a list of numbers and alphabets."""
 while 1:
  len = input('Password length? \n')
  lst = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','1','2','3','4','5','6','7','8','9','0','.','','@','!',' ','$','A','S','D','F','G','H','J','K','L','M','N','B','V','C','X','Z','Q','W','E','R','T','Y','U','I','O','P','!','@','.','1','2','0','9','8','7','3','4','6','5']
  pwd = ''
  for i in range(1,len+1):
   n = random.choice(lst)
   pwd = pwd+n
  print 'Your password is: ' +pwd
  c = raw_input("Is this password OK? Press 'Y' to save this password in the file, else 'N' to generate a new password: ")
  c = c.lower()
  if c == 'y':
   save(pwd,key)
  if not c == 'n':
   sys.exit()

def save(pwd,key):
 """The save(password) function takes a password as input from the gen() function and encrypts the password for securely storing it under the file named .list""" 
 decrypt_file(key,'.list.enc','list')
 f = open('list','a')
 web = raw_input("Save the password under which website? \n")
 web = web.lower()
 f.write(web+ ' : ' +pwd+ '\n')
 f.close()
 print "Success! Password stored in the file."
 encrypt_file(key,'list','.list.enc')
 cmd = 'rm -f list'
 print commands.getoutput(cmd)
 i = raw_input('Do you want to get back to main menu or exit(Q)? \n')
 if i.lower() == 'q':
  sys.exit()
 else:
  main()

def get(key):
 """The get function retrieves the password as asked by user, by searching and decrypting the password from the stored file."""
 web = raw_input('Enter the name of the website for getting its password: \n')
 web = web.lower()
 decrypt_file(key,'.list.enc','list')
 f = open('list','r')
 for i in f:
  if web in i:
   print i
 f.close()
 encrypt_file(key,'list','.list.enc')
 cmd = 'rm -f list'
 print commands.getoutput(cmd)

def main():
 """This is the main() function which asks the user to select from generating a password or retrieving any passwords."""
 f=open('list','a')
 t = strftime("%Y-%m-%d %H:%M:%S")
 f.write(t)
 key = raw_input("Enter your passphrase: \n")
 encrypt_file(key,'list')
 i=input("What do you want to do? \nPress 1 to Generate password \nPress 2 to Retrieve Password \n")
 if i == 1:
  gen(key)
 if i == 2:
  get(key)

if __name__ == '__main__':
 main()
