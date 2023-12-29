import wx
import os
import sys
import time
from PIL import Image
from utils import csv_fun as C
from utils import timefun as T
from utils import Dlog as D
from utils import txtfun as TF
from utils import version as V

from utils.fpath import *


ID_ABOUT = 101
ID_UPDATE = 102
ID_ADD = 201
ID_LOOK = 202
ID_DAY = 203


class MainFrame(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, size=(550, 340))
        self.initUI()


    def initUI(self):
        self.panel = wx.Panel(self, -1)
        ix = 42
        wx.StaticText(self.panel, label="时间记录工具", pos=(ix, 22))

        self.pic_path = os.path.join(pic_path, "blue_eyes.jpg")
        img = Image.open(self.pic_path)
        imsize = (200, 200)
        img = img.resize(imsize, Image.ANTIALIAS)  # 指定目标尺寸并使用抗锯齿算法
        img = img.convert("RGB")  # 将图像转换为RGB模式，wx.Bitmap需要RGB图像

        # 创建 wx.StaticBitmap 控件，并将缩放后的图像转换为 wx.Bitmap
        bmp = self.pil_image_to_wx_bitmap(img)
        self.bitmap = wx.StaticBitmap(self.panel, -1, bmp, pos=(247, 20), size=imsize)


        self.buttonStart = wx.Button(self.panel, -1, "Start", (ix, 52), (60, 30))
        self.panel.Bind(wx.EVT_BUTTON, self.OnClick, self.buttonStart)
        self.buttonShow = wx.Button(self.panel, -1, "Show", (ix, 112), (60, 30))
        self.panel.Bind(wx.EVT_BUTTON, self.OnClick, self.buttonShow)
        self.buttonDel = wx.Button(self.panel, -1, "Del", (ix, 172), (60, 30))
        self.panel.Bind(wx.EVT_BUTTON, self.OnClick, self.buttonDel)

        self.setBar()   # 设置状态栏
        self.setMenu()
        self.setupIcon()
        self.Center()


    def pil_image_to_wx_bitmap(self, pil_image):
        width, height = pil_image.size
        image = wx.Image(width, height)
        image.SetData(pil_image.convert("RGB").tobytes())
        wx_bitmap = wx.Bitmap(image)
        return wx_bitmap



    def OnClick(self, event):
        if event.GetEventObject() == self.buttonStart:
            self.start()
        elif event.GetEventObject() == self.buttonDel:
            self.del_()
        elif event.GetEventObject() == self.buttonShow:
            self.show_()

    def show_(self):
        dlg = ShowDialog(None, 0)
        self.hish(dlg)

    def del_(self):
        dlg = DelDialog(None, -1)
        self.hish(dlg)

    def start(self):
        dlg = StaDialog(None, -1)
        self.hish(dlg)

    def Notify(self):
        t = time.localtime(time.time())
        st = time.strftime('%Y-%m-%d  %H:%M:%S', t)
        self.SetStatusText(st, 1)

    def setBar(self):
        # 创建状态栏
        sb = self.CreateStatusBar(2)
        self.SetStatusWidths([-1, -2])
        self.SetStatusText("Created by DQZ", 0)

        self.timer = wx.PyTimer(self.Notify)
        self.timer.Start(1000, wx.TIMER_CONTINUOUS)
        self.Notify()

    def setMenu(self):
        menubar = wx.MenuBar()

        fmenu = wx.Menu()  # 创建子菜单项 "File"
        ab_menu = wx.MenuItem(fmenu, ID_ABOUT, "使用说明(&H)", "How to use this tool")
        ab_menu.SetBitmap(wx.Bitmap(os.path.join(pic_path, "ab.png")))
        up_menu = wx.MenuItem(fmenu, ID_UPDATE, "更新日志(&U)", "Details of Update")
        up_menu.SetBitmap(wx.Bitmap(os.path.join(pic_path, "up.png")))
        fmenu.Append(ab_menu)
        fmenu.Append(up_menu)

        menubar.Append(fmenu, "关于")  # 将 "MI" 添加到菜单栏

        tmenu = wx.Menu()  # 创建子菜单项 "File"
        ad_menu = wx.MenuItem(fmenu, ID_ADD, "项目导入(&A)", "Add project and its time")
        ad_menu.SetBitmap(wx.Bitmap(os.path.join(pic_path, "Targets.png")))
        tmenu.Append(ad_menu)
        # 查看记录功能
        lk_menu = wx.MenuItem(fmenu, ID_LOOK, "查看当日记录(&L)", "Today's records")
        lk_menu.SetBitmap(wx.Bitmap(os.path.join(pic_path, "饭团.png")))
        tmenu.Append(lk_menu)
        # 琐事记录功能
        dy_menu = wx.MenuItem(fmenu, ID_DAY, "日常琐事(&D)", "Daily routine")
        dy_menu.SetBitmap(wx.Bitmap(os.path.join(pic_path, "米饭.png")))
        tmenu.Append(dy_menu)

        menubar.Append(tmenu, "更多功能")

        self.SetMenuBar(menubar)

        self.Bind(wx.EVT_MENU, self.OnMenuAbout, id=ID_ABOUT)
        self.Bind(wx.EVT_MENU, self.OnMenuUpdate, id=ID_UPDATE)
        self.Bind(wx.EVT_MENU, self.OnMenuAdd, id=ID_ADD)
        self.Bind(wx.EVT_MENU, self.OnMenuLOOK, id=ID_LOOK)
        self.Bind(wx.EVT_MENU, self.OnMenuDAY, id=ID_DAY)

    def setupIcon(self):
        self.img_path = os.path.join(pic_path, "logo.png")
        icon = wx.Icon(self.img_path, type=wx.BITMAP_TYPE_PNG)
        self.SetIcon(icon)

    def readtxt(self, filename):
        filepath = os.path.join(BASE_DIR, "res", filename)
        with open(filepath, "r", encoding="utf-8") as file:
            info = file.read()
        return info

    def OnMenuAbout(self, event):
        info = self.readtxt("about.txt")
        dlg = ShowInfo(None, -1, info, "使用说明")
        self.hish(dlg)

    def OnMenuUpdate(self, event):
        info = self.readtxt("update.txt")
        dlg = ShowInfo(None, -1, info, "Update Info")
        self.hish(dlg)

    def OnMenuAdd(self, event):
        dlg = D.AddDialog(None, 3)
        self.hish(dlg)

    def OnMenuLOOK(self, event):
        dlg = D.RecDialog(None, 4)
        self.hish(dlg)

    def OnMenuDAY(self, event):
        dlg = D.DayDialog(None, 5)
        self.hish(dlg)

    def hish(self, dlg):
        self.Hide()
        dlg.ShowModal()
        dlg.Destroy()
        self.Show()

class ShowDialog(wx.Dialog):
    def __init__(self, parent, id):
        super(ShowDialog, self).__init__(parent, id, "历史时间记录", size=(350, 500))
        self.app = wx.GetApp()
        self.panel = self.app.frame

        # 图标
        D.button_icon(self, "show.png")

        self.Center()
        info = C.show_info(file_path)
        wx.StaticText(self, label=info, pos=(40, 20), size=(300, -1))
        wx.Button(self, wx.ID_OK, pos=(135, 400))

class ShowInfo(wx.Dialog):
    def __init__(self, parent, id, info, title):
        super(ShowInfo, self).__init__(parent, id, title, size=(300, 200))
        self.app = wx.GetApp()
        self.panel = self.app.frame
        self.Center()
        wx.StaticText(self, label=info, pos=(40, 20), size=(200, 110), style=wx.ALIGN_CENTER|wx.EXPAND)
        wx.Button(self, wx.ID_OK, pos=(135, 400))

class DelDialog(wx.Dialog):
    def __init__(self, parent, id):
        super(DelDialog, self).__init__(parent, id, "删除记录", size=(350, 250))
        self.app = wx.GetApp()
        self.panel = self.app.frame

        wx.StaticText(self, label="所要删除的项目名称：", pos=(20, 24))
        self.proj = wx.TextCtrl(self, pos=(145, 20))

        D.show_exit_projs(self)

        self.submit_btn = wx.Button(self, label="提交", pos=(135, 140))
        self.Bind(wx.EVT_BUTTON, self.OnClick, self.submit_btn)
        self.Bind(wx.EVT_CHAR_HOOK, self.OnChar)

        # 图标
        D.button_icon(self, "历史数据.png")

        self.Center()

    def OnClick(self, event):
        proj = self.proj.GetValue()
        C.del_2(file_path, proj)
        dlg = ShowDialog(None, -1)
        self.Close()
        dlg.ShowModal()
        dlg.Destroy()


    def OnChar(self, event):
        keycode = event.GetKeyCode()
        if keycode == wx.WXK_RETURN or keycode == wx.WXK_NUMPAD_ENTER:
            self.OnClick(event)
        else:
            event.Skip()

class StaDialog(wx.Dialog):
    def __init__(self, parent, id):
        super(StaDialog, self).__init__(parent, id, "开始（项目专用）", size=(350, 250))
        self.app = wx.GetApp()
        self.panel = self.app.frame
        wx.StaticText(self, label="所要进行的项目名称", pos=(20, 24))

        D.show_exit_projs(self)


        self.proj = wx.TextCtrl(self, pos=(145, 20))
        self.submit_btn = wx.Button(self, label="开始计时", pos=(135, 140))
        self.Bind(wx.EVT_BUTTON, self.OnClick, self.submit_btn)
        self.Bind(wx.EVT_CHAR_HOOK, self.OnChar)

        # 图标
        D.button_icon(self, "我的流程.png")

        self.Center()
    def OnClick(self, event):
        proj = self.proj.GetValue()
        info = C.change_info(file_path, proj)
        dlg = TimDialog(None, 1, info, proj)
        self.Close()
        dlg.ShowModal()
        dlg.Destroy()

    def OnChar(self, event):
        keycode = event.GetKeyCode()
        if keycode == wx.WXK_RETURN or keycode == wx.WXK_NUMPAD_ENTER:
            self.OnClick(event)
        else:
            event.Skip()


class TimDialog(wx.Dialog):
    def __init__(self, parent, id, info, proj):
        super(TimDialog, self).__init__(parent, id, "计时开始", size=(350, 200))
        _, self.begin_t = TF.da_hour()
        self.start_time = time.time()
        self.proj = proj
        self.app = wx.GetApp()
        self.panel = self.app.frame
        self.elapsed_time_label = wx.StaticText(self, label="", pos=(20, 60), size=(300, -1))

        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.update_elapsed_time, self.timer)
        self.timer.Start(1000)  # 每1000毫秒（1秒）更新一次

        wx.StaticText(self, label=info, pos=(20, 24), size=(300, -1))
        self.submit_btn = wx.Button(self, label="结束计时", pos=(135, 110))
        self.Bind(wx.EVT_BUTTON, self.OnClick, self.submit_btn)
        self.Bind(wx.EVT_CHAR_HOOK, self.OnChar)

        # 图标
        D.button_icon(self, "日程安排.png")

        self.Center()
    def update_elapsed_time(self, event):
        current_time = time.time()
        elapsed_time = current_time - self.start_time
        formatted_time = T.time_s2(elapsed_time)
        self.elapsed_time_label.SetLabel(f"计时中：{formatted_time}")

    def OnClick(self, event):
        self.timer.Stop()
        self.end_time = time.time()  # 记录结束时间
        TF.setlog(self.proj, self.begin_t)
        elapsed_time = self.end_time - self.start_time
        s = "您此次花费的的时间为: " + T.time_s2(elapsed_time)
        C.change_3(file_path, self.proj, elapsed_time)
        dlg = D.ResDialog(None, 2, s)
        self.Close()
        dlg.ShowModal()
        dlg.Destroy()

    def OnChar(self, event):
        keycode = event.GetKeyCode()
        if keycode == wx.WXK_RETURN or keycode == wx.WXK_NUMPAD_ENTER:
            self.OnClick(event)
        else:
            event.Skip()


class App(wx.App):
    def __init__(self):
        super(self.__class__, self).__init__()


    def OnInit(self):
        self.flag = FLAG
        self.version = V.version_control(Version_Path, self.flag)
        self.title = "计时工具 v." + self.version
        self.frame = MainFrame(None, -1, self.title)
        self.frame.Show(True)

        return True


FLAG = False
app = App()
app.MainLoop()
