#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
历史记录对话框 - 显示和管理计算历史记录
"""

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QListWidget, QListWidgetItem,
    QPushButton, QLabel, QLineEdit, QMessageBox, QSplitter, QWidget
)
from PySide6.QtCore import Qt, Signal, Slot
from PySide6.QtGui import QFont


class HistoryDialog(QDialog):
    """历史记录对话框"""
    
    # 信号定义
    expression_selected = Signal(str)  # 选择表达式信号
    
    def __init__(self, history_manager, parent=None):
        super().__init__(parent)
        self.history_manager = history_manager
        self.setWindowTitle("计算历史记录")
        self.setMinimumSize(600, 400)
        self.resize(700, 500)
        
        self.init_ui()
        self.load_history()
        self.connect_signals()
        
    def init_ui(self):
        """初始化用户界面"""
        layout = QVBoxLayout(self)
        
        # 搜索区域
        search_layout = QHBoxLayout()
        search_layout.addWidget(QLabel("搜索:"))
        
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("输入关键词搜索历史记录...")
        search_layout.addWidget(self.search_edit)
        
        self.search_button = QPushButton("搜索")
        search_layout.addWidget(self.search_button)
        
        layout.addLayout(search_layout)
        
        # 分割器
        splitter = QSplitter(Qt.Horizontal)
        layout.addWidget(splitter)
        
        # 历史记录列表
        self.history_list = QListWidget()
        self.history_list.setAlternatingRowColors(True)
        splitter.addWidget(self.history_list)
        
        # 详情面板
        details_widget = self.create_details_panel()
        splitter.addWidget(details_widget)
        
        # 设置分割器比例
        splitter.setStretchFactor(0, 2)
        splitter.setStretchFactor(1, 1)
        
        # 按钮区域
        button_layout = QHBoxLayout()
        
        self.use_button = QPushButton("使用选中表达式")
        self.use_button.setEnabled(False)
        button_layout.addWidget(self.use_button)
        
        self.clear_button = QPushButton("清除所有历史")
        button_layout.addWidget(self.clear_button)
        
        button_layout.addStretch()
        
        self.close_button = QPushButton("关闭")
        button_layout.addWidget(self.close_button)
        
        layout.addLayout(button_layout)
        
    def create_details_panel(self):
        """创建详情面板"""
        details_widget = QVBoxLayout()
        
        # 统计信息
        self.stats_label = QLabel("统计信息")
        font = QFont()
        font.setBold(True)
        self.stats_label.setFont(font)
        details_widget.addWidget(self.stats_label)
        
        self.total_label = QLabel("总计算次数: 0")
        details_widget.addWidget(self.total_label)
        
        self.operations_label = QLabel("常用运算:")
        details_widget.addWidget(self.operations_label)
        
        details_widget.addStretch()
        
        # 创建容器widget
        container = QWidget()
        container.setLayout(details_widget)
        return container
        
    def connect_signals(self):
        """连接信号槽"""
        self.search_button.clicked.connect(self.search_history)
        self.search_edit.returnPressed.connect(self.search_history)
        self.search_edit.textChanged.connect(self.on_search_text_changed)
        
        self.history_list.itemSelectionChanged.connect(self.on_selection_changed)
        self.history_list.itemDoubleClicked.connect(self.use_selected_expression)
        
        self.use_button.clicked.connect(self.use_selected_expression)
        self.clear_button.clicked.connect(self.clear_all_history)
        self.close_button.clicked.connect(self.accept)
        
        # 连接历史管理器信号
        self.history_manager.history_updated.connect(self.load_history)
        
    def load_history(self):
        """加载历史记录"""
        self.history_list.clear()
        
        history = self.history_manager.get_history()
        for record in history:
            item_text = f"{record['expression']} = {record['result']}"
            item = QListWidgetItem(item_text)
            item.setData(Qt.UserRole, record)
            
            # 设置工具提示
            tooltip = f"表达式: {record['expression']}\n结果: {record['result']}\n时间: {record['formatted_time']}"
            item.setToolTip(tooltip)
            
            self.history_list.addItem(item)
            
        # 更新统计信息
        self.update_statistics()
        
    def update_statistics(self):
        """更新统计信息"""
        stats = self.history_manager.get_statistics()
        
        self.total_label.setText(f"总计算次数: {stats['total_calculations']}")
        
        if stats['most_used_operations']:
            ops_text = "常用运算:\n"
            for op, count in stats['most_used_operations']:
                ops_text += f"  {op}: {count}次\n"
            self.operations_label.setText(ops_text.strip())
        else:
            self.operations_label.setText("常用运算: 暂无数据")
            
    @Slot()
    def search_history(self):
        """搜索历史记录"""
        keyword = self.search_edit.text().strip()
        if not keyword:
            self.load_history()
            return
            
        self.history_list.clear()
        results = self.history_manager.search_history(keyword)
        
        for record in results:
            item_text = f"{record['expression']} = {record['result']}"
            item = QListWidgetItem(item_text)
            item.setData(Qt.UserRole, record)
            
            tooltip = f"表达式: {record['expression']}\n结果: {record['result']}\n时间: {record['formatted_time']}"
            item.setToolTip(tooltip)
            
            self.history_list.addItem(item)
            
    @Slot()
    def on_search_text_changed(self):
        """搜索文本改变时的处理"""
        if not self.search_edit.text().strip():
            self.load_history()
            
    @Slot()
    def on_selection_changed(self):
        """选择改变时的处理"""
        self.use_button.setEnabled(bool(self.history_list.currentItem()))
        
    @Slot()
    def use_selected_expression(self):
        """使用选中的表达式"""
        current_item = self.history_list.currentItem()
        if current_item:
            record = current_item.data(Qt.UserRole)
            self.expression_selected.emit(record['expression'])
            self.accept()
            
    @Slot()
    def clear_all_history(self):
        """清除所有历史记录"""
        reply = QMessageBox.question(
            self, 
            "确认清除", 
            "确定要清除所有历史记录吗？此操作不可撤销。",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.history_manager.clear_history()
            QMessageBox.information(self, "完成", "历史记录已清除。")
