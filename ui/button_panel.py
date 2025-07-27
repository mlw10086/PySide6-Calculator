#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
按钮面板基类 - 所有计算器面板的基础类
提供通用的按钮创建和布局功能
"""

from PySide6.QtWidgets import QWidget, QGridLayout, QPushButton, QSizePolicy
from PySide6.QtCore import Qt, Signal, Slot
from PySide6.QtGui import QFont


class ButtonPanel(QWidget):
    """按钮面板基类"""
    
    # 信号定义
    button_clicked = Signal(str)  # 按钮点击信号
    
    def __init__(self):
        super().__init__()
        self.buttons = {}  # 存储按钮引用
        self.init_ui()
        
    def init_ui(self):
        """初始化用户界面 - 子类需要重写"""
        self.layout = QGridLayout(self)
        self.layout.setContentsMargins(8, 8, 8, 8)
        self.layout.setSpacing(6)
        
    def create_button(self, text, row, col, row_span=1, col_span=1, button_type="normal"):
        """
        创建按钮
        
        Args:
            text: 按钮文本
            row: 行位置
            col: 列位置
            row_span: 行跨度
            col_span: 列跨度
            button_type: 按钮类型 ("normal", "operator", "function", "special")
        """
        button = QPushButton(text)
        # 设置更合理的按钮尺寸，确保文字显示完整
        button.setMinimumSize(70, 55)
        button.setMaximumSize(150, 70)
        # 设置尺寸策略，允许按钮适应布局
        button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # 设置按钮类型属性（用于QSS选择器）
        button.setProperty("buttonType", button_type)

        # 设置按钮样式
        self.apply_button_style(button, button_type)
        
        # 设置工具提示
        self.set_button_tooltip(button, text, button_type)

        # 连接信号
        button.clicked.connect(lambda: self.on_button_clicked(text))

        # 添加到布局
        self.layout.addWidget(button, row, col, row_span, col_span)

        # 存储按钮引用
        self.buttons[text] = button

        return button

    def set_button_tooltip(self, button, text, button_type):
        """设置按钮工具提示"""
        tooltip_map = {
            # 数字和基本运算
            "0": "数字 0",
            "1": "数字 1", "2": "数字 2", "3": "数字 3",
            "4": "数字 4", "5": "数字 5", "6": "数字 6",
            "7": "数字 7", "8": "数字 8", "9": "数字 9",
            ".": "小数点",
            "+": "加法", "-": "减法", "×": "乘法", "÷": "除法",
            "=": "计算结果",

            # 功能键
            "C": "全部清除", "CE": "清除输入", "⌫": "退格删除",
            "±": "正负号切换", "%": "百分比",

            # 内存功能
            "MC": "内存清除", "MR": "内存读取", "MS": "内存存储",
            "M+": "内存加法", "M-": "内存减法",

            # 数学函数
            "√x": "平方根", "x²": "平方", "x³": "立方", "1/x": "倒数",
            "π": "圆周率", "e": "自然常数",

            # 三角函数
            "sin": "正弦", "cos": "余弦", "tan": "正切",
            "asin": "反正弦", "acos": "反余弦", "atan": "反正切",

            # 对数函数
            "log": "常用对数", "ln": "自然对数", "exp": "指数函数",

            # 进制
            "HEX": "十六进制", "DEC": "十进制", "OCT": "八进制", "BIN": "二进制",

            # 位运算
            "AND": "按位与", "OR": "按位或", "XOR": "按位异或",
            "NOT": "按位非", "LSH": "左移", "RSH": "右移",
        }

        tooltip = tooltip_map.get(text, text)
        button.setToolTip(tooltip)
        
    def apply_button_style(self, button, button_type):
        """应用按钮样式"""
        base_style = """
            QPushButton {
                border: 1px solid #CCCCCC;
                border-radius: 6px;
                font-size: 14px;
                font-weight: bold;
                padding: 8px;
                margin: 1px;
            }
            QPushButton:hover {
                border-color: #4A90E2;
                background-color: #F0F8FF;
            }
            QPushButton:pressed {
                background-color: #E6F3FF;
                border-color: #2E86AB;
            }
        """
        
        if button_type == "normal":
            # 普通数字按钮 - 白色背景
            style = base_style + """
                QPushButton {
                    background-color: #FFFFFF;
                    color: #333333;
                }
            """
        elif button_type == "operator":
            # 运算符按钮 - 蓝色背景
            style = base_style + """
                QPushButton {
                    background-color: #4A90E2;
                    color: #FFFFFF;
                    border-color: #357ABD;
                }
                QPushButton:hover {
                    background-color: #357ABD;
                }
                QPushButton:pressed {
                    background-color: #2E86AB;
                }
            """
        elif button_type == "function":
            # 功能按钮 - 浅灰色背景
            style = base_style + """
                QPushButton {
                    background-color: #F8F9FA;
                    color: #495057;
                    border-color: #DEE2E6;
                }
                QPushButton:hover {
                    background-color: #E9ECEF;
                }
            """
        elif button_type == "special":
            # 特殊按钮 - 橙色背景
            style = base_style + """
                QPushButton {
                    background-color: #FF8C00;
                    color: #FFFFFF;
                    border-color: #FF7F00;
                }
                QPushButton:hover {
                    background-color: #FF7F00;
                }
                QPushButton:pressed {
                    background-color: #FF6347;
                }
            """
        else:
            style = base_style + """
                QPushButton {
                    background-color: #FFFFFF;
                    color: #333333;
                }
            """
            
        button.setStyleSheet(style)
        
    @Slot()
    def on_button_clicked(self, text):
        """按钮点击处理"""
        self.button_clicked.emit(text)
        
    def get_button(self, text):
        """获取按钮引用"""
        return self.buttons.get(text)
        
    def enable_button(self, text, enabled=True):
        """启用/禁用按钮"""
        button = self.get_button(text)
        if button:
            button.setEnabled(enabled)
            
    def set_button_text(self, old_text, new_text):
        """修改按钮文本"""
        button = self.get_button(old_text)
        if button:
            button.setText(new_text)
            # 更新字典键
            self.buttons[new_text] = self.buttons.pop(old_text)
            
    def highlight_button(self, text, highlight=True):
        """高亮显示按钮"""
        button = self.get_button(text)
        if button:
            if highlight:
                button.setStyleSheet(button.styleSheet() + """
                    QPushButton {
                        border: 2px solid #FF6B6B;
                        background-color: #FFE5E5;
                    }
                """)
            else:
                # 恢复原始样式 - 这里简化处理，实际应该保存原始样式
                self.apply_button_style(button, "normal")
                
    def clear_highlights(self):
        """清除所有按钮高亮"""
        for text, button in self.buttons.items():
            self.apply_button_style(button, "normal")
