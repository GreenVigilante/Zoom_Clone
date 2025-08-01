from vidstream import *
import tkinter as tk
import threading
import requests
import socket
from tkinter import filedialog, messagebox
local_ip = socket.gethostbyname(socket.gethostname())
public = requests.get("https://api.ipify.org").text

connect_text = "Connect"
screen_text = "Start Screen Streaming"
camera_text = "Start Camera Stream"
audio_text = "Start Audio Streaming"
video_text = "Start Video Streaming"
ca = 1
sc = 1
au = 1
vi = 1
temp_sc = None
temp_ca = None
temp_au = None
temp_vi = None
audio = None

server = StreamingServer(local_ip, 9999)
reciever = AudioReceiver(local_ip, 8888)

def connect():
    t1= threading.Thread(target=server.start_server)
    t2= threading.Thread(target=reciever.start_server)
    t1.start()
    t2.start()
    btn_Connect.config(text="Reconnect")
    
  
def start_camera():
    global ca
    global temp_ca
    print(text_IP.get(1.0, "end-1c"))
    if ca %2 == 1:
        if ca > 1:
            CameraClient._get_frame = temp_ca
        camera= CameraClient(text_IP.get(1.0, "end-1c"), 7777)
        
        t3 = threading.Thread(target=camera.start_stream)
        t3.start()
        btn_Camera.config(text="Stop Camera Streaming")
        ca +=1
    else:
        temp_ca = CameraClient._get_frame
        CameraClient._get_frame = None
        btn_Camera.config(text="Start Camera Streaming")
        ca +=1

def start_screen():
    global sc
    global temp_sc
    if sc %2 ==1:
        if sc > 1:
            ScreenShareClient._get_frame = temp_sc
        screen = ScreenShareClient(text_IP.get(1.0, "end-1c"), 7777)
        t4 = threading.Thread(target=screen.start_stream)
        t4.start()
        btn_Screen.config(text="Stop Screen Streaming")
        sc +=1
    else:
        temp_sc = ScreenShareClient._get_frame
        ScreenShareClient._get_frame= None
        btn_Screen.config(text="Start Screen Streaming")
        sc +=1
def start_audio():
    global audio
    global au
    if au%2 ==1:
        audio = AudioSender(text_IP.get(1.0, "end-1c"), 6666)
        t5 = threading.Thread(target=audio.start_stream)
        t5.start()
        btn_Audio.config(text="Stop Audio Streaming")
        au +=1
    else:
        if audio is not None:
            audio.stop_stream()
            audio = None
            t5 = None
        btn_Audio.config(text="Start Audio Streaming")
        au +=1
def start_video():
    global vi, temp_vi
    if vi%2 ==1:
        if vi > 1:
            VideoClient._get_frame = temp_vi
        filename = filedialog.askopenfilename(defaultextension="mp4", filetypes=[("MP4", ".mp4")])
        video = VideoClient(text_IP.get(1.0, "end-1c"), 7777, filename)
        t6 = threading.Thread(target=video.start_stream)
        t6.start()
        btn_Video.config(text="Stop Video Streaming")
        vi +=1
    else:
        temp_vi = VideoClient._get_frame
        VideoClient._get_frame= None
        btn_Video.config(text="Start Video Streaming")
        vi +=1
window = tk.Tk()
window.title("Drop some zoom")
window.geometry("400x400")

label_IP = tk.Label(window, text="Enter IP :", font=("Arial", 12))
label_IP.pack()
text_IP = tk.Text(window, height=1)
text_IP.pack()
    
btn_Connect = tk.Button(window, text=connect_text, width=60, command= connect)
btn_Connect.pack(anchor=tk.CENTER, expand=True)
btn_Screen = tk.Button(window, text=screen_text, width=60, command= start_screen)
btn_Screen.pack(anchor=tk.CENTER, expand=True)
btn_Camera = tk.Button(window, text=camera_text, width=60, command= start_camera)
btn_Camera.pack(anchor=tk.CENTER, expand=True)
btn_Audio = tk.Button(window, text=audio_text, width=60, command=start_audio )
btn_Audio.pack(anchor=tk.CENTER, expand=True)
btn_Video = tk.Button(window, text=video_text, width=60, command=start_video )
btn_Video.pack(anchor=tk.CENTER, expand=True)

window.mainloop()