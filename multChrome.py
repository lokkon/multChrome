import tkinter as tk
import tkinter.font as tkfont
import tkinter.messagebox
import json
import win32process
import ctypes, sys, os
import base64
from icon import img

tmp = open("tmp.ico", "wb+")
tmp.write(base64.b64decode(img))
tmp.close()

class Display():

    def __init__(self):
        self.win = tk.Tk()
        self.win.title('Chrome多开管理器')
        self.win.geometry('350x400')
        self.menu = tk.Menu(self.win, tearoff=0)
        self.usersfile = 'users.json'
        self.win.iconbitmap("tmp.ico")
        os.remove("tmp.ico")
        # win.configure(background='white')

    def draw(self):
        title = tk.Label(self.win,text="Chrome多开管理器",font=tkfont.Font(family='黑体', size=16),justify='center')
        title.pack(side="top", padx=10, pady=10, fill="both")

        add_user_frm = tk.Frame(self.win)
        add_user_frm.pack(side="top", padx=5, pady=5, fill="both")
        target_label = tk.Label(add_user_frm, text="添加用户")
        target_label.pack(side="left", padx=10, pady=5)
        #用户名输入窗
        var_new_user = tk.StringVar()
        new_user_entry = tk.Entry(add_user_frm, width=20, textvariable=var_new_user)
        new_user_entry.pack(side="left", padx=10, pady=5)

        add_user_button = tk.Button(add_user_frm, text='添加', width=12, command=lambda: self.add_user(var_new_user))
        add_user_button.pack(side="left", padx=10, pady=5)

        #读取用户名列表
        var_user_lb = tk.StringVar()
        user_list_frm = tk.Frame(self.win)
        user_list_frm.pack(side="left", padx=10, pady=5, fill="y")
        user_scrollbar = tk.Scrollbar(user_list_frm)
        user_scrollbar.pack(side="right", fill="y")
        user_lb = tk.Listbox(user_list_frm, width=26, height=50, selectmode=tk.EXTENDED,
                             yscrollcommand=user_scrollbar.set, listvariable=var_user_lb)
        user_lb.pack(side="top", padx=10, pady=10)
        user_scrollbar.config(command=user_lb.yview)
        self.user_lb = user_lb
        self.readUser()     #读取用户名文档并添加至列表
        # print(var_user_lb.get())  #测试输出整个用户名列表
        #通过双击事件选中并打开用户浏览器窗口
        user_lb.bind("<Double-Button-1>", self.selectedUser)

        #打开按钮
        r0_frm = tk.Frame(self.win)
        r0_frm.pack(side="top", padx=5, pady=10, fill="both")
        open_buttom = tk.Button(r0_frm, text='打开', width=12, command=self.selectedUser)
        open_buttom.pack(side="left", padx=0, pady=0)

        #移除按钮
        r1_frm = tk.Frame(self.win)
        r1_frm.pack(side="top", padx=5, pady=10, fill="both")
        remove_buttom = tk.Button(r1_frm, text='移除', width=12, command=self.remove_user)
        remove_buttom.pack(side="left", padx=0, pady=0)

        # #移除并删除数据按钮，权限问题未启用
        # r2_frm = tk.Frame(self.win)
        # r2_frm.pack(side="top", padx=5, pady=10, fill="both")
        # delete_buttom = tk.Button(r2_frm, text='移除并删除数据', width=40, command=self.delete_user)
        # delete_buttom.pack(side="left", padx=0, pady=0)

        #打开用户文件夹
        r3_frm = tk.Frame(self.win)
        r3_frm.pack(side="top", padx=5, pady=10, fill="both")
        remove_buttom = tk.Button(r3_frm, text='打开用户文件夹', width=12, command=self.open_userfolder)
        remove_buttom.pack(side="left", padx=0, pady=0)

        self.win.mainloop()


    def selectedUser(self, event=None):
        users = self.user_lb.curselection()  # 提取点中选项的下标
        for i in users:
            user = self.user_lb.get(i)  # 提取点中选项下标的值
            openChrome(user)


    def add_user(self,var_new_user):
        new_user = var_new_user.get()
        try:
            if new_user.isalnum():
                with open(self.usersfile, 'r', encoding='utf-8') as f_obj:
                    file = f_obj.read()
                    if len(file) == 0:
                        user_list = []
                        user_list.append(new_user)
                    else:
                        user_list = json.loads(file)
                        # print(user_list)
                        if new_user in user_list:
                            tk.messagebox.showerror('错误','该用户已存在！')
                        else:
                            user_list.append(new_user)
                            self.user_lb.insert('end', new_user)
                with open(self.usersfile, 'w') as f_obj:
                    json.dump(user_list, f_obj)
            else:
                tk.messagebox.showerror('错误', '输入格式错误！仅限数字及字母')
        except FileNotFoundError:
            with open(self.usersfile, 'w') as f_obj:
                user_list = []
                user_list.append(new_user)
                json.dump(user_list, f_obj)
                self.user_lb.insert('end', new_user)

    def readUser(self):
        try:
            with open(self.usersfile, 'r', encoding='utf-8') as f_obj:
                user_list = json.load(f_obj)
                for user in user_list:
                    self.user_lb.insert('end', user)
        except FileNotFoundError:
            print('File not found, please add user first')

    def remove_user(self):
        users = self.user_lb.curselection()  # 提取点中选项的下标
        for i in range(len(users)-1,-1,-1):
            user = self.user_lb.get(users[i])
            with open(self.usersfile, 'r', encoding='utf-8') as f_obj:
                user_list = json.load(f_obj)
            user_list.remove(user)
            self.user_lb.delete(users[i])
            with open(self.usersfile, 'w') as f_obj:
                json.dump(user_list, f_obj)

    #删除数据因权限问题暂未实现
    # def delete_user(self):
    #     user = self.user_lb.get(self.user_lb.curselection())
    #     appdata = os.getenv("LOCALAPPDATA")
    #     user_data = appdata + r'\Google\Chrome\User Data' + '\\' + user
    #     print(user_data)
    #     if os.path.exists(user_data):
    #         if is_admin():
    #             os.remove(user_data)
    #             print('deleted')
    #             self.remove_user()
    #         else:
    #             if sys.version_info[0] == 3:
    #                 ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
    #     else:
    #         print('file does not exist')


    def open_userfolder(self):
        users = self.user_lb.curselection()  # 提取点中选项的下标
        for i in users:
            user = self.user_lb.get(i)
            appdata = os.getenv("LOCALAPPDATA")
            user_data = appdata + r'\Google\Chrome\User Data' + '\\' + user
            # print(user_data)
            if os.path.exists(user_data):
                os.startfile(user_data)
            else:
                tk.messagebox.showerror('错误', '用户 ' + user + ' 文件不存在！')

def openChrome(user_name):
    chrome_baseurl = 'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'
    chrome_url = chrome_baseurl + '  --profile-directory="%s"' % user_name
    win32process.CreateProcess(None, chrome_url, None, None, 0, win32process.CREATE_NO_WINDOW, None, None,
                               win32process.STARTUPINFO())

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False





my = Display()
my.draw()

