import os
import shutil
from tqdm import tqdm



CLOSE_EYE_DIR = os.path.join("MRL Eye Data", "Prepared_Data", "Close Eyes")
OPEN_EYE_DIR = os.path.join("MRL Eye Data", "Prepared_Data", "Open Eyes")

os.makedirs(CLOSE_EYE_DIR, exist_ok=True)
print("Directory '%s' created successfully" % CLOSE_EYE_DIR)

os.makedirs(OPEN_EYE_DIR, exist_ok=True)
print("Directory '%s' created successfully" % OPEN_EYE_DIR)

Raw_DIR = os.path.join("MRL Eye Data", "mrlEyes_2018_01")
for dirpath, dirname, filenames in os.walk(Raw_DIR):
    for i in tqdm([f for f in filenames if f.endswith('.png')]):
        if i.split('_')[4] == '0':
            shutil.copy(src=dirpath + '/' + i, dst=CLOSE_EYE_DIR)
        elif i.split('_')[4] == '1':
            shutil.copy(src=dirpath + '/' + i, dst=OPEN_EYE_DIR)
