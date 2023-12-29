import wx
import os
import time

from utils import csv_fun as C
from utils import timefun as T
from utils import txtfun as TF
from utils.fpath import *


def show_exit_projs(self):
    s = C.show_pros(file_path)
    text = wx.StaticText(self, label=s, pos=(20, 60))
    text.Wrap(300)  # 设置最大宽度为 200 像素，超过宽度将自动换行


def button_icon(self, pic):
    img_path = os.path.join(pic_path, pic)
    icon = wx.Icon(img_path, type=wx.BITMAP_TYPE_PNG)
    self.SetIcon(icon)


class AddDialog(wx.Dialog):
    """添加项目对话框"""
    def __init__(self, parent, id):
        super(AddDialog, self).__init__(parent, id, "添加项目记录", size=(350, 250))
        self.app = wx.GetApp()
        self.panel = self.app.frame

        wx.StaticText(self, label="添加的项目名称：", pos=(20, 24))
        self.proj = wx.TextCtrl(self, pos=(118, 20), size=(50, 26))
        wx.StaticText(self, label="时间：", pos=(175, 24))
        self.pro_t = wx.TextCtrl(self, pos=(212, 20), size=(50, 26))
        wx.StaticText(self, label="H", pos=(268, 24))

        # 显示文本
        show_exit_projs(self)

        self.submit_btn = wx.Button(self, label="提交", pos=(135, 140))
        self.Bind(wx.EVT_BUTTON, self.OnClick, self.submit_btn)
        self.Bind(wx.EVT_CHAR_HOOK, self.OnChar)

        # 图标
        button_icon(self, "Targets.png")

        self.Center()

    def OnClick(self, event):
        proj = self.proj.GetValue()
        t = self.pro_t.GetValue()
        C.add_1(file_path, proj, t)
        dlg = ShowDialog(None, -1)
        self.Close()
        dlg.ShowModal()
        dlg.Destroy()


    def OnChar(self, event):
        keycode = event.GetKeyCode()
        if keycode == wx.WXK_RETURN or keycode == wx.WXK_NUMPAD_ENTER:
            if self.pro_t.GetValue() is not None:
                self.OnClick(event)
        else:
            event.Skip()


class ShowDialog(wx.Dialog):
    def __init__(self, parent, id):
        super(ShowDialog, self).__init__(parent, id, "历史时间记录", size=(350, 500))
        self.app = wx.GetApp()
        self.panel = self.app.frame

        # 图标
        button_icon(self, "show.png")

        self.Center()
        info = C.show_info(file_path)
        wx.StaticText(self, label=info, pos=(40, 20), size=(300, -1))
        wx.Button(self, wx.ID_OK, pos=(135, 400))


class RecDialog(wx.Dialog):
    """显示当日记录对话框"""
    def __init__(self, parent, id):
        super(RecDialog, self).__init__(parent, id, "当日记录", size=(350, 500))
        self.app = wx.GetApp()
        self.panel = self.app.frame

        # 图标
        button_icon(self, "饭团.png")

        self.Center()
        info = TF.readlog()
        wx.StaticText(self, label=info, pos=(40, 20), size=(300, -1))
        wx.Button(self, wx.ID_OK, pos=(135, 400))


class DayDialog(wx.Dialog):
    """添加日常记录对话框"""
    def __init__(self, parent, id):
        super(DayDialog, self).__init__(parent, id, "开始日常", size=(350, 250))
        self.app = wx.GetApp()
        self.panel = self.app.frame
        wx.StaticText(self, label="所要进行的活动名称", pos=(20, 24))

        self.proj = wx.TextCtrl(self, pos=(145, 20))
        self.submit_btn = wx.Button(self, label="开始计时", pos=(135, 140))
        self.Bind(wx.EVT_BUTTON, self.OnClick, self.submit_btn)
        self.Bind(wx.EVT_CHAR_HOOK, self.OnChar)

        # 图标
        button_icon(self, "我的流程.png")

        self.Center()
    def OnClick(self, event):
        proj = self.proj.GetValue()
        info = C.change_info(file_path, proj)
        dlg = DtimDialog(None, 1, info, proj)
        self.Close()
        dlg.ShowModal()
        dlg.Destroy()

    def OnChar(self, event):
        keycode = event.GetKeyCode()
        if keycode == wx.WXK_RETURN or keycode == wx.WXK_NUMPAD_ENTER:
            self.OnClick(event)
        else:
            event.Skip()


class DtimDialog(wx.Dialog):
    """日程记录计时对话框"""
    def __init__(self, parent, id, info, proj):
        super(DtimDialog, self).__init__(parent, id, "计时开始", size=(350, 200))
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
        button_icon(self, "日程安排.png")

        self.Center()

    def update_elapsed_time(self, event):
        current_time = time.time()
        elapsed_time = current_time - self.start_time
        formatted_time = T.time_s2(elapsed_time)
        self.elapsed_time_label.SetLabel(f"计时中：{formatted_time}")

    def OnClick(self, event):
        self.timer.Stop()
        self.end_time = time.time()  # 记录结束时间
        TF.setlog(self.proj, self.begin_t)  # 记录至日常记录中

        elapsed_time = self.end_time - self.start_time
        s = "您此次花费的的时间为: " + T.time_s2(elapsed_time)
        dlg = ResDialog(None, 2, s)
        self.Close()
        dlg.ShowModal()
        dlg.Destroy()

    def OnChar(self, event):
        keycode = event.GetKeyCode()
        if keycode == wx.WXK_RETURN or keycode == wx.WXK_NUMPAD_ENTER:
            self.OnClick(event)
        else:
            event.Skip()


class ResDialog(wx.Dialog):
    """生成时间记录显示"""
    def __init__(self, parent, id, info):
        super(ResDialog, self).__init__(parent, id, "时间记录", size=(350, 200))
        self.app = wx.GetApp()
        self.panel = self.app.frame
        wx.StaticText(self, label=info, pos=(20, 20), size=(300, -1))
        wx.Button(self, wx.ID_OK, pos=(135, 100))
        # 图标
        button_icon(self, "生成报告.png")
        self.Center()
