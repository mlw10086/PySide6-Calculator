#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
显示屏组件 - 计算器的显示区域
支持表达式显示、结果显示和历史记录
"""

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QLabel
from PySide6.QtCore import Qt, Signal, Slot
from PySide6.QtGui import QFont, QPalette


class DisplayWidget(QWidget):
    """显示屏组件"""
    
    # 信号定义
    expression_changed = Signal(str)  # 表达式改变信号
    
    def __init__(self):
        super().__init__()
        self.current_expression = ""
        self.init_ui()
        self.apply_styles()
        
    def init_ui(self):
        """初始化用户界面"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(2)
        
        # 历史表达式显示（小字体，灰色）
        self.history_label = QLabel()
        self.history_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.history_label.setMinimumHeight(25)
        self.history_label.setWordWrap(True)
        layout.addWidget(self.history_label)
        
        # 当前表达式显示
        self.expression_edit = QLineEdit()
        self.expression_edit.setAlignment(Qt.AlignRight)
        self.expression_edit.setReadOnly(True)
        self.expression_edit.setMinimumHeight(40)
        self.expression_edit.setText("0")
        layout.addWidget(self.expression_edit)
        
        # 结果显示（大字体）
        self.result_label = QLabel("0")
        self.result_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.result_label.setMinimumHeight(60)
        self.result_label.setWordWrap(True)
        layout.addWidget(self.result_label)
        
    def apply_styles(self):
        """应用样式"""
        # 历史记录样式
        self.history_label.setStyleSheet("""
            QLabel {
                color: #888888;
                font-size: 12px;
                background: transparent;
                border: none;
                padding: 2px 8px;
            }
        """)
        
        # 表达式输入框样式
        self.expression_edit.setStyleSheet("""
            QLineEdit {
                background-color: #FFFFFF;
                border: 1px solid #CCCCCC;
                border-radius: 4px;
                padding: 8px 12px;
                font-size: 16px;
                color: #333333;
                selection-background-color: #4A90E2;
            }
            QLineEdit:focus {
                border-color: #4A90E2;
            }
        """)
        
        # 结果显示样式
        self.result_label.setStyleSheet("""
            QLabel {
                background-color: #F8F9FA;
                border: 1px solid #E9ECEF;
                border-radius: 4px;
                padding: 12px;
                font-size: 24px;
                font-weight: bold;
                color: #2C3E50;
            }
        """)
        
    def append_text(self, text):
        """添加文本到表达式"""
        current = self.expression_edit.text()

        # 输入验证
        if not self.validate_input(current, text):
            return

        # 如果当前显示的是"0"或错误信息，则替换
        if current == "0" or current.startswith("错误"):
            if text in "0123456789.":
                self.expression_edit.setText(text)
            else:
                self.expression_edit.setText("0" + text)
        else:
            self.expression_edit.setText(current + text)

        self.current_expression = self.expression_edit.text()
        self.expression_changed.emit(self.current_expression)

    def validate_input(self, current, new_text):
        """验证输入是否合法"""
        # 防止连续的运算符
        if new_text in "+-×÷" and current.endswith(("+-×÷", " ")):
            return False

        # 防止多个小数点
        if new_text == "." and "." in current.split()[-1]:
            return False

        # 防止表达式过长
        if len(current) > 100:
            return False

        return True
        
    def clear(self):
        """清除所有内容"""
        self.expression_edit.setText("0")
        self.result_label.setText("0")
        self.history_label.setText("")
        self.current_expression = ""
        self.expression_changed.emit("")
        
    def clear_entry(self):
        """清除当前输入"""
        self.expression_edit.setText("0")
        self.current_expression = ""
        self.expression_changed.emit("")
        
    def backspace(self):
        """退格删除"""
        current = self.expression_edit.text()
        if len(current) > 1:
            new_text = current[:-1]
            self.expression_edit.setText(new_text)
        else:
            self.expression_edit.setText("0")
            
        self.current_expression = self.expression_edit.text()
        self.expression_changed.emit(self.current_expression)
        
    @Slot(str)
    def set_result(self, result):
        """设置计算结果"""
        # 保存历史记录
        if self.current_expression and self.current_expression != "0":
            history_text = f"{self.current_expression} ="
            self.history_label.setText(history_text)
            
        # 显示结果
        self.result_label.setText(str(result))
        self.expression_edit.setText(str(result))
        self.current_expression = str(result)
        
    @Slot(str)
    def set_error(self, error_msg):
        """设置错误信息"""
        self.result_label.setText(f"错误: {error_msg}")
        self.expression_edit.setText("0")
        self.current_expression = ""
        
        # 错误时使用红色显示
        self.result_label.setStyleSheet("""
            QLabel {
                background-color: #FFF5F5;
                border: 1px solid #FEB2B2;
                border-radius: 4px;
                padding: 12px;
                font-size: 18px;
                font-weight: bold;
                color: #E53E3E;
            }
        """)
        
        # 2秒后恢复正常样式
        from PySide6.QtCore import QTimer
        QTimer.singleShot(2000, self.restore_normal_style)
        
    def restore_normal_style(self):
        """恢复正常样式"""
        self.result_label.setStyleSheet("""
            QLabel {
                background-color: #F8F9FA;
                border: 1px solid #E9ECEF;
                border-radius: 4px;
                padding: 12px;
                font-size: 24px;
                font-weight: bold;
                color: #2C3E50;
            }
        """)
        
    def get_current_expression(self):
        """获取当前表达式"""
        return self.current_expression
        
    def get_current_result(self):
        """获取当前结果"""
        return self.result_label.text()

    def set_expression(self, expression):
        """设置表达式"""
        self.expression_edit.setText(expression)
        self.current_expression = expression
        self.expression_changed.emit(expression)
