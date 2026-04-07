import os
import requests
import tarfile

# Create the folder for the raw data
os.makedirs("data/raw/en/wav", exist_ok=True)

# URL for a very small set of English sentences
url = "https://www.openslr.org/resources/12/dev-clean.tar.gz"
target_path = "data/raw/en/temp_audio.tar.gz"

print("Downloading English audio samples... please wait.")
response = requests.get(url, stream=True)
with open(target_path, "wb") as f:
    for chunk in response.iter_content(chunk_size=1024):
        if chunk:
            f.write(chunk)

print("Extracting files...")
with tarfile.open(target_path, "r:gz") as tar:
    # We only take the first 5 files to keep it fast
    members = [m for m in tar.getmembers() if m.name.endswith(".flac")][:5]
    tar.extractall(path="data/raw/en/", members=members)

print("Done! Check your data/raw/en/ folder.")
