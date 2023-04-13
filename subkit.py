
from modules import Scanner, SubGenerator
from zgui import * 
from threading import Thread 
import t 



app = App().set_size(400,280).set_loc(1000,100).set_title('subkit')
root = app.instance


def func():
    pass

def on_click_scan():
    global video_path_input
    global caption_lower_input
    global caption_upper_input
    global white_threshold_input
    global consist_threshold_input

    video_path = video_path_input.get()
    caption_lower = int(caption_lower_input.get())
    caption_upper = int(caption_upper_input.get())
    white_threshold = int(white_threshold_input.get())
    consist_threshold = int(consist_threshold_input.get())
    # Scanner.scan(video_path, caption_lower, caption_upper, white_threshold, consist_threshold)

    thread = Thread(target=Scanner.scan, args=(video_path, caption_lower, caption_upper, white_threshold, consist_threshold))
    thread.daemon = True
    thread.start()

def on_click_text():
    global video_folder
    video_path = video_path_input.get()
    video_folder = t.get_folder(video_path)
    txt_path = t.path_join(video_folder,'text.txt')
    f = open(txt_path,'w')
    f.close()
    t.open_file(txt_path)

def on_click_gen_sub():
    global video_folder
    video_path = video_path_input.get()
    video_folder = t.get_folder(video_path)
    text_path = t.path_join(video_folder,'text.txt')
    time_path = t.path_join(video_folder,'time.pkl')
    sub_path = video_path.split('.')[0]+'.srt'
    try:
        SubGenerator.srt(text_path, time_path, sub_path)
    except Exception as e:
        print('字幕生成失败')
        print(e)
    else:
        print('字幕生成成功')

video_folder = None
app.label(root, '视频路径').grid(row=1, column=1, padx=1)
video_path_input = app.input(root, func)
video_path_input.grid(row=1, column=2, padx=1)

app.label(root, '字幕高低').grid(row=2, column=1, padx=1)
caption_lower_input = app.input(root, func)
# caption_lower_input.place(width=50, height=50) 
caption_lower_input.grid(row=2, column=2, padx=1)
caption_upper_input = app.input(root, func)
caption_upper_input.grid(row=2, column=3, padx=1)
app.label(root, '字幕色值 连续值').grid(row=3, column=1, padx=1)
white_threshold_input = app.input(root, func)
white_threshold_input.grid(row=3, column=2, padx=1)
consist_threshold_input = app.input(root, func)
consist_threshold_input.grid(row=3, column=3, padx=1)
scan_button = app.button(root, '扫描',on_click_scan)
scan_button.grid(row=4, column=1, padx=1)
scan_button = app.button(root, '中止',func)
scan_button.grid(row=4, column=2, padx=1)
scan_button = app.button(root, '粗译',on_click_text)
scan_button.grid(row=5, column=1, padx=1)
scan_button = app.button(root, '提词',func)
scan_button.grid(row=5, column=2, padx=1)
scan_button = app.button(root, '格式化',func)
scan_button.grid(row=6, column=1, padx=1)
scan_button = app.button(root, '字幕生成',on_click_gen_sub)
scan_button.grid(row=6, column=2, padx=1)

app.run()



if __name__ == '__main__':
    # video_path = r'G:\字幕专家\2中译英\wp146210元買了2條牛舌，今天做個新奇美食“椒麻牛舌”，又麻又辣，3碗飯都不夠吃！【半吨先生】.mp4'
    # Scanner.scan(video_path,625,681)
    pass
    # a = TimeProcessor.convert(100)
