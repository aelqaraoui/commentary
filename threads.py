
import os
import threading
import time
import whisper
import ffmpeg
import glob
import cv2
import os 

model = whisper.load_model("base")

def task_sleep(sleep_duration, video_filename, lock):
    lock.acquire()
    # Perform operation that require a common data/resource
    lock.release()

    cap = cv2.VideoCapture(video_filename)

    if (cap.isOpened()== False): 
        print("Error opening video stream or file")
    else:
        os.mkdir(video_filename.split(".mp4")[0])
        print(cap.get(cv2.CAP_PROP_FPS))

    while(cap.isOpened()):
        # Capture frame-by-frame
        ret, frame = cap.read()
        if ret == True:
        
            cv2.imwrite(
                    video_filename.split(".mp4")[0] + "/" + str(len(glob.glob(video_filename.split(".mp4")[0] + "/*.jpg"))) + ".jpg" , 
                    frame
            )
        
        else: 
            break
        
    cap.release()
    

    input = ffmpeg.input(video_filename)

    counter = 0
    duration = 3
    while True:
        try:
            out = input.audio
            out = out.filter("atrim", start=counter, duration=duration)
            out = out.output(video_filename.split(".mp4")[0] + "/" + f"{counter//duration}.mp3")
            out.run()

            name = video_filename.split(".mp4")[0] + "/" + f"{counter//duration}.mp3"

            result = model.transcribe(name)

            f = open(name.replace(".mp4", ".txt"), "w")
            f.write(result["text"])

            counter += duration
        except Exception as e:
            print(e)
            break


if __name__ == "__main__":
    time_start = time.time()

    # Create lock (optional)
    thread_lock = threading.Lock()

    t = []
    for video_filename in glob.glob("matches/*.mp4"):
        t.append(threading.Thread(target=task_sleep, args=(2, video_filename, thread_lock)))

    for thread in t:
        thread.start()

    for thread in t:
        thread.join()

    time_end = time.time()
    print(f"Time elapsed: {round(time_end - time_start, 2)}s")