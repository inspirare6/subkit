import cv2
import numpy as np
from threading import Thread
from pathlib import Path
import time

def get_timestamp():
    return int(time.time())


class VideoStream:
    def __init__(self, src):
        self.capture = cv2.VideoCapture(src)
        self.time_ms = 1

    def get_frame(self):
        self.capture.set(cv2.CAP_PROP_POS_MSEC, self.time_ms)
        (status, frame) = self.capture.read()
        if not status:
            print(self.time_ms)
            raise VideoEndException()
        rst =  (self.time_ms, frame)
        self.time_ms += 350
        return rst



class CaptionContainer:
    def __init__(self, folder):
        self.caption_index = 0
        self.instance = None
        self.folder = folder

    def init(self, caption):
        self.instance = np.zeros(caption.shape)

    def write(self, caption):
        if self.caption_index == 0:
            self.init(caption)
        self.instance = np.concatenate([self.instance, caption], axis=0)
        self.caption_index += 1
        if self.caption_index%20 == 0:
            self.export()
            self.init(caption)

    def export(self):
        path = self.folder / f'{get_timestamp()}.jpg'
        cv2.imencode('.jpg', self.instance)[1].tofile(str(path))


class VideoEndException(Exception):
    pass 


class Scanner:
    def __init__(self, video_path):
        self.prev_sample = None
        self.video_folder = Path(video_path).parent
        caption_folder = self.video_folder / f'{Path(video_path).stem}_captions'
        self.caption_container = CaptionContainer(caption_folder)
        if not caption_folder.is_dir():
            caption_folder.mkdir()
        self.stream = VideoStream(video_path)

    @staticmethod
    def calc_vector_distance(v1, v2):
        return np.sqrt(np.sum(np.square(v1^v2)))

    def extract_caption(self, matrix, white_threshold = 220):
        time, frame = self.stream.get_frame()
        screen_width = frame.shape[1]
        sample_left, caption_lower, sample_right, caption_upper = matrix
        sample_left = int(screen_width/2-(caption_upper-caption_lower)) if not sample_left else sample_left
        sample_right = int(screen_width/2+(caption_upper-caption_lower)) if not sample_right else sample_right
        caption = frame[caption_lower:caption_upper,:]
        caption = cv2.cvtColor(caption, cv2.COLOR_BGR2GRAY)
        caption_sample = caption[:,sample_left:sample_right]
        white_map = caption_sample > white_threshold  
        # white_map = caption_sample < 20
        white_total = white_map.sum()
        height, width = white_map.shape
        area = width * height
        ratio = white_total / area 
        if(ratio<0.05):
            return None
        return time, caption, white_map

    def run(self, caption_sample, white_threshold=230, consistency_threshold=10):
        while(True):
            try:
                tmp =  self.extract_caption(caption_sample)
            except VideoEndException:
                self.caption_container.export()
                break

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


if __name__ == '__main__':
    import sys
    video_path = sys.argv[1]
    scanner = Scanner(video_path)
    scanner.run((0, 315, 0, 337)) # 沈帅波
    # scanner.run((0, 301, 0, 320))  # 老曾 不稳定
    # scanner.run((0, 280, 0, 312))  # 阿杜早期
    # scanner.run((0, 293, 0, 325))  # 阿杜晚期
    # scanner.run((0, 305, 0, 330))  
    # scanner.run((0, 312, 0, 342))  #凉子访谈
    # scanner.run((0, 300, 0, 320))  #阿涛访谈
    # scanner.run((0, 326, 0, 352))  #老谢聊上海
    # scanner.run((0, 323, 0, 343))  #雪鸡
    # scanner.run((0, 282, 0, 301)) 
    # scanner.run((0, 319, 0, 335)) 
    # scanner.run((0, 317, 0, 341)) #铁锤
    # scanner.run((0, 299, 0, 321)) #程前
    # scanner.run((0, 307, 0, 332)) #程前
    # scanner.run((0, 313, 0, 336))
    # scanner.run((0, 300, 0, 321)) 
    # scanner.run((0, 327, 0, 343))  
    # scanner.run((0, 284, 0, 307)) 
    # scanner.run((0, 291, 0, 309)) 
    # scanner.run((0, 312, 0, 335))  #有数研究所
    # scanner.run((0, 307, 0, 332))  #暴富研究局
    # scanner.run((0, 327, 0, 346))  #峰弟
    # scanner.run((0, 314, 0, 336))  #RGB工具人
    # scanner.run((0, 316, 0, 345))  
    # scanner.run((0, 303, 0, 319))  # 刘小板
    # scanner.run((0, 310, 0, 335))  # 浪哥
    # scanner.run((0, 295, 0, 323))  # 李自然早期
    # scanner.run((0, 276, 0, 298))  # 李自然
    # scanner.run((0, 298, 0, 323))  # 金牛刀
    # scanner.run((0, 300, 0, 323))  # 致富经 厉害财经
    # scanner.run((0, 302, 0, 322))  # 对话
    # scanner.run((0, 282, 0, 305))  # 生财有道
    # scanner.run((0, 289, 0, 315)) # 央视财经
    # scanner.run((0, 319, 0, 342)) # 央视财经
    # scanner.run((96, 283, 118, 310)) #1818
    # scanner.run((0, 657, 0, 706)) # 开开心心
    # scanner.run((105, 616, 176, 652)) #非诚勿扰
  



