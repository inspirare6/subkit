# -*- coding: utf-8 -*-
# @Author: de retour
# @Date:   2019-11-02 05:23:41
# @Last Modified by:   de retour
# @Last Modified time: 2019-12-31 18:50:34
from tkinter import *
from tkinter.messagebox import showinfo
class App:
    def __init__(self, setting = None):
        '''
        setting 窗口属性设置
        app =  App({'title':'123','size':(300,200),'loc':(500,300)})
        app.run()
        '''
        self.instance = Tk() 
        self.instance.wm_attributes('-topmost',1)    #窗口置顶 
        if(setting):
            if('title' in setting):   
                self.set_title(setting['title'])    
            if('size' in setting):   
                self.set_size(*setting['size'])  
            if('loc' in setting):   
                self.set_loc(*setting['loc'])      

    def set_title(self, title):
        '''设置标题'''
        self.instance.title(title)
        return self

    def set_size(self, width, height):
        '''设置窗口大小'''
        self.instance.geometry("%sx%s" % (width, height))
        return self

    def set_loc(self, x, y):
        '''设置窗口初始位置'''
        self.instance.geometry("+%s+%s" % (x, y))
        return self

    #组件类需要用pack()实例化
    def button(self, root, text, callback, **kwargs):
        '''按钮组件
        app.button('123',sayhi).pack()'''
        btn = Button(root, text = text, command = callback, **kwargs)
        return btn


    def message(self, text, **kwargs):
        '''按钮组件
        app.button('123',sayhi).pack()'''
        msg = Message(self.instance, text = text, **kwargs)
        return msg

    def text(self, width=100, height=100):
        '''文本显示编辑组件
        app.text().pack()
        '''
        text = Text(self.instance, width=width, height=height)
        return text

    def label(self, root, text, **kwargs): # text, bg, width, height, wraplength, justify
        '''
        app.label('haha').pack()
        '''
        tk_label = Label(root, text = text, **kwargs)
        return tk_label

    # def listbox(self, root, **kwargs):
    #     tk_listbox = Listbox(root, **kwargs)
    #     rety

    def alert(self, title, content):
        showinfo(title, content)

    def menu(self, root, items, **kwargs):
        '''列表组件
        app.menu(['鲍鱼','燕窝','鱼翅']).pack()'''
        tk_list = Listbox(root, **kwargs)
        for i, item in enumerate(items):
            tk_list.insert(i, item)
        return tk_list

    def string_var(self, text):
        return StringVar(value=text)

    def input(self, root, string_var, callback=print, **kwargs):
        tk_input = Entry(root, textvariable=string_var, **kwargs)
        tk_input.bind('<Return>', callback)
        return tk_input

    def run(self):
        '''启动窗口程序
        app.run()'''
        self.instance.mainloop() 


if __name__ == '__main__':
    app =  App({'title':'123','size':(300,200),'loc':(500,300)})
    app.run()
# def sayhi():
#     print('hi')

# def say(what):
#     print(what)

# app.text().pack()
# app.button('123',sayhi).pack()
# app.label('haha').pack()
# # app.menu(['鲍鱼','燕窝','鱼翅']).pack()
# app.input(say).pack()
# app.run()



# a = {'1':'a'}
# print('2' in a)
