from modules import TimeProcessor as tp
from modules import TextProcessor
# import TimeProcessor as tp
# import TextProcessor
import t

def srt_block(time_block, text):
    global block_index
    time_block[0] = tp.convert(time_block[0])
    time_block[1] = tp.convert(time_block[1])
    rst = str(block_index)+'\n'+' --> '.join(time_block)+'\n'+text+'\n\n'
    block_index += 1
    return rst 

block_index = 1

def srt(text_path, time_path, dest_path):
    text = open(text_path, 'r').read()
    srt_file = open(dest_path,'w')
    text = TextProcessor.process(text)
    time = t.open_pickle(time_path)
    for line in text.split('\n'):
        if(not '/' in line):
            continue
        mark, text = line.split('/')
        try:
            start, end = mark.split('+')
            time_block = [time[start][0], time[end][1]]
            srt_file.write(srt_block(time_block, text))
        except Exception as e:
            time_block = time[mark]
            srt_file.write(srt_block(time_block, text))

if __name__ == '__main__':
    text_path = r'G:\字幕专家\2中译英\wp193\wp193.txt'
    time_path = r'G:\字幕专家\2中译英\wp193\wp193.pkl'   
    srt(text_path, time_path,'1.srt')