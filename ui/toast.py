import threading

from PySide2 import QtWidgets, QtGui, QtCore


class Toast(QtWidgets.QWidget):
    """
    仿 Android 的 Toast
    直接Copy https://blog.csdn.net/weixin_44295684/article/details/105412596 代码进行修改。
    """
    background_color_dark = QtGui.QColor("#1D1D1D")  # 设置背景色
    text_color_dark = QtGui.QColor("#D3D3D3")        # 设置字体颜色
    background_color = QtGui.QColor("#FFFFFF")  # 设置背景色
    text_color = QtGui.QColor("#7F7F7F")        # 设置字体颜色
    font = QtGui.QFont('Microsoft YaHei', 10)    # 设置字体字体大小，
    text = ''
    times = 3
    parent = None
    min_height = 10
    min_width = 10
    pos = QtCore.QPointF(0, 0)

    def __init__(self, parent=None, ):
        super(Toast, self).__init__(parent)
        self.parent = parent
        self.dark_mode = False
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

    def init_UI(self):
        # 计算气泡长宽及移动气泡到指定位置
        self.height = self.get_font_size() * 2
        self.width = len(self.text) * self.height * 0.8
        if self.height < self.min_height:
            self.height = self.min_height
        # else:
        #     self.height = self.min_height * 2
        if self.width < self.min_width:
            self.width = self.min_width
        self.resize(self.width, self.height)
        if self.pos.x() != 0 or self.pos.y() != 0:
            self.move(self.pos.x() - self.width / 2, self.pos.y() - self.height / 2)

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setRenderHints(QtGui.QPainter.Antialiasing | QtGui.QPainter.TextAntialiasing)
        rect_line_path = QtGui.QPainterPath()
        rectangle = QtCore.QRectF(0, 0, self.width, self.height)
        rect_line_path.addRoundedRect(rectangle, self.height / 2, self.height / 2, QtCore.Qt.AbsoluteSize)
        if self.dark_mode:
            painter.fillPath(rect_line_path, QtGui.QColor(self.background_color_dark))
            pen = QtGui.QPen(QtGui.QColor(self.text_color_dark))
        else:
            painter.fillPath(rect_line_path, QtGui.QColor(self.background_color))
            pen = QtGui.QPen(QtGui.QColor(self.text_color))
        painter.setPen(pen)
        painter.setFont(self.font)
        self.draw_text(painter)

    def get_font_size(self):
        return self.font.pointSizeF()

    def draw_text(self, painter):
        painter.drawText(QtCore.QRectF(0, 0, self.width, self.height),
                         QtCore.Qt.AlignCenter, self.text)

    def make_text(self, text, left_pos, top_pos,  times=None, dark_mode=False):
        if 0 == left_pos and self.parent:
            left_pos = self.parent.geometry().x() + self.parent.size().width() / 2
        if 0 == top_pos and self.parent:
            top_pos = self.parent.geometry().y() + self.parent.size().height() / 2
        pos = QtCore.QPointF(left_pos, top_pos)
        if pos:
            self.pos = pos
        if text:
            self.text = text
        if times:
            self.times = times
        self.dark_mode = dark_mode
        self.init_UI()
        self.repaint()
        self.show()

        toast_timer = threading.Timer(self.times, self.toast_timeout)
        toast_timer.start()

    def toast_timeout(self):
        self.close()