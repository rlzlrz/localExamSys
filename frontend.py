import tkinter as tk
from tkinter import messagebox
import backend, configure
from threading import Timer

class FrontEnd():
    def __init__(self):
        self.count = 0
        # 考试时间，单位：分钟
        self.minute = configure.EXAM_MINUTE
        # 考试时间，单位：秒
        self.second = 0
        # 考生得分
        self.score = 0
        # 考生作答内容
        self.ans = []
        # 生成题库
        self.questionList = backend.backEnd()
        # 考试是否结束 
        self.state = False
        # 登录窗口
        self.loginWindow = tk.Tk()
        self.initialLoginWindow(self.loginWindow)

    
    def initialLoginWindow(self, loginWindow):
        loginWindow['bg'] = '#999999'
        loginWindow.title('login')
        loginWindow.resizable(width=True, height=True)
        loginWindow.geometry(configure.EXAM_RESOLUTION)
        self.varAccount = tk.StringVar()
        self.varAccount.set('')
        self.varKey = tk.StringVar()
        self.varKey.set('')

        # 创建标签
        self.labelAccount = tk.Label(
            loginWindow,
            text='User Name',
            justify=tk.RIGHT,
            font=('Arial', 14),
            width=80)
        self.labelKey = tk.Label(
            loginWindow,
            text='Password',
            font=('Arial', 14),
            justify=tk.RIGHT,
            width=80)
        self.labelRegister = tk.Label(
            loginWindow, text='Register', justify=tk.RIGHT, width=80)

        #为窗口的标签设置属性
        self.labelAccount.place(x=20, y=10, width=160, height=40)
        self.labelKey.place(x=20, y=60, width=160, height=40)

        # 创建账号文本框，同时设置关联的变量
        self.account = tk.Entry(
            loginWindow,
            width=80,
            textvariable=self.varAccount)
        self.account.place(x=200, y=10, width=160, height=40)
        #self.account=tk.Label(font=('Arial',12),justify='center')
        
        # 创建密码文本框
        self.key = tk.Entry(
            loginWindow,
            show='*',
            width=80,
            textvariable=self.varKey)
        self.key.place(x=200, y=60, width=160, height=40)

         # 创建按钮组件，同时设置按钮事件处理函数
        buttonOk = tk.Button(loginWindow, text='Login', command=self.login)
#        buttonOK=tk.Label(font=('Arial', 14))
        buttonOk.place(x=20, y=140, width=100, height=40)
        buttonRegister = tk.Button(loginWindow, text='Register', command=self.regist)
        buttonRegister.place(x=260, y=140, width=100, height=40)

        # make Esc exit the program
        loginWindow.bind('<Escape>', lambda e: loginWindow.destroy())
        # 启动消息循环
        loginWindow.mainloop()

    def login(self):
        account = self.account.get()
        passwd = self.key.get()
        ret = backend.authCheck(account, passwd)
        if ret == True:
            messagebox.showinfo(title='LOGIN', message='Login in Successfully!')
            self.loginWindow.destroy()
            self.mainWindow = tk.Tk()
            self.initialMainWindow()
            return
        messagebox.showinfo('Oops!', message='bad account or passwd!')

    def regist(self):
        account = self.account.get()
        passwd = self.key.get()
        ret = backend.registCheck(account)
        if ret == True:
            backend.addUser(account, passwd)
            return
        messagebox.showinfo('Oops!', message='Your account could be used!')

    def initialMainWindow(self):
        self.mainWindow.geometry(configure.EXAM_RESOLUTION)
        self.mainWindow['bg'] = '#E4E5B5'
        self.mainWindow.title('Main Window')
        self.mainWindow.resizable(width=True, height=True)

        self.mainWindow.protocol('WM_DELETE_WINDOW', self.closeMainWindow)
        # self.setMenu(self.mainWindow)
        # make Esc exit the program
        self.mainWindow.bind('<Escape>', lambda e: self.mainWindow.destroy())

        self.printQuestion()
        self.watchDog()
        self.mainWindow.mainloop()

    def printQuestion(self):
        t = self.questionList.Questions[self.count]
        self.Q = tk.Label(self.mainWindow, text = t['question'])
        self.questioncount =tk.StringVar()
        self.questioncount.set('Question:'+str(self.questionList.Questions[self.count]['count']))
        self.Qcount = tk.Label(self.mainWindow, textvariable = self.questioncount)
        self.Qcount.pack(side = 'right')
        self.Q.place(x = 20, y = 10, width = 100, height = 50)
        self.A = tk.Entry(self.mainWindow, bd = 5)
        self.A.place(x = 130, y = 10, width = 100, height = 50)
        submitButton = tk.Button(self.mainWindow, text = 'Submit', command = self.submit)
        submitButton.place(x = 20, y = 70, width= 210, height= 50)

        self.varTimeLeft = tk.StringVar()
        self.timeLabel = tk.Label(self.mainWindow, textvariable= self.varTimeLeft)
        self.timeLabel.place(x = 20, y = 200, width= 210, height= 50)

    def submit(self):
        self.ans.append(self.A.get())
        if self.ans[self.count] == int(self.questionList.Questions[self.count]['answer']):
            self.score += 1
        if self.count < 20:
            self.count += 1
            self.printQuestion()
        else:
            self.showDoneFsm()

    def closeMainWindow(self):
        # 确认是否退出程序
        ans = messagebox.askyesno(title='Exit', message='Do you really want to exit?')
        if ans:
            self.mainWindow.destroy()
        else:
            pass

    def watchDog(self):
        """ 定时程序，时间最多一小时"""
        timeLeft = 60 * self.minute + self.second

        timeLeft -= 1
        self.second = self.second - 1
        if self.second < 0:
            self.minute = self.minute - 1
            self.second = 59
        if self.minute < 0 or timeLeft == 0:
            self.state = True
            self.showDoneFsm()
        self.varTimeLeft.set(str(self.minute) + ':' + str(self.second))
        self.timeCount = Timer(1, self.watchDog, ())
        self.timeCount.start() # 计时器启动


    def showDoneFsm(self):
        messagebox.showinfo('Exam Done!', message='your score is %d' %self.score)
        self.mainWindow.destroy()


    





if __name__ == '__main__':
    window = FrontEnd()
