#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
样式管理器 - 管理计算器的界面样式
提供中国化的界面设计和主题支持
"""

import os
from PySide6.QtCore import QObject


class StyleManager(QObject):
    """样式管理器类"""

    def __init__(self):
        super().__init__()
        self.current_theme = "default"
        self.theme_file = os.path.join(os.path.dirname(__file__), "themes.qss")
        
    def load_theme_from_file(self):
        """从文件加载主题"""
        try:
            with open(self.theme_file, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            return self.get_fallback_style()

    def get_main_window_style(self):
        """获取主窗口样式"""
        return self.load_theme_from_file()

    def get_fallback_style(self):
        """获取备用样式（当主题文件不存在时使用）"""
        return """
            QMainWindow {
                background-color: #F5F5F5;
                color: #333333;
                font-family: "Microsoft YaHei", "SimHei", sans-serif;
            }
            
            QMenuBar {
                background-color: #FFFFFF;
                border-bottom: 1px solid #E0E0E0;
                padding: 4px;
                font-size: 13px;
            }
            
            QMenuBar::item {
                background-color: transparent;
                padding: 6px 12px;
                border-radius: 4px;
            }
            
            QMenuBar::item:selected {
                background-color: #E3F2FD;
                color: #1976D2;
            }
            
            QMenu {
                background-color: #FFFFFF;
                border: 1px solid #CCCCCC;
                border-radius: 6px;
                padding: 4px;
                font-size: 13px;
            }
            
            QMenu::item {
                padding: 8px 20px;
                border-radius: 4px;
            }
            
            QMenu::item:selected {
                background-color: #E3F2FD;
                color: #1976D2;
            }
            
            QStatusBar {
                background-color: #FFFFFF;
                border-top: 1px solid #E0E0E0;
                padding: 4px;
                font-size: 12px;
                color: #666666;
            }
            
            QTabWidget::pane {
                border: 1px solid #CCCCCC;
                border-radius: 6px;
                background-color: #FFFFFF;
                margin-top: -1px;
            }
            
            QTabWidget::tab-bar {
                alignment: center;
            }
            
            QTabBar::tab {
                background-color: #F0F0F0;
                border: 1px solid #CCCCCC;
                border-bottom: none;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
                padding: 8px 20px;
                margin-right: 2px;
                font-size: 14px;
                font-weight: bold;
                color: #666666;
            }
            
            QTabBar::tab:selected {
                background-color: #4A90E2;
                color: #FFFFFF;
                border-color: #357ABD;
            }
            
            QTabBar::tab:hover:!selected {
                background-color: #E3F2FD;
                color: #1976D2;
            }
        """
        
    def get_button_styles(self):
        """获取按钮样式字典"""
        return {
            "normal": """
                QPushButton {
                    background-color: #FFFFFF;
                    color: #333333;
                    border: 1px solid #CCCCCC;
                    border-radius: 6px;
                    font-size: 14px;
                    font-weight: bold;
                    padding: 8px;
                    margin: 1px;
                    font-family: "Microsoft YaHei", "SimHei", sans-serif;
                }
                QPushButton:hover {
                    border-color: #4A90E2;
                    background-color: #F0F8FF;
                }
                QPushButton:pressed {
                    background-color: #E6F3FF;
                    border-color: #2E86AB;
                }
                QPushButton:disabled {
                    background-color: #F5F5F5;
                    color: #CCCCCC;
                    border-color: #E0E0E0;
                }
            """,
            
            "operator": """
                QPushButton {
                    background-color: #4A90E2;
                    color: #FFFFFF;
                    border: 1px solid #357ABD;
                    border-radius: 6px;
                    font-size: 14px;
                    font-weight: bold;
                    padding: 8px;
                    margin: 1px;
                    font-family: "Microsoft YaHei", "SimHei", sans-serif;
                }
                QPushButton:hover {
                    background-color: #357ABD;
                }
                QPushButton:pressed {
                    background-color: #2E86AB;
                }
            """,
            
            "function": """
                QPushButton {
                    background-color: #F8F9FA;
                    color: #495057;
                    border: 1px solid #DEE2E6;
                    border-radius: 6px;
                    font-size: 14px;
                    font-weight: bold;
                    padding: 8px;
                    margin: 1px;
                    font-family: "Microsoft YaHei", "SimHei", sans-serif;
                }
                QPushButton:hover {
                    background-color: #E9ECEF;
                    border-color: #ADB5BD;
                }
                QPushButton:pressed {
                    background-color: #DEE2E6;
                }
                QPushButton:disabled {
                    background-color: #F5F5F5;
                    color: #CCCCCC;
                    border-color: #E0E0E0;
                }
            """,
            
            "special": """
                QPushButton {
                    background-color: #FF8C00;
                    color: #FFFFFF;
                    border: 1px solid #FF7F00;
                    border-radius: 6px;
                    font-size: 16px;
                    font-weight: bold;
                    padding: 8px;
                    margin: 1px;
                    font-family: "Microsoft YaHei", "SimHei", sans-serif;
                }
                QPushButton:hover {
                    background-color: #FF7F00;
                }
                QPushButton:pressed {
                    background-color: #FF6347;
                }
            """
        }
        
    def get_display_styles(self):
        """获取显示区域样式"""
        return {
            "history": """
                QLabel {
                    color: #888888;
                    font-size: 12px;
                    background: transparent;
                    border: none;
                    padding: 2px 8px;
                    font-family: "Consolas", "Microsoft YaHei", monospace;
                }
            """,
            
            "expression": """
                QLineEdit {
                    background-color: #FFFFFF;
                    border: 1px solid #CCCCCC;
                    border-radius: 4px;
                    padding: 8px 12px;
                    font-size: 16px;
                    color: #333333;
                    selection-background-color: #4A90E2;
                    font-family: "Consolas", "Microsoft YaHei", monospace;
                }
                QLineEdit:focus {
                    border-color: #4A90E2;
                }
            """,
            
            "result": """
                QLabel {
                    background-color: #F8F9FA;
                    border: 1px solid #E9ECEF;
                    border-radius: 4px;
                    padding: 12px;
                    font-size: 24px;
                    font-weight: bold;
                    color: #2C3E50;
                    font-family: "Consolas", "Microsoft YaHei", monospace;
                }
            """,
            
            "error": """
                QLabel {
                    background-color: #FFF5F5;
                    border: 1px solid #FEB2B2;
                    border-radius: 4px;
                    padding: 12px;
                    font-size: 18px;
                    font-weight: bold;
                    color: #E53E3E;
                    font-family: "Microsoft YaHei", sans-serif;
                }
            """
        }
        
    def set_theme(self, theme_name):
        """设置主题"""
        if theme_name in ["default", "dark", "light"]:
            self.current_theme = theme_name
            
    def get_current_theme(self):
        """获取当前主题"""
        return self.current_theme
