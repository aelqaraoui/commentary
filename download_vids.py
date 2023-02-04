import os
from tqdm import tqdm
from pytube import YouTube 

SAVE_PATH = "matches"
  
matches = [line.split(",") for line in open("match_links.csv", "r").read().split("\n")]

os.mkdir(SAVE_PATH)

for line in tqdm(matches):

    link = line[1]
  
    yt = YouTube(link) 
  
    yt.streams.get_lowest_resolution().download(SAVE_PATH)