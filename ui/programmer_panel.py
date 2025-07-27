#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
程序员模式面板 - 程序员计算器功能
包含进制转换、位运算等程序开发相关功能
"""

from .button_panel import ButtonPanel


class ProgrammerPanel(ButtonPanel):
    """程序员计算器面板"""
    
    def __init__(self):
        super().__init__()
        self.current_base = 10  # 当前进制：10进制
        self.create_buttons()
        
    def create_buttons(self):
        """创建程序员模式的所有按钮"""
        
        # 第一行：进制选择
        self.create_button("HEX", 0, 0, button_type="function")  # 十六进制
        self.create_button("DEC", 0, 1, button_type="function")  # 十进制
        self.create_button("OCT", 0, 2, button_type="function")  # 八进制
        self.create_button("BIN", 0, 3, button_type="function")  # 二进制
        self.create_button("QWORD", 0, 4, button_type="function") # 64位
        
        # 第二行：字长选择
        self.create_button("DWORD", 1, 0, button_type="function") # 32位
        self.create_button("WORD", 1, 1, button_type="function")  # 16位
        self.create_button("BYTE", 1, 2, button_type="function")  # 8位
        self.create_button("MS", 1, 3, button_type="function")    # 内存存储
        self.create_button("M+", 1, 4, button_type="function")    # 内存加
        
        # 第三行：十六进制字母和位运算
        self.create_button("A", 2, 0, button_type="normal")      # 十六进制A
        self.create_button("B", 2, 1, button_type="normal")      # 十六进制B
        self.create_button("C", 2, 2, button_type="normal")      # 十六进制C
        self.create_button("D", 2, 3, button_type="normal")      # 十六进制D
        self.create_button("E", 2, 4, button_type="normal")      # 十六进制E
        
        # 第四行：十六进制F和位运算
        self.create_button("F", 3, 0, button_type="normal")      # 十六进制F
        self.create_button("AND", 3, 1, button_type="operator")  # 按位与
        self.create_button("OR", 3, 2, button_type="operator")   # 按位或
        self.create_button("XOR", 3, 3, button_type="operator")  # 按位异或
        self.create_button("NOT", 3, 4, button_type="operator")  # 按位非
        
        # 第五行：位移运算和清除
        self.create_button("LSH", 4, 0, button_type="operator")  # 左移
        self.create_button("RSH", 4, 1, button_type="operator")  # 右移
        self.create_button("CE", 4, 2, button_type="function")   # 清除输入
        self.create_button("C", 4, 3, button_type="function")    # 全部清除
        self.create_button("⌫", 4, 4, button_type="function")    # 退格
        
        # 第六行：数字和运算符
        self.create_button("÷", 5, 0, button_type="operator")    # 除法
        self.create_button("×", 5, 1, button_type="operator")    # 乘法
        self.create_button("-", 5, 2, button_type="operator")    # 减法
        self.create_button("+", 5, 3, button_type="operator")    # 加法
        self.create_button("=", 5, 4, button_type="special")     # 等号
        
        # 第七行：数字9、8、7、6、5
        self.create_button("9", 6, 0, button_type="normal")      # 数字9
        self.create_button("8", 6, 1, button_type="normal")      # 数字8
        self.create_button("7", 6, 2, button_type="normal")      # 数字7
        self.create_button("6", 6, 3, button_type="normal")      # 数字6
        self.create_button("5", 6, 4, button_type="normal")      # 数字5
        
        # 第八行：数字4、3、2、1、0
        self.create_button("4", 7, 0, button_type="normal")      # 数字4
        self.create_button("3", 7, 1, button_type="normal")      # 数字3
        self.create_button("2", 7, 2, button_type="normal")      # 数字2
        self.create_button("1", 7, 3, button_type="normal")      # 数字1
        self.create_button("0", 7, 4, button_type="normal")      # 数字0
        
        # 初始化时设置十六进制模式，这样所有按钮都可用
        self.set_base_mode(16)
        
        # 调整布局比例，确保按钮均匀分布
        for i in range(5):
            self.layout.setColumnStretch(i, 1)
            self.layout.setColumnMinimumWidth(i, 80)
        for i in range(8):
            self.layout.setRowStretch(i, 1)
            self.layout.setRowMinimumHeight(i, 60)
            
    def set_base_mode(self, base):
        """设置进制模式"""
        self.current_base = base
        
        # 重置所有进制按钮样式
        for base_btn in ["HEX", "DEC", "OCT", "BIN"]:
            button = self.get_button(base_btn)
            if button:
                self.apply_button_style(button, "function")
        
        # 高亮当前进制按钮
        if base == 16:
            self.highlight_base_button("HEX")
            self.enable_hex_buttons(True)
        elif base == 10:
            self.highlight_base_button("DEC")
            self.enable_hex_buttons(False)
        elif base == 8:
            self.highlight_base_button("OCT")
            self.enable_hex_buttons(False)
            self.enable_octal_buttons()
        elif base == 2:
            self.highlight_base_button("BIN")
            self.enable_hex_buttons(False)
            self.enable_binary_buttons()
            
    def highlight_base_button(self, base_name):
        """高亮进制按钮"""
        button = self.get_button(base_name)
        if button:
            button.setStyleSheet("""
                QPushButton {
                    background-color: #4A90E2;
                    color: #FFFFFF;
                    border: 2px solid #357ABD;
                    border-radius: 6px;
                    font-size: 14px;
                    font-weight: bold;
                    padding: 8px;
                    margin: 1px;
                }
            """)
            
    def enable_hex_buttons(self, enabled):
        """启用/禁用十六进制字母按钮的视觉效果"""
        hex_buttons = ["A", "B", "C", "D", "E", "F"]
        for btn_text in hex_buttons:
            button = self.get_button(btn_text)
            if button:
                if enabled:
                    # 启用状态 - 正常样式
                    self.apply_button_style(button, "normal")
                else:
                    # 禁用状态 - 灰色样式，但仍然可以点击
                    button.setStyleSheet("""
                        QPushButton {
                            background-color: #F5F5F5;
                            color: #AAAAAA;
                            border: 2px solid #E0E0E0;
                            border-radius: 8px;
                            font-size: 13px;
                            font-weight: bold;
                            padding: 8px 6px;
                            margin: 3px;
                        }
                        QPushButton:hover {
                            background-color: #EEEEEE;
                            border: 3px solid #CCCCCC;
                        }
                    """)
            
    def enable_octal_buttons(self):
        """设置八进制按钮样式（0-7可用，8-9和A-F灰色）"""
        # 设置8、9和十六进制字母为灰色样式
        disabled_buttons = ["8", "9", "A", "B", "C", "D", "E", "F"]
        for btn_text in disabled_buttons:
            button = self.get_button(btn_text)
            if button:
                button.setStyleSheet("""
                    QPushButton {
                        background-color: #F5F5F5;
                        color: #AAAAAA;
                        border: 2px solid #E0E0E0;
                        border-radius: 8px;
                        font-size: 13px;
                        font-weight: bold;
                        padding: 8px 6px;
                        margin: 3px;
                    }
                    QPushButton:hover {
                        background-color: #EEEEEE;
                        border: 3px solid #CCCCCC;
                    }
                """)
        # 设置0-7为正常样式
        enabled_buttons = ["0", "1", "2", "3", "4", "5", "6", "7"]
        for btn_text in enabled_buttons:
            button = self.get_button(btn_text)
            if button:
                self.apply_button_style(button, "normal")
            
    def enable_binary_buttons(self):
        """设置二进制按钮样式（0-1可用，其他灰色）"""
        # 设置2-9和十六进制字母为灰色样式
        disabled_buttons = ["2", "3", "4", "5", "6", "7", "8", "9",
                           "A", "B", "C", "D", "E", "F"]
        for btn_text in disabled_buttons:
            button = self.get_button(btn_text)
            if button:
                button.setStyleSheet("""
                    QPushButton {
                        background-color: #F5F5F5;
                        color: #AAAAAA;
                        border: 2px solid #E0E0E0;
                        border-radius: 8px;
                        font-size: 13px;
                        font-weight: bold;
                        padding: 8px 6px;
                        margin: 3px;
                    }
                    QPushButton:hover {
                        background-color: #EEEEEE;
                        border: 3px solid #CCCCCC;
                    }
                """)
        # 设置0-1为正常样式
        enabled_buttons = ["0", "1"]
        for btn_text in enabled_buttons:
            button = self.get_button(btn_text)
            if button:
                self.apply_button_style(button, "normal")
            
    def get_current_base(self):
        """获取当前进制"""
        return self.current_base
        
    def get_button_layout(self):
        """获取按钮布局信息"""
        return {
            "rows": 8,
            "cols": 5,
            "buttons": list(self.buttons.keys()),
            "current_base": self.current_base
        }
