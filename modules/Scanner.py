from threading import Thread
import cv2
import t
import numpy as np
from pathlib import Path


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


class Scanner:
    def __init__(self, video_path):
        self.captions = []
        self.time_sequences = {}
        self.prev_sample = None
        self.time_start = 0
        self.last_time = 0
        self.caption_index = 0
        self.caption_output_index = 0
        self.caption_container = None
        self.video_folder = Path(video_path).parent
        self.caption_folder = self.video_folder / 'captions'
        if not self.caption_folder.is_dir():
            self.caption_folder.mkdir()
        self.stream = VideoStream(video_path)

    @staticmethod 
    def get_timestamp():
        return int(time.time())

    @staticmethod
    def calc_vector_distance(v1, v2):
        return np.sqrt(np.sum(np.square(v1^v2)))

    @staticmethod
    def concat_2d_matrix(im1, im2):
        return np.concatenate([im1, im2],axis=0)

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
        print(ratio)
        if(ratio<0.05 or ratio>0.8):
            return None
        caption = frame[caption_lower:caption_upper,:]
        return time, caption, white_map

    def filter_captions(self, caption_lower, caption_upper, white_threshold, consistency_threshold):
        tmp =  extract_caption(caption_lower, caption_upper)
        if tmp:
            time, caption, sample = tmp
            try:
                if((time-last_time)>200):
                    raise Exception('break point: natural ')
                else:
                    d = self.calc_vector_distance(prev_sample, sample)
                    if(d > consistency_threshold):
                        raise Exception('break point: surpass consistency threshold')
            except Exception as e:
                prev_sample = sample
                self.caption_receiver(caption_index, caption)
                time_sequences[str(caption_index-1)] = [time_start, last_time]
                time_start = time
                caption_index += 1
            last_time = time

    def caption_receiver(index, caption):
        caption = cv2.cvtColor(caption, cv2.COLOR_BGR2GRAY)
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(caption, str(index), (400,50), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 255, 0), 3) 
        if(self.caption_output_index < 1):
            self.caption_container = np.zeros(caption.shape)
        self.caption_container = concat_2d_matrix(self.caption_container,caption)
        if(self.caption_output_index%10==0):
            if(self.caption_output_index>0):
                cv2.imwrite(f'{video_folder}/captions/{self.get_timestamp()}.jpg', self.caption_container)
            self.caption_container = np.zeros(caption.shape)
        self.caption_output_index +=1

    def write_left_captions(self):
        cv2.imwrite(f'{self.video_folder}/captions/{self.get_timestamp()}.jpg', self.caption_container)


    def run(caption_lower, caption_upper, white_threshold=230, consistency_threshold=20):
        while(True):
            try:
                filter_captions(caption_lower, caption_upper, white_threshold, consistency_threshold)
            except:
                write_left_captions()
                break
        t.save_pickle(video_folder+'\\time.pkl',time_sequences)

if __name__ == '__main__':
    scanner = Scanner(r'C:\Users\heinz97\Desktop\1.mp4')
    rst = scanner.extract_caption(610, 653)
    print(rst)
    # video_path = r'G:\字幕专家\2中译英\wp146210元買了2條牛舌，今天做個新奇美食“椒麻牛舌”，又麻又辣，3碗飯都不夠吃！【半吨先生】.mp4'
    # scan(video_path,625,681)
    
  



