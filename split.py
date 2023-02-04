import whisper
import ffmpeg
import glob
import cv2
import os 

model = whisper.load_model("base")

for video_filename in glob.glob("matches/*.mp4"):
    
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

            result = model.transcribe(video_filename.split(".mp4")[0] + "/" + f"{counter//duration}.mp3")

            counter += duration
        except Exception as e:
            print(e)
            break