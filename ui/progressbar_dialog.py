# # -*- coding:utf-8 -*-


# from time import sleep
# import time
# from PySide2.QtCore import Qt
# from ui.base_dialog import BaseDialog
# from utils.work_thread import SUCCESS, WorkThread


# class ProgressBarDialog(BaseDialog):
#     """

#     @author: purejiang
#     @created: 2022/7/12

#     通用的进度条弹出框

#     """
#     __UI_FILE = "./res/ui/progressbar_dialog.ui"
#     __QSS_FILE = "./res/qss/progressbar_dialog.qss"
    
#     # _signal = Signal(str)

#     def __init__(self, main_window, title, run_func, end_func, close_func, is_auto_close=False, min_value=0, max_value=100):
#         self.__title = title
#         self.__run_func = run_func
#         self.__end_func = end_func
#         self.__close_func = close_func
#         self.__min_value = min_value
#         self.__max_value = max_value
#         self.__is_auto_close = is_auto_close
#         self.__thread = WorkThread(self.__run_func)
#         self.__thread._state.connect(self.__sig_out)
#         super(ProgressBarDialog, self).__init__(main_window)
#         self.init()

#     def init(self):
#         self.__start_loader()

#     def _on_pre_show(self):
#         self._loadUi(self.__UI_FILE)
#         self._ui.progressbar_title_label.setText(self.__title)
#         self._ui.progress_bar.setMinimum(self.__min_value)
#         self._ui.progress_bar.setMaximum(self.__max_value)
#         self._ui.progress_bar.setVisible(True)
#         self._ui.progress_confirm_btn.setVisible(False)
        

#     def _setup_qss(self):
#         # 禁止其他界面响应
#         self.setWindowModality(Qt.ApplicationModal)
#         self.setWindowFlags(Qt.FramelessWindowHint)
#         self._loadQss(self.__QSS_FILE)

#     def _setup_listener(self):
#         self._ui.progress_confirm_btn.clicked.connect(self.__close)

#     def keyPressEvent(self, e):
#         # 键盘事件
#         # if e.key() == Qt.Key_Escape:
#         #     self.close()
#         pass

#     def __close(self):
#         print("close")
#         self.close()
#         if self.__close_func:
#             time.sleep(3)
#             self.__close_func()

#     def progress_callback(self, progress=None, msg=None):
#         if progress:
#             self.__set_progress(progress)
#         if msg:
#             self.__set_msg(msg)

#     def __set_progress(self, value):
#         print("progress_bar.setvalue:"+str(value))
#         self._ui.progress_bar.setValue(value)
    
#     def __set_msg(self, msg):
#         print("progress_bar.setText:"+str(msg))
#         self._ui.progressbar_message_label.setText(msg)

#     def __start_loader(self):
#         self.__thread.start()

#     def __sig_out(self, state):
#         if state==SUCCESS:
#             if self._ui.progress_bar.value() < 100:
#                 self.__set_progress(100)
#             self.__end_func()
#             print("SUCCESS")
#             if self.__is_auto_close:   
#                 print("__close")
#                 time.sleep(3)  
#                 self.__close()
#             else:
#                 print("setVisible")
#                 self._ui.progress_bar.setVisible(False)
#                 self._ui.progress_confirm_btn.setVisible(True)
#             print("terminate")
#             self.__thread.terminate()
            

            
            