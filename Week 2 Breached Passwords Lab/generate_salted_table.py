"""
Ethan Paek
TA: Rachael Brooks
Lab #1
COEN 150L - T/Th 2:15 PM - 5:00 PM
6 October 2020
"""

import hashlib
import time

from generate_unsalted_table import hash_table, passwords


# Step 3: limit the number of salts in our dictionary to 100 and re-hash the passwords with salt
hash_salt_table = hash_table

# extract the salts so we can add them to our passwords
f1 = open("breached_data_salted.txt", "r")
salts = []
breached_data_pwds = []
for user_data in f1:
    # we only need 100 salts
    if len(salts) == 100:
        break
    # split the username, salt, and hash
    user_line = user_data.split("\t\t")
    # append the hash to our comprehensive list
    salts.append(user_line[1])
    breached_data_pwds.append(user_line[2].strip('\n'))
f1.close()

# add the salts to our passwords
pre_hashes = []
for i in range(len(hash_salt_table)):
    for salt in salts:
        tmp_str = salt + hash_salt_table[i]
        pre_hashes.append(tmp_str)

# now re-hash our passwords: hash(salt+hash(password))
post_hashes = []
for salted_hash in pre_hashes:
    hash_object = hashlib.sha256(salted_hash.encode('utf-8'))
    py_hash = hash_object.hexdigest()
    post_hashes.append(py_hash)

# Step 4: record the amount of time it takes to find our passwords
matched_pwds = []
start_time = time.time()
for i in range(len(post_hashes)):
    for j in range(len(breached_data_pwds)):
        if post_hashes[i] == breached_data_pwds[j]:
            matched_pwds.append(passwords[int(i/100)])
recorded_time = time.time() - start_time
print("\nTime to compare the generated hashes to those in breached_data_salted.txt:", (recorded_time * 1000), "ms")
print("Number of salted passwords cracked:", len(matched_pwds))


# now write the matched passwords to a txt file
f2 = open("cracked_passwords_salted.txt", "a")
for pwd in matched_pwds:
    f2.write(pwd)
    f2.write("\n")
f2.close()
