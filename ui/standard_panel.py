#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
标准模式面板 - 基础计算器功能
包含数字键、基本运算符和常用功能
"""

from .button_panel import ButtonPanel


class StandardPanel(ButtonPanel):
    """标准计算器面板"""
    
    def __init__(self):
        super().__init__()
        self.create_buttons()
        
    def create_buttons(self):
        """创建标准模式的所有按钮"""
        
        # 第一行：内存和清除功能
        self.create_button("MC", 0, 0, button_type="function")  # 内存清除
        self.create_button("MR", 0, 1, button_type="function")  # 内存读取
        self.create_button("M+", 0, 2, button_type="function")  # 内存加
        self.create_button("M-", 0, 3, button_type="function")  # 内存减
        self.create_button("MS", 0, 4, button_type="function")  # 内存存储
        
        # 第二行：百分比、清除、退格、除法
        self.create_button("%", 1, 0, button_type="function")   # 百分比
        self.create_button("CE", 1, 1, button_type="function")  # 清除输入
        self.create_button("C", 1, 2, button_type="function")   # 全部清除
        self.create_button("⌫", 1, 3, button_type="function")   # 退格
        self.create_button("÷", 1, 4, button_type="operator")   # 除法
        
        # 第三行：倒数、平方、开方、乘法
        self.create_button("1/x", 2, 0, button_type="function") # 倒数
        self.create_button("x²", 2, 1, button_type="function")  # 平方
        self.create_button("√x", 2, 2, button_type="function")  # 开方
        self.create_button("×", 2, 3, button_type="operator")   # 乘法
        
        # 第四行：数字7、8、9、减法
        self.create_button("7", 3, 0, button_type="normal")     # 数字7
        self.create_button("8", 3, 1, button_type="normal")     # 数字8
        self.create_button("9", 3, 2, button_type="normal")     # 数字9
        self.create_button("-", 3, 3, button_type="operator")   # 减法
        
        # 第五行：数字4、5、6、加法
        self.create_button("4", 4, 0, button_type="normal")     # 数字4
        self.create_button("5", 4, 1, button_type="normal")     # 数字5
        self.create_button("6", 4, 2, button_type="normal")     # 数字6
        self.create_button("+", 4, 3, button_type="operator")   # 加法
        
        # 第六行：数字1、2、3、等号（跨两行）
        self.create_button("1", 5, 0, button_type="normal")     # 数字1
        self.create_button("2", 5, 1, button_type="normal")     # 数字2
        self.create_button("3", 5, 2, button_type="normal")     # 数字3
        self.create_button("=", 5, 3, 2, 1, button_type="special")  # 等号（跨两行）
        
        # 第七行：正负号、数字0、小数点
        self.create_button("±", 6, 0, button_type="function")   # 正负号
        self.create_button("0", 6, 1, button_type="normal")     # 数字0
        self.create_button(".", 6, 2, button_type="normal")     # 小数点
        # 等号按钮已经在上一行创建并跨越到这一行
        
        # 调整布局比例，确保按钮均匀分布
        for i in range(5):
            self.layout.setColumnStretch(i, 1)
            self.layout.setColumnMinimumWidth(i, 80)
        for i in range(7):
            self.layout.setRowStretch(i, 1)
            self.layout.setRowMinimumHeight(i, 60)
            
    def get_button_layout(self):
        """获取按钮布局信息（用于测试和调试）"""
        return {
            "rows": 7,
            "cols": 5,
            "buttons": list(self.buttons.keys())
        }
