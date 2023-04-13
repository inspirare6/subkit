import cv2
import numpy as np
from threading import Thread
from pathlib import Path
import time


class VideoStream:
    def __init__(self, src):
        self.capture = cv2.VideoCapture(src)
        self.time_ms = 0

    def get_frame(self):
        self.capture.set(cv2.CAP_PROP_POS_MSEC, self.time_ms)
        (self.status, self.frame) = self.capture.read()
        rst =  (self.time_ms, self.frame)
        self.time_ms += 200
        return rst


class CaptionContainer:
    def __init__(self, folder):
        self.caption_index = 0
        self.instance = None
        self.folder = folder

    @staticmethod 
    def get_timestamp():
        return int(time.time())

    def init(self, caption):
        self.instance = np.zeros(caption.shape)

    def write(self, caption):
        caption = cv2.cvtColor(caption, cv2.COLOR_BGR2GRAY)
        if self.caption_index == 0:
            self.init(caption)
        self.instance = np.concatenate([self.instance, caption], axis=0)
        self.caption_index += 1
        if self.caption_index%5 == 0:
            self.export()
            self.init(caption)

    def export(self):
        cv2.imwrite(f'{self.folder}/{self.get_timestamp()}.jpg', self.instance)


class Scanner:
    def __init__(self, video_path):
        self.captions = []
        self.prev_sample = None
        self.time_start = 0
        self.last_time = 0
        self.caption_index = 0
        self.video_folder = Path(video_path).parent
        self.caption_folder = self.video_folder / 'captions'
        self.caption_container = CaptionContainer(self.caption_folder)
        if not self.caption_folder.is_dir():
            self.caption_folder.mkdir()
        self.stream = VideoStream(video_path)

    @staticmethod
    def calc_vector_distance(v1, v2):
        return np.sqrt(np.sum(np.square(v1^v2)))

    def extract_caption(self, caption_lower, caption_upper, white_threshold = 230):
        time, frame = self.stream.get_frame()
        screen_width = frame.shape[1]
        sample_left = int(screen_width/2-(caption_upper-caption_lower))
        sample_right = int(screen_width/2+(caption_upper-caption_lower)) 
        sample_region = frame[caption_lower:caption_upper,sample_left:sample_right]
        sample_region = cv2.cvtColor(sample_region, cv2.COLOR_BGR2GRAY)
        white_map = sample_region > white_threshold  
        white_total = white_map.sum()
        height, width = white_map.shape
        area = width * height
        ratio = white_total / area 
        # print(ratio)
        if(ratio<0.05 or ratio>0.8):
            return None
        caption = frame[caption_lower:caption_upper,:]
        self.caption_container.write(caption)
        return time, caption, white_map

    def run(self, caption_lower, caption_upper, white_threshold=230, consistency_threshold=3):
        while(True):
            tmp =  self.extract_caption(caption_lower, caption_upper)
            if tmp:
                time, caption, sample = tmp
                try:
                    d = self.calc_vector_distance(self.prev_sample, sample)
                    print(d)
                    if(d > consistency_threshold):
                        raise Exception('break point: surpass consistency threshold')
                except Exception as e:
                    self.prev_sample = sample
                    self.caption_container.write(caption)
                self.last_time = time


if __name__ == '__main__':
    scanner = Scanner(r'C:\Users\heinz97\Desktop\1.mp4')
    # rst = scanner.extract_caption(610, 653)
    # print(rst)
    scanner.run(610, 653)
    # video_path = r'G:\字幕专家\2中译英\wp146210元買了2條牛舌，今天做個新奇美食“椒麻牛舌”，又麻又辣，3碗飯都不夠吃！【半吨先生】.mp4'
    # scan(video_path,625,681)
    
  



