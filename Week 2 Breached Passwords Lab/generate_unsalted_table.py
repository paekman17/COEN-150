"""
Ethan Paek
TA: Rachael Brooks
Lab #1
COEN 150L - T/Th 2:15 PM - 5:00 PM
6 October 2020
"""

import hashlib
import time

# Step 1: open the passwords file and append each individual one to a list
passwords = []
f1 = open("passes_real.txt", "r")
for password in f1:
    passwords.append(password.strip('\n'))
f1.close()

# hash each individual password
hash_table = []
for password in passwords:
    hash_object = hashlib.sha256(password.encode('utf-8'))
    py_hash = hash_object.hexdigest()
    hash_table.append(py_hash)


# Step 2: compare the generated hashes to those in breached_data.txt

# get the hashes from breached data
f2 = open("breached_data.txt", "r")
salted_passwords = []
for user_data in f2:
    # split the username and hash
    user_line = user_data.split("\t\t")
    # append the hash to our comprehensive list
    salted_passwords.append(user_line[1].strip('\n'))
f2.close()

matched_pwds = []
# record the amount of time it takes to find our passwords
start_time = time.time()
# matched_hashes = list((set(salted_passwords) & set(hash_table)))
for i in range(len(salted_passwords)):
    for j in range(len(hash_table)):
        if salted_passwords[i] == hash_table[j]:
            matched_pwds.append(passwords[j])
recorded_time = time.time() - start_time
print("Time to compare the generated hashes to those in breached_data.txt:", (recorded_time*1000), "ms")
print("Number of unsalted passwords cracked:", len(matched_pwds))

# now write the matched passwords to a txt file
f3 = open("cracked_passwords.txt", "a")
for pwd in matched_pwds:
    f3.write(pwd)
    f3.write("\n")
f3.close()
