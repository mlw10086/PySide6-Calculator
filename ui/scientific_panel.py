#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
科学模式面板 - 科学计算器功能
包含三角函数、对数函数、指数函数等高级数学功能
"""

from .button_panel import ButtonPanel


class ScientificPanel(ButtonPanel):
    """科学计算器面板"""
    
    def __init__(self):
        super().__init__()
        self.create_buttons()
        
    def create_buttons(self):
        """创建科学模式的所有按钮"""
        
        # 第一行：角度模式、函数切换、常数
        self.create_button("Deg", 0, 0, button_type="function")  # 角度模式
        self.create_button("F-E", 0, 1, button_type="function")  # 函数切换
        self.create_button("(", 0, 2, button_type="function")    # 左括号
        self.create_button(")", 0, 3, button_type="function")    # 右括号
        self.create_button("MC", 0, 4, button_type="function")   # 内存清除
        self.create_button("MR", 0, 5, button_type="function")   # 内存读取
        
        # 第二行：三角函数
        self.create_button("sin", 1, 0, button_type="function")  # 正弦
        self.create_button("cos", 1, 1, button_type="function")  # 余弦
        self.create_button("tan", 1, 2, button_type="function")  # 正切
        self.create_button("log", 1, 3, button_type="function")  # 常用对数
        self.create_button("M+", 1, 4, button_type="function")   # 内存加
        self.create_button("M-", 1, 5, button_type="function")   # 内存减
        
        # 第三行：反三角函数和自然对数
        self.create_button("asin", 2, 0, button_type="function") # 反正弦
        self.create_button("acos", 2, 1, button_type="function") # 反余弦
        self.create_button("atan", 2, 2, button_type="function") # 反正切
        self.create_button("ln", 2, 3, button_type="function")   # 自然对数
        self.create_button("MS", 2, 4, button_type="function")   # 内存存储
        self.create_button("M", 2, 5, button_type="function")    # 内存显示
        
        # 第四行：指数和幂函数
        self.create_button("π", 3, 0, button_type="function")    # 圆周率
        self.create_button("e", 3, 1, button_type="function")    # 自然常数
        self.create_button("x²", 3, 2, button_type="function")   # 平方
        self.create_button("x³", 3, 3, button_type="function")   # 立方
        self.create_button("xʸ", 3, 4, button_type="function")   # 幂运算
        self.create_button("10ˣ", 3, 5, button_type="function")  # 10的x次方
        
        # 第五行：根号和阶乘
        self.create_button("√x", 4, 0, button_type="function")   # 平方根
        self.create_button("∛x", 4, 1, button_type="function")   # 立方根
        self.create_button("ʸ√x", 4, 2, button_type="function")  # y次根
        self.create_button("n!", 4, 3, button_type="function")   # 阶乘
        self.create_button("1/x", 4, 4, button_type="function")  # 倒数
        self.create_button("eˣ", 4, 5, button_type="function")   # e的x次方
        
        # 第六行：清除和退格
        self.create_button("%", 5, 0, button_type="function")    # 百分比
        self.create_button("CE", 5, 1, button_type="function")   # 清除输入
        self.create_button("C", 5, 2, button_type="function")    # 全部清除
        self.create_button("⌫", 5, 3, button_type="function")    # 退格
        self.create_button("÷", 5, 4, button_type="operator")    # 除法
        self.create_button("mod", 5, 5, button_type="operator")  # 取模
        
        # 第七行：数字7、8、9和乘法
        self.create_button("7", 6, 0, button_type="normal")      # 数字7
        self.create_button("8", 6, 1, button_type="normal")      # 数字8
        self.create_button("9", 6, 2, button_type="normal")      # 数字9
        self.create_button("×", 6, 3, button_type="operator")    # 乘法
        self.create_button("Exp", 6, 4, button_type="function")  # 科学记数法
        self.create_button("dms", 6, 5, button_type="function")  # 度分秒转换
        
        # 第八行：数字4、5、6和减法
        self.create_button("4", 7, 0, button_type="normal")      # 数字4
        self.create_button("5", 7, 1, button_type="normal")      # 数字5
        self.create_button("6", 7, 2, button_type="normal")      # 数字6
        self.create_button("-", 7, 3, button_type="operator")    # 减法
        self.create_button("sinh", 7, 4, button_type="function") # 双曲正弦
        self.create_button("cosh", 7, 5, button_type="function") # 双曲余弦
        
        # 第九行：数字1、2、3和加法
        self.create_button("1", 8, 0, button_type="normal")      # 数字1
        self.create_button("2", 8, 1, button_type="normal")      # 数字2
        self.create_button("3", 8, 2, button_type="normal")      # 数字3
        self.create_button("+", 8, 3, button_type="operator")    # 加法
        self.create_button("tanh", 8, 4, button_type="function") # 双曲正切
        self.create_button("Int", 8, 5, button_type="function")  # 取整
        
        # 第十行：正负号、0、小数点和等号
        self.create_button("±", 9, 0, button_type="function")    # 正负号
        self.create_button("0", 9, 1, button_type="normal")      # 数字0
        self.create_button(".", 9, 2, button_type="normal")      # 小数点
        self.create_button("=", 9, 3, button_type="special")     # 等号
        self.create_button("Rand", 9, 4, button_type="function") # 随机数
        self.create_button("Ave", 9, 5, button_type="function")  # 平均值
        
        # 调整布局比例，确保按钮均匀分布
        for i in range(6):
            self.layout.setColumnStretch(i, 1)
            self.layout.setColumnMinimumWidth(i, 75)
        for i in range(10):
            self.layout.setRowStretch(i, 1)
            self.layout.setRowMinimumHeight(i, 55)
            
    def get_button_layout(self):
        """获取按钮布局信息"""
        return {
            "rows": 10,
            "cols": 6,
            "buttons": list(self.buttons.keys())
        }
