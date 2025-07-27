#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PySide6 多功能计算器
作者：Claude 4.0 sonnet
功能：标准计算器、科学计算器、程序员计算器
"""

import sys
import os
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QIcon

# 添加项目路径到系统路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ui.main_window import MainWindow


def setup_application():
    """设置应用程序的基本属性"""
    app = QApplication(sys.argv)
    
    # 设置应用程序基本信息
    app.setApplicationName("多功能计算器")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("Claude 4.0 sonnet")
    app.setApplicationDisplayName("多功能计算器")
    
    # 设置默认字体为微软雅黑，符合中国用户习惯
    font = QFont("Microsoft YaHei", 10)
    app.setFont(font)
    
    # 设置高DPI支持（Qt 6.x 中这些属性已默认启用）
    # app.setAttribute(Qt.AA_EnableHighDpiScaling, True)  # Qt 6.x 中已弃用
    # app.setAttribute(Qt.AA_UseHighDpiPixmaps, True)     # Qt 6.x 中已弃用
    
    return app


def main():
    """主函数"""
    app = setup_application()
    
    # 创建主窗口
    window = MainWindow()
    window.show()
    
    # 启动应用程序事件循环
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
