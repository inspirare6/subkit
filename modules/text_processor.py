import t
import re 

def process(content):
    text = ''
    for block in content.split('\n\n'):
        tmp_index = 0
        if('*' in block):
            b = re.findall(r'([0-9]*)\*([\s\S]*)\n([0-9]*)\*',block,re.M)
            index = int(b[0][0])
            block = b[0][1]
            # print(block)
            block_end = int(b[0][2])
            for block_line in block.split('\n'):
                if(tmp_index==0):
                    block_line = block_line[0].upper()+block_line[1:]
                tmp_index += 1
                if('/' in block_line):
                    x,y = block_line.split('/')
                    y = y[0].upper()+y[1:]
                    if('+' in x):
                        start, end = x.split('+')
                        text +=  x+'/'+y+'\n'
                        if(index!=int(start)):
                                raise Exception('marks wrong at index %s, block: %s'%(index,y))
                        index = int(end)+1
                    else:
                        length = int(x)
                        text += str(index)+'+'+str(index+length-1)+'/'+y+'\n'
                        index +=  length
                    continue
                block_line = block_line[0].upper()+block_line[1:]
                text += '%s/%s'%(index,block_line)+'\n'
                index +=  1
            if(index!=(block_end+1)):
                raise Exception(str(index)+'marks wrong: block end %s'%block_end)
        else:
            x,y = block.split('/')
            y = y[0].upper()+y[1:]
            if('+' in x):
                start, end = x.split('+')  #unfinished
                text += x+'/'+y+'\n'
                index =  int(end)+1
            else:
                text += x+'/'+y+'\n'
                index +=  int(x) +1
    return text

if __name__ == '__main__':
    text = open(r'G:\字幕专家\2中译英\wp193\wp193.txt','r').read()
    a = process(text)
    print(a)