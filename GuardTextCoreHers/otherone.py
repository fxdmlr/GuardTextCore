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
import pygame as pg
'''
Image dims : 322x181
'''

pg.init()
disp = pg.display.set_mode((500, 500))
url = 'https://guardts.ir/api/pastes/'

def random_char():
    arr = [[48, 57], [97, 122]]
    z = arr[random.randint(0, len(arr) - 1)]
    return chr(random.randint(z[0], z[1]))
    
    
def generate_random_string(length):
    return "".join([random_char() for i in range(length)])

def read_from_stream(stream_addr):
    '''
    Each message is a json : {"msg" : <the message>, 
    "next" : <where the next message will be written>,
    "time":<the exact time the message was written}
    '''
    read_request = requests.get(url + stream_addr)
    while read_request.status_code == 404:
        time.sleep(0.01)
        read_request = requests.get(url + stream_addr)
    
    msg_dict = json.loads(utils.read_paste(stream_addr))
    msg, next_addr, time_sent = msg_dict["msg"], msg_dict["next"], msg_dict["time"]
    index = 0
    while msg != "NULL":
        print(msg)
        print("\n\n\n")
        curr_sent_time = time_sent
        read_request = requests.get(url + next_addr)
        while read_request.status_code == 404:
            time.sleep(0.01)
            read_request = requests.get(url + next_addr)
        
        msg_dict = json.loads(utils.read_paste(next_addr))
        msg, next_addr, time_sent = msg_dict["msg"], msg_dict["next"], msg_dict["time"]
        time.sleep(float(time_sent) - float(curr_sent_time))
    
    return

def read_image_stream(stream_addr, screen=disp):
    '''
    Each message is a json : {"msg" : <the message>, 
    "next" : <where the next message will be written>,
    "time":<the exact time the message was written}
    '''
    read_request = requests.get(url + stream_addr)
    while read_request.status_code == 404:
        time.sleep(0.01)
        read_request = requests.get(url + stream_addr)
    
    msg_dict = json.loads(utils.read_paste(stream_addr))
    msg, next_addr, time_sent = msg_dict["msg"], msg_dict["next"], msg_dict["time"]
    index = 0
    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
        print(msg)
        decode_image_from_text(msg, "restored.webp")
        #img = Image.open("restored.webp")
        #img.show()
        screen.fill((0, 0, 0))
        image = pg.image.load("restored.webp")
        screen.blit(image, (0, 0))
        pg.display.update()
        print("\n\n\n")
        curr_sent_time = time_sent
        read_request = requests.get(url + next_addr)
        while read_request.status_code == 404:
            time.sleep(0.01)
            read_request = requests.get(url + next_addr)
        
        msg_dict = json.loads(utils.read_paste(next_addr))
        msg, next_addr, time_sent = msg_dict["msg"], msg_dict["next"], msg_dict["time"]
        time.sleep(float(time_sent) - float(curr_sent_time))
    pg.quit()
    return


read_image_stream(input("Enter read address : "))