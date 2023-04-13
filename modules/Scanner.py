from threading import Thread
import cv2
import t
import numpy as np


def get_timestamp():
    return int(time.time())

class VideoStream:
    def __init__(self, src):
        self.capture = cv2.VideoCapture(src)
        self.time_ms = 0

    def get_frame(self):
        self.capture.set(cv2.CAP_PROP_POS_MSEC, self.time_ms)
        (self.status, self.frame) = self.capture.read()
        rst =  {'time': self.time_ms,'frame': self.frame}
        self.time_ms += 200
        return rst

def extract_caption(vs,caption_lower, caption_upper, white_threshold = 230):
    # in: frames
    # out: captions
    tmp = vs.get_frame()
    frame = tmp['frame']
    time = tmp['time']
    screen_width = frame.shape[1]
    sample_left = int(screen_width/2-(caption_upper-caption_lower))
    sample_right = int(screen_width/2+(caption_upper-caption_lower)) 
    sample_region = frame[caption_lower:caption_upper,sample_left:sample_right]
    sample_region = cv2.cvtColor(sample_region, cv2.COLOR_BGR2GRAY)
    
    white_map = sample_region > white_threshold  
            
    white_total = white_map.sum()
    
    try:
        height, width = white_map.shape
        area = width * height
        ratio = white_total / area 
        print(ratio)
        if(ratio<0.05 or ratio>0.8):
            raise Exception('not a caption')
        # vertical_shape_vector = white_map.sum(axis=1)
        # horizontal_shape_vector = white_map.sum(axis=0)
        # shape_std = np.std(vertical_shape_vector)/np.mean(vertical_shape_vector)
        # if(shape_std<0.5 and shape_std>1):
        #     raise Exception('not a caption')
        # vertical_filled_rate = (vertical_shape_vector >2).sum()/len(vertical_shape_vector)
        # if(vertical_filled_rate<0.7):
        #     raise Exception('not a caption')
        # horizontal_filled_rate = (horizontal_shape_vector >2).sum()/len(horizontal_shape_vector)
        # if(horizontal_filled_rate<0.35):
        #     raise Exception('not a caption')
    except:
        return None
    caption = frame[caption_lower:caption_upper,:]
    return {'time': time, 'caption': caption, 'sample':white_map}    

def filter_captions(vs,caption_lower, caption_upper, white_threshold, consistency_threshold):
    # in: captions
    # out: caption blocks
    global captions 
    global time_sequences
    global prev_sample
    global time_start
    global last_time
    global caption_index
    tmp =  extract_caption(vs, caption_lower, caption_upper)
    if(tmp != None):
        time = tmp['time']
        caption = tmp['caption']
        sample = tmp['sample']
        try:
            if((time-last_time)>200):
                raise Exception('break point: natural ')
            else:
                d = calc_vector_distance(prev_sample, sample)
                if(d > consistency_threshold):
                    raise Exception('break point: surpass consistency threshold')
        except Exception as e:
            prev_sample = sample
            caption_receiver(caption_index, caption)
            time_sequences[str(caption_index-1)] = [time_start, last_time]
            time_start = time
            caption_index += 1
        last_time = time
        # print(time_sequences)

def calc_vector_distance(v1, v2):
    # in: matrix
    # out: diff
    return np.sqrt(np.sum(np.square(v1^v2)))


def caption_receiver(index, caption):
    global caption_output_index
    global caption_container
    caption = cv2.cvtColor(caption, cv2.COLOR_BGR2GRAY)
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(caption, str(index), (400,50), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 255, 0), 3) 
    if(caption_output_index < 1):
        caption_container = np.zeros(caption.shape)
    caption_container = concat_2d_matrix(caption_container,caption)
    if(caption_output_index%10==0):
        if(caption_output_index>0):
            cv2.imwrite(f'{video_folder}/captions/{get_timestamp()}.jpg',caption_container)
        caption_container = np.zeros(caption.shape)
    caption_output_index +=1

def write_left_captions():
    global caption_container
    global video_folder
    cv2.imwrite(f'{video_folder}/captions/{get_timestamp()}.jpg',caption_container)

def concat_2d_matrix(im1, im2):
    return np.concatenate([im1, im2],axis=0)

captions = []
time_sequences = {}
prev_sample = None
time_start = 0
last_time = 0
caption_index = 0
caption_output_index = 0
caption_container = None
video_folder = ''

def scan(video_path, caption_lower, caption_upper, white_threshold=230, consistency_threshold=20):
    global video_folder
    video_folder = t.get_folder(video_path)
    caption_folder = t.path_join(video_folder,'captions')
    t.mkdir(caption_folder)
    vs = VideoStream(video_path)
    while(True):
        try:
            filter_captions(vs, caption_lower, caption_upper, white_threshold, consistency_threshold)
        except:
            write_left_captions()
            break
    t.save_pickle(video_folder+'\\time.pkl',time_sequences)

if __name__ == '__main__':
    video_path = r'G:\字幕专家\2中译英\wp146210元買了2條牛舌，今天做個新奇美食“椒麻牛舌”，又麻又辣，3碗飯都不夠吃！【半吨先生】.mp4'
    scan(video_path,625,681)
    
  



