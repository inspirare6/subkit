import t 

def cvt_int_to_digit(integer, digit):
    if(digit==2):
        if integer<10:
            return '0'+str(integer)
        else:
            return str(integer)
    if(digit==3):
        if integer<10:
            return '00'+str(integer)
        elif(integer<100):
            return '0'+str(integer)
        else:
            return str(integer)

def convert(time_ms):
    hour = int(time_ms/1000/60/60)
    minute = int(time_ms/1000/60)
    second = int(time_ms/1000%60) 
    ms = time_ms%1000
    hour = cvt_int_to_digit(hour,2)
    minute = cvt_int_to_digit(minute,2)
    second = cvt_int_to_digit(second,2)
    ms = cvt_int_to_digit(ms,3)

    return '%s:%s:%s,%s'%(hour,minute,second,ms)

if __name__ == '__main__':
    time = t.open_pickle(r'G:\字幕专家\2中译英\wp193\wp193.pkl')
    # a = process(text)
    print(type(time))
    # print(a)