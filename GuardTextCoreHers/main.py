import requests
import utils
import random
import json
import time
import os
import capture_photo
import img_to_ascii
from encode_image import encode_image_to_fit
from decode_image import decode_image_from_text
from PIL import Image
from threshold_image import threshold_image

url = 'https://guardts.ir/api/pastes/'

def random_char():
    arr = [[48, 57], [97, 122]]
    z = arr[random.randint(0, len(arr) - 1)]
    return chr(random.randint(z[0], z[1]))
    
    
def generate_random_string(length):
    return "".join([random_char() for i in range(length)])

def write_on_stream(stream_addr):
    print("Now writing on %s"%stream_addr)
    msg = input()
    t = time.time()
    current_address = stream_addr
    while msg != "":
        next = generate_random_string(10)
        
        msg_dict = {
            "msg" : msg,
            "next" : next,
            "time": t
        }
        
        r = utils.create_paste(current_address, json.dumps(msg_dict))
        print(r)
        msg = input()
        t = time.time()
        current_address = next
    next = generate_random_string(10)

    msg_dict = {
        "msg" : "NULL",
        "next" : next,
        "time": t
    }
    
    utils.create_paste(stream_addr, json.dumps(msg_dict))
    msg = input()
    t = time.time()

def write_ascii_stream(stream_addr):
    print("Now writing on %s"%stream_addr)
    capture_photo.capture_photo(camera_index=0, output_path="image.jpg")
    msg = img_to_ascii.image_to_ascii("image.jpg", width=75)
    print(msg)
    t = time.time()
    current_address = stream_addr
    while msg != "":
        next = generate_random_string(10)
        
        msg_dict = {
            "msg" : msg,
            "next" : next,
            "time": t
        }
        
        r = utils.create_paste(current_address, json.dumps(msg_dict))
        print(r)
        capture_photo.capture_photo(camera_index=0, output_path="image.jpg")
        msg = img_to_ascii.image_to_ascii("image.jpg", width=50)
        t = time.time()
        current_address = next
    next = generate_random_string(10)
            
    msg_dict = {
        "msg" : "NULL",
        "next" : next,
        "time": t
    }
    
    utils.create_paste(stream_addr, json.dumps(msg_dict))
    msg = input()
    t = time.time()

def write_image_stream(stream_addr):
    print("Now writing on %s"%stream_addr)
    a = input("Press Enter to start!")
    capture_photo.capture_photo(camera_index=0, output_path="image.jpg")
    #bw_img = threshold_image("image.jpg", threshold=128, output_path="bw.png")
    msg = encode_image_to_fit("image.jpg", char_limit=1748)
    print(msg)
    t = time.time()
    current_address = stream_addr
    while msg != "":
        next = generate_random_string(10)
        
        msg_dict = {
            "msg" : msg,
            "next" : next,
            "time": t
        }
        
        r = utils.create_paste(current_address, json.dumps(msg_dict))
        print(r)
        capture_photo.capture_photo(camera_index=0, output_path="image.jpg")
        #bw_img = threshold_image("image.jpg", threshold=128, output_path="bw.png")
        msg = encode_image_to_fit("image.jpg", char_limit=1748)
        t = time.time()
        print(msg)
        current_address = next
    next = generate_random_string(10)
            
    msg_dict = {
        "msg" : "NULL",
        "next" : next,
        "time": t
    }
    
    utils.create_paste(stream_addr, json.dumps(msg_dict))
    msg = input()
    t = time.time()

addr = generate_random_string(10)
print(addr)
write_image_stream(addr)
