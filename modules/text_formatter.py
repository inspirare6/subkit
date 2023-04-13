def word_capture(text_path):
    text = open(text_path,'r').read()
    b = re.findall(r'([a-zA-Z]*),,',text,re.M)
    b = list(set(b))
    with open('wordlist.txt','w') as f:
        f.write(',\n'.join(b))
        f.close()
    t.open_file('wordlist.txt')

def word_replace(text_path):
    text = open(text_path,'r').read()
    pairs =[
        [" i "," I "],
        [" u ","you"],
        ["\nu ","\nyou "],
        [" r ","are"],
        ["\nr ","\nare "],
        [" yr "," you are "],
        ["\nyr ","\nyou are "],
        ["whats","what's"],
        ["dont","don't"],
        ["wont","won't"],
        ["dst","doesn't"],
        ["cant","can't"],
        ["i'm","I'm"],
        ["i'll","I'll"],
        ["i've","I've"],
        ["hv","have"],
        ["gv","give"],
        ["ft","father"],
        ["mt","mother"],
        ["remb","remember"],
        ["pls","please"],
        ["mum","Mum"],
        ["dad","Dad"],
        ["rmb","RMB"],
        ["god","God"]
    ]
    for pair in pairs:
        text = text.replace(pair[0],pair[1])
    with open('wordlist.txt','r') as f:
        content = f.read()
        for line in content.split('\n'):
            try:
                old, new = line.split(',')
                text = text.replace(old+',,',new)
                text = text.replace(old,new)
            except:
                pass
    with open(text_path,'w') as f:
        f.write(text)        
        f.close()


def format(text_path):
    src = open(text_path,'r')
    dest = open(text_path,'w')
    text = src.read()
    
    import re

    text_buffer = ''
    for (index, block) in enumerate(text.split('\n\n')):
        if(index>0):
            text_buffer += '\n\n'
        block_buffer = ''
        for (index2, line) in enumerate(re.split(r'\n\s{0,}',block)):
            if(index2>0):
                block_buffer += '\n'
            line = line.strip()
            try:
                line = line[0].upper()+line[1:]
                block_buffer += line
            except:
                block_buffer += line
        text_buffer += block_buffer 
    text = text_buffer

    text_buffer = ''
    for (index, line) in enumerate(re.split('\.\s{1,}',text)):
        if(index>0):
            text_buffer += '. '
        line = line.strip()
        try:
            line = line[0].upper()+line[1:]
            text_buffer += line
        except:
            text_buffer += line
    text = text_buffer

    text_buffer = ''
    for (index, line) in enumerate(re.split(r'\?[^\S\n]{1,}',text)):
        if(index>0):
            text_buffer += '? '
        line = line.strip()
        try:
            line = line[0].upper()+line[1:]
            text_buffer += line
        except:
            text_buffer += line
    text = text_buffer

    dest.write(text)

    src.close()
    dest.close()
    t.rm(src)
    t.mv(dest,src)
