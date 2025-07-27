#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
计算引擎 - 计算器的核心计算逻辑
处理表达式解析、计算和错误处理
"""

import math
import re
from PySide6.QtCore import QObject, Signal, Slot
from .history_manager import HistoryManager


class CalculatorEngine(QObject):
    """计算引擎类"""
    
    # 信号定义
    result_ready = Signal(str)      # 计算结果就绪信号
    error_occurred = Signal(str)    # 错误发生信号
    
    def __init__(self):
        super().__init__()
        self.current_expression = ""
        self.last_result = 0
        self.memory_value = 0
        self.angle_mode = "deg"  # 角度模式：deg(度) 或 rad(弧度)
        self.history_manager = HistoryManager()
        
        # 运算符映射
        self.operator_map = {
            "×": "*",
            "÷": "/",
            "√": "sqrt",
            "²": "**2",
            "³": "**3",
            "π": str(math.pi),
            "e": str(math.e),
            "xʸ": "**",
            "10ˣ": "10**",
            "eˣ": "exp",
            "∛": "cbrt",
            "ʸ√": "nthroot",
            "n!": "factorial",
            "mod": "%",
        }
        
    @Slot(str)
    def set_expression(self, expression):
        """设置当前表达式"""
        self.current_expression = expression
        
    @Slot()
    def calculate(self):
        """执行计算"""
        if not self.current_expression or self.current_expression == "0":
            return
            
        try:
            # 预处理表达式
            processed_expr = self.preprocess_expression(self.current_expression)
            
            # 计算结果
            result = self.evaluate_expression(processed_expr)
            
            # 格式化结果
            formatted_result = self.format_result(result)
            
            # 保存结果
            self.last_result = result

            # 添加到历史记录
            self.history_manager.add_record(self.current_expression, formatted_result)

            # 发送结果信号
            self.result_ready.emit(formatted_result)
            
        except Exception as e:
            error_msg = self.get_error_message(e)
            self.error_occurred.emit(error_msg)
            
    def preprocess_expression(self, expression):
        """预处理表达式"""
        # 替换运算符
        processed = expression
        for old_op, new_op in self.operator_map.items():
            processed = processed.replace(old_op, new_op)

        # 处理百分比
        processed = re.sub(r'(\d+(?:\.\d+)?)%', r'(\1/100)', processed)

        # 处理正负号
        processed = processed.replace('±', '-')

        # 处理平方根函数
        processed = processed.replace('√', 'sqrt')
        processed = re.sub(r'sqrt(\d+(?:\.\d+)?)', r'sqrt(\1)', processed)

        # 处理平方
        processed = re.sub(r'(\d+(?:\.\d+)?)\*\*2', r'(\1)**2', processed)

        return processed
        
    def evaluate_expression(self, expression):
        """计算表达式"""
        # 创建安全的计算环境
        safe_dict = {
            "__builtins__": {},
            "abs": abs,
            "round": round,
            "pow": pow,
            "sqrt": math.sqrt,
            "cbrt": lambda x: x**(1/3),
            "nthroot": lambda x, n: x**(1/n),
            "sin": self.sin,
            "cos": self.cos,
            "tan": self.tan,
            "asin": self.asin,
            "acos": self.acos,
            "atan": self.atan,
            "sinh": math.sinh,
            "cosh": math.cosh,
            "tanh": math.tanh,
            "log": math.log10,
            "ln": math.log,
            "exp": math.exp,
            "pi": math.pi,
            "e": math.e,
            "factorial": math.factorial,
            "degrees": math.degrees,
            "radians": math.radians,
            "ceil": math.ceil,
            "floor": math.floor,
        }
        
        # 计算表达式
        result = eval(expression, safe_dict)
        return result
        
    def format_result(self, result):
        """格式化计算结果"""
        if isinstance(result, complex):
            if result.imag == 0:
                result = result.real
            else:
                return f"{result.real:.10g}+{result.imag:.10g}i"
                
        if isinstance(result, float):
            if result.is_integer():
                return str(int(result))
            else:
                # 限制小数位数，避免浮点精度问题
                formatted = f"{result:.10g}"
                return formatted
        else:
            return str(result)
            
    def get_error_message(self, exception):
        """获取友好的错误信息"""
        error_type = type(exception).__name__
        
        if error_type == "ZeroDivisionError":
            return "除数不能为零"
        elif error_type == "ValueError":
            return "输入值无效"
        elif error_type == "OverflowError":
            return "数值溢出"
        elif error_type == "SyntaxError":
            return "表达式语法错误"
        elif "math domain error" in str(exception):
            return "数学域错误"
        else:
            return "计算错误"
            
    # 三角函数（支持角度/弧度模式）
    def sin(self, x):
        """正弦函数"""
        if self.angle_mode == "deg":
            x = math.radians(x)
        return math.sin(x)
        
    def cos(self, x):
        """余弦函数"""
        if self.angle_mode == "deg":
            x = math.radians(x)
        return math.cos(x)
        
    def tan(self, x):
        """正切函数"""
        if self.angle_mode == "deg":
            x = math.radians(x)
        return math.tan(x)
        
    def asin(self, x):
        """反正弦函数"""
        result = math.asin(x)
        if self.angle_mode == "deg":
            result = math.degrees(result)
        return result
        
    def acos(self, x):
        """反余弦函数"""
        result = math.acos(x)
        if self.angle_mode == "deg":
            result = math.degrees(result)
        return result
        
    def atan(self, x):
        """反正切函数"""
        result = math.atan(x)
        if self.angle_mode == "deg":
            result = math.degrees(result)
        return result
        
    # 内存操作
    @Slot()
    def memory_clear(self):
        """清除内存"""
        self.memory_value = 0
        
    @Slot()
    def memory_recall(self):
        """读取内存"""
        self.result_ready.emit(str(self.memory_value))
        
    @Slot()
    def memory_store(self):
        """存储到内存"""
        try:
            self.memory_value = float(self.current_expression)
        except:
            self.memory_value = self.last_result
            
    @Slot()
    def memory_add(self):
        """内存加法"""
        try:
            value = float(self.current_expression)
            self.memory_value += value
        except:
            self.memory_value += self.last_result
            
    @Slot()
    def memory_subtract(self):
        """内存减法"""
        try:
            value = float(self.current_expression)
            self.memory_value -= value
        except:
            self.memory_value -= self.last_result
            
    @Slot()
    def clear(self):
        """清除所有数据"""
        self.current_expression = ""
        self.last_result = 0
        
    def set_angle_mode(self, mode):
        """设置角度模式"""
        if mode in ["deg", "rad"]:
            self.angle_mode = mode
            
    def get_memory_value(self):
        """获取内存值"""
        return self.memory_value

    # 进制转换功能
    def convert_to_base(self, number, base):
        """转换数字到指定进制"""
        try:
            if isinstance(number, str):
                # 如果是字符串，先转换为整数
                if number.startswith('0x'):
                    num = int(number, 16)
                elif number.startswith('0o'):
                    num = int(number, 8)
                elif number.startswith('0b'):
                    num = int(number, 2)
                else:
                    num = int(float(number))
            else:
                num = int(number)

            if base == 2:
                return bin(num)
            elif base == 8:
                return oct(num)
            elif base == 10:
                return str(num)
            elif base == 16:
                return hex(num).upper()
            else:
                return str(num)
        except:
            return "错误"

    def bitwise_operation(self, a, b, operation):
        """位运算"""
        try:
            # 转换为整数
            if isinstance(a, str):
                num_a = int(a, 0)  # 自动识别进制
            else:
                num_a = int(a)

            if isinstance(b, str):
                num_b = int(b, 0)
            else:
                num_b = int(b)

            if operation == "AND":
                return num_a & num_b
            elif operation == "OR":
                return num_a | num_b
            elif operation == "XOR":
                return num_a ^ num_b
            elif operation == "NOT":
                return ~num_a
            elif operation == "LSH":
                return num_a << num_b
            elif operation == "RSH":
                return num_a >> num_b
            else:
                return 0
        except:
            return 0
