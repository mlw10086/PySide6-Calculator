#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
主窗口类 - 计算器的主界面
实现标签页切换和整体布局管理
"""

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QTabWidget, 
    QMenuBar, QStatusBar, QApplication
)
from PySide6.QtCore import Qt, Signal, Slot
from PySide6.QtGui import QKeySequence, QAction

from .display_widget import DisplayWidget
from .standard_panel import StandardPanel
from .scientific_panel import ScientificPanel
from .programmer_panel import ProgrammerPanel
from .history_dialog import HistoryDialog
from core.calculator_engine import CalculatorEngine
from styles.style_manager import StyleManager


class MainWindow(QMainWindow):
    """主窗口类"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("多功能计算器 - Claude 4.0 sonnet")
        # 设置更合理的最小尺寸，确保按钮不会挤压
        self.setMinimumSize(500, 700)
        self.resize(550, 750)
        
        # 初始化核心组件
        self.calculator_engine = CalculatorEngine()
        self.style_manager = StyleManager()
        
        # 设置窗口属性
        self.setWindowFlags(Qt.Window | Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint)
        
        # 初始化UI
        self.init_ui()
        self.init_menu()
        self.init_status_bar()
        self.apply_styles()
        self.connect_signals()
        
    def init_ui(self):
        """初始化用户界面"""
        # 创建中央窗口部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建主布局
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        
        # 创建显示屏
        self.display = DisplayWidget()
        main_layout.addWidget(self.display)
        
        # 创建标签页控件
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabPosition(QTabWidget.North)
        main_layout.addWidget(self.tab_widget)
        
        # 创建各模式面板
        self.standard_panel = StandardPanel()
        self.scientific_panel = ScientificPanel()
        self.programmer_panel = ProgrammerPanel()
        
        # 添加标签页
        self.tab_widget.addTab(self.standard_panel, "标准")
        self.tab_widget.addTab(self.scientific_panel, "科学")
        self.tab_widget.addTab(self.programmer_panel, "程序员")
        
        # 设置默认标签页
        self.tab_widget.setCurrentIndex(0)
        
    def init_menu(self):
        """初始化菜单栏"""
        menubar = self.menuBar()
        
        # 查看菜单
        view_menu = menubar.addMenu("查看(&V)")
        
        # 标准模式
        standard_action = QAction("标准(&S)", self)
        standard_action.setShortcut(QKeySequence("Alt+1"))
        standard_action.triggered.connect(lambda: self.tab_widget.setCurrentIndex(0))
        view_menu.addAction(standard_action)
        
        # 科学模式
        scientific_action = QAction("科学(&C)", self)
        scientific_action.setShortcut(QKeySequence("Alt+2"))
        scientific_action.triggered.connect(lambda: self.tab_widget.setCurrentIndex(1))
        view_menu.addAction(scientific_action)
        
        # 程序员模式
        programmer_action = QAction("程序员(&P)", self)
        programmer_action.setShortcut(QKeySequence("Alt+3"))
        programmer_action.triggered.connect(lambda: self.tab_widget.setCurrentIndex(2))
        view_menu.addAction(programmer_action)
        
        view_menu.addSeparator()
        
        # 历史记录
        history_action = QAction("历史记录(&R)", self)
        history_action.setShortcut(QKeySequence("Ctrl+H"))
        history_action.triggered.connect(self.show_history)
        view_menu.addAction(history_action)

        # 帮助菜单
        help_menu = menubar.addMenu("帮助(&H)")
        
        about_action = QAction("关于(&A)", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
        
    def init_status_bar(self):
        """初始化状态栏"""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("就绪", 2000)
        
    def apply_styles(self):
        """应用样式"""
        self.setStyleSheet(self.style_manager.get_main_window_style())
        
    def connect_signals(self):
        """连接信号槽"""
        # 连接计算引擎信号
        self.calculator_engine.result_ready.connect(self.display.set_result)
        self.calculator_engine.error_occurred.connect(self.display.set_error)
        
        # 连接面板信号
        self.standard_panel.button_clicked.connect(self.handle_button_click)
        self.scientific_panel.button_clicked.connect(self.handle_button_click)
        self.programmer_panel.button_clicked.connect(self.handle_button_click)
        
        # 连接显示屏信号
        self.display.expression_changed.connect(self.calculator_engine.set_expression)
        
    @Slot(str)
    def handle_button_click(self, button_text):
        """处理按钮点击事件"""
        self.status_bar.showMessage(f"按下: {button_text}", 1000)

        # 根据按钮类型处理
        if button_text == "=":
            self.calculator_engine.calculate()
        elif button_text == "C":
            self.display.clear()
            self.calculator_engine.clear()
        elif button_text == "CE":
            self.display.clear_entry()
        elif button_text == "⌫":
            self.display.backspace()
        elif button_text == "MC":
            self.calculator_engine.memory_clear()
        elif button_text == "MR":
            self.calculator_engine.memory_recall()
        elif button_text == "MS":
            self.calculator_engine.memory_store()
        elif button_text == "M+":
            self.calculator_engine.memory_add()
        elif button_text == "M-":
            self.calculator_engine.memory_subtract()
        elif button_text in ["√x", "x²", "1/x", "%", "±"]:
            self.handle_function_button(button_text)
        elif button_text in ["sin", "cos", "tan", "asin", "acos", "atan",
                            "sinh", "cosh", "tanh", "log", "ln", "exp",
                            "x³", "xʸ", "10ˣ", "eˣ", "∛x", "ʸ√x", "n!", "π", "e"]:
            self.handle_scientific_function(button_text)
        elif button_text in ["HEX", "DEC", "OCT", "BIN"]:
            self.handle_base_change(button_text)
        elif button_text in ["AND", "OR", "XOR", "NOT", "LSH", "RSH"]:
            self.handle_bitwise_operation(button_text)
        elif button_text in ["A", "B", "C", "D", "E", "F"]:
            # 十六进制字母按钮处理
            current_base = self.get_current_base()
            if current_base == 16:
                self.display.append_text(button_text)
            else:
                # 如果不是十六进制模式，提示用户切换到十六进制
                self.status_bar.showMessage(f"请先切换到十六进制模式才能使用 {button_text}", 2000)
        elif button_text in ["8", "9"]:
            # 数字8、9的进制检查
            current_base = self.get_current_base()
            if current_base >= 10:  # 十进制或十六进制
                self.display.append_text(button_text)
            else:
                self.status_bar.showMessage(f"当前进制不支持数字 {button_text}", 2000)
        elif button_text in ["2", "3", "4", "5", "6", "7"]:
            # 数字2-7的进制检查
            current_base = self.get_current_base()
            if current_base >= 8:  # 八进制、十进制或十六进制
                self.display.append_text(button_text)
            else:
                self.status_bar.showMessage(f"当前进制不支持数字 {button_text}", 2000)
        else:
            self.display.append_text(button_text)

    def handle_function_button(self, function):
        """处理功能按钮"""
        current_text = self.display.get_current_expression()
        if not current_text or current_text == "0":
            return

        if function == "√x":
            self.display.append_text("√(")
        elif function == "x²":
            self.display.append_text("²")
        elif function == "1/x":
            self.display.set_expression(f"1/({current_text})")
            self.calculator_engine.calculate()
        elif function == "%":
            self.display.append_text("%")
        elif function == "±":
            if current_text.startswith("-"):
                self.display.set_expression(current_text[1:])
            else:
                self.display.set_expression("-" + current_text)

    def handle_scientific_function(self, function):
        """处理科学计算函数"""
        current_text = self.display.get_current_expression()

        if function in ["π", "e"]:
            # 常数直接添加
            self.display.append_text(function)
        elif function in ["sin", "cos", "tan", "asin", "acos", "atan",
                         "sinh", "cosh", "tanh", "log", "ln", "exp"]:
            # 函数需要括号
            self.display.append_text(f"{function}(")
        elif function == "x³":
            self.display.append_text("³")
        elif function == "n!":
            if current_text and current_text != "0":
                self.display.append_text("!")
        elif function == "10ˣ":
            self.display.append_text("10^(")
        elif function == "eˣ":
            self.display.append_text("exp(")
        elif function == "∛x":
            self.display.append_text("∛(")
        elif function == "xʸ":
            self.display.append_text("^")
        elif function == "ʸ√x":
            self.display.append_text("√(")

    def handle_base_change(self, base_name):
        """处理进制切换"""
        current_value = self.display.get_current_expression()
        if not current_value or current_value == "0":
            return

        # 获取当前进制
        current_base = self.get_current_base()

        # 确定目标进制
        target_base = {"HEX": 16, "DEC": 10, "OCT": 8, "BIN": 2}[base_name]

        # 转换数值
        converted = self.calculator_engine.convert_to_base(current_value, target_base)
        self.display.set_expression(converted)

        # 更新程序员面板的进制模式
        if hasattr(self.programmer_panel, 'set_base_mode'):
            self.programmer_panel.set_base_mode(target_base)

    def handle_bitwise_operation(self, operation):
        """处理位运算"""
        current_text = self.display.get_current_expression()
        if operation == "NOT":
            # NOT是一元运算符
            if current_text and current_text != "0":
                result = self.calculator_engine.bitwise_operation(current_text, 0, operation)
                self.display.set_expression(str(result))
        else:
            # 其他是二元运算符
            self.display.append_text(f" {operation} ")

    def get_current_base(self):
        """获取当前进制"""
        if hasattr(self.programmer_panel, 'get_current_base'):
            return self.programmer_panel.get_current_base()
        return 10

    @Slot()
    def show_history(self):
        """显示历史记录"""
        try:
            dialog = HistoryDialog(self.calculator_engine.history_manager, self)
            dialog.expression_selected.connect(self.use_history_expression)
            dialog.exec()
        except Exception as e:
            print(f"显示历史记录时出错: {e}")
            import traceback
            traceback.print_exc()

    @Slot(str)
    def use_history_expression(self, expression):
        """使用历史记录中的表达式"""
        self.display.set_expression(expression)
        
    @Slot()
    def show_about(self):
        """显示关于对话框"""
        from PySide6.QtWidgets import QMessageBox
        QMessageBox.about(
            self, 
            "关于多功能计算器",
            "多功能计算器 v1.0.0\n\n"
            "作者：Claude 4.0 sonnet\n"
            "基于 PySide6 开发\n\n"
            "支持标准、科学和程序员三种计算模式\n"
            "界面设计符合中国用户使用习惯"
        )
        
    def keyPressEvent(self, event):
        """处理键盘事件"""
        key = event.key()
        text = event.text()
        
        # 数字键
        if key >= Qt.Key_0 and key <= Qt.Key_9:
            self.handle_button_click(text)
        # 运算符键
        elif key == Qt.Key_Plus:
            self.handle_button_click("+")
        elif key == Qt.Key_Minus:
            self.handle_button_click("-")
        elif key == Qt.Key_Asterisk:
            self.handle_button_click("×")
        elif key == Qt.Key_Slash:
            self.handle_button_click("÷")
        elif key == Qt.Key_Period:
            self.handle_button_click(".")
        elif key == Qt.Key_Enter or key == Qt.Key_Return:
            self.handle_button_click("=")
        elif key == Qt.Key_Escape:
            self.handle_button_click("C")
        elif key == Qt.Key_Backspace:
            self.handle_button_click("⌫")
        else:
            super().keyPressEvent(event)

    def resizeEvent(self, event):
        """处理窗口大小改变事件"""
        super().resizeEvent(event)

        # 根据窗口大小动态调整字体
        width = self.width()
        height = self.height()

        # 计算合适的字体大小
        if width < 550 or height < 750:
            font_size = 11
        elif width < 650 or height < 850:
            font_size = 12
        else:
            font_size = 13

        # 更新按钮字体大小
        self.update_button_font_size(font_size)

    def update_button_font_size(self, font_size):
        """更新所有按钮的字体大小"""
        style_template = """
            QPushButton {{
                font-size: {font_size}px;
            }}
        """

        # 应用新的字体大小样式
        additional_style = style_template.format(font_size=font_size)
        current_style = self.styleSheet()

        # 移除旧的字体大小设置，添加新的
        import re
        current_style = re.sub(r'QPushButton\s*\{\s*font-size:\s*\d+px;\s*\}', '', current_style)
        self.setStyleSheet(current_style + additional_style)
