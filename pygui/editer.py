#!/usr/bin/env python

"""
    1年前的练习题
"""
import Tkinter
import tkFileDialog,tkMessageBox
from idlelib.Percolator import Percolator
from idlelib.ColorDelegator import ColorDelegator
from idlelib.textView import TextViewer
import os,webbrowser
class Windows:
    def __init__(self):
        self.root = Tkinter.Tk()
        self.Opition=self.makeMenu()
        self.text = self.makeText()
        self.filename=None
        Percolator(self.text).insertfilter(ColorDelegator())
        #self.flag=True
        self.root.title("Simple IDE")
    def makeText(self):
        text = Tkinter.Text(self.root,selectbackground='blue',selectforeground='gray',undo=True)
        text.pack()
        return text
    def makeMenu(self):
        #生成菜单
        menu = Tkinter.Menu(self.root)
        #生成下拉菜单
        submenu = Tkinter.Menu(menu,tearoff=0)
        submenu.add_command(label='Open',command=self.fileOpen)
        #submenu.add_separator()#分割线测试
        submenu.add_command(label='Save',command=self.fileSave)
        submenu.add_command(label='Close',command=self.root.destroy)
        #下拉菜单添加到菜单之中
        menu.add_cascade(label="File",menu=submenu)

        submenu = Tkinter.Menu(menu,tearoff=0)
        submenu.add_command(label='RunScript',command=self.runScript)
        submenu.add_command(label='Redo',command=self.redo)
        submenu.add_command(label='Undo',command=self.undo)
        submenu.add_command(label='SelectAll',command=self.selectAll)
        menu.add_cascade(label="Edit",menu=submenu)

        submenu = Tkinter.Menu(menu,tearoff=0)
        submenu.add_command(label="isPyScript",command=self.isPyScript)
        menu.add_cascade(label="Options",menu=submenu)
        
        submenu = Tkinter.Menu(menu,tearoff=0)
        submenu.add_command(label='About IDE',command=self.showHelp)
        submenu.add_command(label='Author',command=self.showAuthor)
        submenu.add_command(label='PyDoc',command=self.showPydoc)
        submenu.add_command(label='Link Us',command=self.linkUs)
        menu.add_cascade(label="Help",menu=submenu)
        self.root.config(menu=menu)
        return menu
    def showPydoc(self):
        webbrowser.open("http://docs.python.org/2/index.html")
    def linkUs(self):
        webbrowser.open('http://shell-von.lofter.com/')
    def selectAll(self):
        self.text.tag_add(Tkinter.SEL, "1.0", Tkinter.END)
    def redo(self):
        try:
            self.text.edit_redo()
        except Tkinter.TclError:
           pass
    def undo(self):
        try:
            self.text.edit_undo()
        except Tkinter.TclError:
            pass
    def isPyScript(self):
        pass
    def showLineNum(self):
        txt = self.text.get("1.0",Tkinter.END)
        line = txt.split("\n")
        for i in xrange(len(line[:])):
            line[i]="%4s"%(i+1)+"\t"+line[i]
        txt="\n".join(line)
        
    def runScript(self):
        if self.filename:
            try:
                execfile(self.filename)
            except:
                tkMessageBox.showerror("Run Error",'Error:\nPlease check again!')
        else:
            tkMessageBox.showinfo('Warnning',' it is an empty file')
    def showAuthor(self):
        tkMessageBox.showinfo('A Simple IDE','  shell-von\nversion:0.0.1')
    def showHelp(self):
        TextViewer(self.root, "About IDE", open(os.getcwd()+'\\readme.txt','rb').read())
    def fileOpen(self):
        self.filename = tkFileDialog.askopenfilename(title="IDE",filetypes=[('python','*.py *.pyw'),('All files','*')])
        if self.filename:
            data = open(self.filename).read()
            if len(self.text.get("1.0",Tkinter.END))>1:
                t=tkMessageBox.askokcancel('Warnning','you have data!!\nare you sure?')
                if t:
                    self.text.delete("1.0",Tkinter.END)
                else:
                    return
            self.text.insert(Tkinter.INSERT,data)
    def fileSave(self):
        self.filename = tkFileDialog.asksaveasfilename(title="IDE",initialdir=r'E:\python',initialfile='Undefined.py')
        if self.filename:
            data = open(self.filename,'w')
            txt = self.text.get("1.0",Tkinter.END)
            data.write(txt)
            data.close()
if __name__ == '__main__':
    Windows().root.mainloop()