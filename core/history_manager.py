#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
历史记录管理器 - 管理计算历史记录
支持保存、读取和管理计算历史
"""

from PySide6.QtCore import QObject, Signal
from datetime import datetime
import json
import os


class HistoryManager(QObject):
    """历史记录管理器"""
    
    # 信号定义
    history_updated = Signal()  # 历史记录更新信号
    
    def __init__(self):
        super().__init__()
        self.history = []
        self.max_history = 100  # 最大历史记录数
        self.history_file = "calculator_history.json"
        self.load_history()
        
    def add_record(self, expression, result):
        """添加计算记录"""
        record = {
            "expression": expression,
            "result": result,
            "timestamp": datetime.now().isoformat(),
            "formatted_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # 添加到历史记录开头
        self.history.insert(0, record)
        
        # 限制历史记录数量
        if len(self.history) > self.max_history:
            self.history = self.history[:self.max_history]
            
        # 保存到文件
        self.save_history()
        
        # 发送更新信号
        self.history_updated.emit()
        
    def get_history(self, limit=None):
        """获取历史记录"""
        if limit:
            return self.history[:limit]
        return self.history
        
    def clear_history(self):
        """清除所有历史记录"""
        self.history.clear()
        self.save_history()
        self.history_updated.emit()
        
    def remove_record(self, index):
        """删除指定索引的记录"""
        if 0 <= index < len(self.history):
            self.history.pop(index)
            self.save_history()
            self.history_updated.emit()
            
    def save_history(self):
        """保存历史记录到文件"""
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(self.history, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存历史记录失败: {e}")
            
    def load_history(self):
        """从文件加载历史记录"""
        try:
            if os.path.exists(self.history_file):
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    self.history = json.load(f)
        except Exception as e:
            print(f"加载历史记录失败: {e}")
            self.history = []
            
    def get_recent_expressions(self, limit=10):
        """获取最近的表达式（用于快速重用）"""
        expressions = []
        for record in self.history[:limit]:
            if record["expression"] not in expressions:
                expressions.append(record["expression"])
        return expressions
        
    def search_history(self, keyword):
        """搜索历史记录"""
        results = []
        keyword = keyword.lower()
        
        for record in self.history:
            if (keyword in record["expression"].lower() or 
                keyword in str(record["result"]).lower()):
                results.append(record)
                
        return results
        
    def get_statistics(self):
        """获取使用统计"""
        if not self.history:
            return {
                "total_calculations": 0,
                "most_used_operations": [],
                "calculation_dates": []
            }
            
        # 统计运算符使用频率
        operations = {}
        dates = set()
        
        for record in self.history:
            # 统计日期
            date = record["formatted_time"].split()[0]
            dates.add(date)
            
            # 统计运算符
            expression = record["expression"]
            for op in ["+", "-", "×", "÷", "√", "²", "³"]:
                if op in expression:
                    operations[op] = operations.get(op, 0) + 1
                    
        # 按使用频率排序
        most_used = sorted(operations.items(), key=lambda x: x[1], reverse=True)
        
        return {
            "total_calculations": len(self.history),
            "most_used_operations": most_used[:5],
            "calculation_dates": sorted(list(dates), reverse=True)
        }
