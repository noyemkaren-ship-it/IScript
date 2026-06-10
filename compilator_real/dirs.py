import os

def create_dirs():
    os.makedirs("build", exist_ok=True)
    os.makedirs("script", exist_ok=True)