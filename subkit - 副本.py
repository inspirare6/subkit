from gui import *

def init():
    app = App().set_size(400,400).set_loc(1000,100).set_title('subkit')

    def func(e):
        pass

    def to_quick_scan():
        video_path = video_path_input.get()
        endtime = int(endtime_input.get())
        caption_lower = int(caption_lower_input.get())
        caption_upper = int(caption_upper_input.get())
        white_threshold = int(white_threshold_input.get())
        consistency_threshold = int(consistency_threshold_input.get())
        from threading import Thread
        global fbp
        fbp = frame_batch_processor()
        thread = Thread(target=fbp.run, args=(video_path, endtime, caption_lower, caption_upper, white_threshold, consistency_threshold))
        thread.daemon = True
        thread.start()

    def cancel_shot():
        global fbp  
        fbp.stop()

    def to_word_replace():
        video_path = video_path_input.get()
        word_replace(video_path)

    def to_word_capture():
        video_path = video_path_input.get()
        word_capture(video_path)

    def to_sub_format():
        video_path = video_path_input.get()
        sub_format(video_path)

    def to_gen_srt():
        video_path = video_path_input.get()
        gen_srt(video_path)
        
    def to_text():
        def new_text():
            pass
        video_path = video_path_input.get()
        new_text()
        # with open


    fbp = None
    app.label('video path').grid(row=1, column=1, padx=1)
    video_path_input = app.input(func)
    video_path_input.grid(row=1, column=2, padx=1)
    app.label('end time').grid(row=1, column=3, padx=1)
    endtime_input = app.input(func)
    endtime_input.grid(row=1, column=4, padx=1)
    app.label('caption lower').grid(row=2, column=1, padx=1)
    caption_lower_input = app.input(func)
    caption_lower_input.grid(row=2, column=2, padx=1)
    app.label('caption upper').grid(row=3, column=1, padx=1)
    caption_upper_input = app.input(func)
    caption_upper_input.grid(row=3, column=2, padx=1)
    app.label('white threshold').grid(row=4, column=1, padx=1)
    white_threshold_input = app.input(func)
    white_threshold_input.grid(row=4, column=2, padx=1)
    app.label('consistency threshold').grid(row=5, column=1, padx=1)
    consistency_threshold_input = app.input(func)
    consistency_threshold_input.grid(row=5, column=2, padx=1)
    app.label('caption number').grid(row=5, column=3, padx=1)
    caption_number_input = app.input(func)
    caption_number_input.grid(row=5, column=4, padx=1)

    app.button('scan',to_quick_scan).grid(row=7, column=1, padx=1)
    app.button('cancel scan',cancel_shot).grid(row=8, column=1, padx=1)
    app.button('text',to_text).grid(row=9, column=1, padx=1)
    app.button('word capture',to_word_capture).grid(row=10, column=1, padx=1)
    app.button('word replace',to_word_replace).grid(row=11, column=1, padx=1)
    app.button('format text',to_sub_format).grid(row=12, column=1, padx=1)
    app.button('gen sub',to_gen_srt).grid(row=13, column=1, padx=1)
    

    app.run()                 


if __name__ == '__main__':
    init()