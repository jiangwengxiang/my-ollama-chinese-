import os
os.environ["OMP_NUM_THREADS"] = "8"
os.environ["OMP_WAIT_POLICY"] = "ACTIVE"

name=str(input("plaese key your name"))
print("hello world,",name)
input("key any to end...")
