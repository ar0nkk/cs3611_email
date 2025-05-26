# -*- coding: utf-8 -*-
"""
垃圾邮件管理菜单模块
"""

import os
import sys
import json
from pathlib import Path
from typing import List, Dict

# 添加项目根目录到Python路径
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from common.utils import setup_logging

# 设置日志
logger = setup_logging("spam_menu")

class SpamManagementMenu:
    """垃圾邮件管理菜单"""

    def __init__(self, main_cli):
        """初始化垃圾邮件管理菜单"""
        self.main_cli = main_cli
        self.keywords_file = Path("config/spam_keywords.json")
        self.keywords = self._load_keywords()

    def _load_keywords(self) -> Dict[str, List[str]]:
        """加载垃圾邮件关键词配置"""
        try:
            if not self.keywords_file.exists():
                return {"subject": [], "body": [], "sender": []}
            
            with open(self.keywords_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"加载垃圾邮件关键词失败: {e}")
            return {"subject": [], "body": [], "sender": []}

    def _save_keywords(self):
        """保存垃圾邮件关键词配置"""
        try:
            self.keywords_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.keywords_file, "w", encoding="utf-8") as f:
                json.dump(self.keywords, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            logger.error(f"保存关键词失败: {e}")
            return False

    def show_menu(self):
        """显示垃圾邮件管理菜单"""
        while True:
            self.main_cli.clear_screen()
            print("\n" + "=" * 60)
            print("🛡️ 垃圾邮件管理")
            print("=" * 60)
            print("1. 📋 查看当前关键词")
            print("2. ➕ 添加关键词")
            print("3. ❌ 删除关键词")
            print("4. 📈 调整过滤阈值")
            print("0. 🔙 返回主菜单")
            print("-" * 60)

            choice = input("\n请选择操作 [0-4]: ").strip()

            if choice == "1":
                self._show_current_keywords()
            elif choice == "2":
                self._add_keyword()
            elif choice == "3":
                self._remove_keyword()
            elif choice == "4":
                self._adjust_threshold()
            elif choice == "0":
                return
            else:
                input("❌ 无效选择，请按回车键继续...")

    def _show_current_keywords(self):
        """显示当前关键词配置"""
        self.main_cli.clear_screen()
        print("\n" + "=" * 60)
        print("📋 当前垃圾邮件关键词")
        print("=" * 60)
        
        for category in ["subject", "body", "sender"]:
            print(f"\n🔍 {category.upper()} 关键词:")
            if self.keywords.get(category):
                for i, keyword in enumerate(self.keywords[category], 1):
                    print(f"  {i}. {keyword}")
            else:
                print("  (暂无关键词)")
        
        input("\n按回车键返回...")

    def _add_keyword(self):
        """添加关键词"""
        self.main_cli.clear_screen()
        print("\n" + "=" * 60)
        print("➕ 添加垃圾邮件关键词")
        print("=" * 60)
        print("1. 主题关键词")
        print("2. 正文关键词")
        print("3. 发件人关键词")
        print("0. 取消")
        print("-" * 60)

        choice = input("\n选择要添加的类别 [0-3]: ").strip()
        category_map = {"1": "subject", "2": "body", "3": "sender"}
        
        if choice not in category_map:
            return
        
        category = category_map[choice]
        keyword = input("\n请输入要添加的关键词（支持正则表达式）: ").strip()
        
        if not keyword:
            input("❌ 关键词不能为空，按回车键继续...")
            return
        
        if keyword in self.keywords[category]:
            input("⚠️ 关键词已存在，按回车键继续...")
            return
        
        self.keywords[category].append(keyword)
        if self._save_keywords():
            input(f"✅ 成功添加 {category} 关键词: {keyword}\n按回车键继续...")
        else:
            input("❌ 保存失败，按回车键继续...")

    def _remove_keyword(self):
        """删除关键词"""
        self.main_cli.clear_screen()
        print("\n" + "=" * 60)
        print("❌ 删除垃圾邮件关键词")
        print("=" * 60)
        print("1. 主题关键词")
        print("2. 正文关键词")
        print("3. 发件人关键词")
        print("0. 取消")
        print("-" * 60)

        choice = input("\n选择要删除的类别 [0-3]: ").strip()
        category_map = {"1": "subject", "2": "body", "3": "sender"}
        
        if choice not in category_map:
            return
        
        category = category_map[choice]
        if not self.keywords[category]:
            input(f"❌ {category} 类别没有可删除的关键词，按回车键继续...")
            return
        
        print(f"\n当前 {category} 关键词:")
        for i, kw in enumerate(self.keywords[category], 1):
            print(f"  {i}. {kw}")
        
        try:
            idx = int(input("\n请输入要删除的关键词序号: ")) - 1
            if 0 <= idx < len(self.keywords[category]):
                removed = self.keywords[category].pop(idx)
                if self._save_keywords():
                    input(f"✅ 已删除关键词: {removed}\n按回车键继续...")
                else:
                    input("❌ 保存失败，按回车键继续...")
            else:
                input("❌ 无效的序号，按回车键继续...")
        except ValueError:
            input("❌ 请输入有效数字，按回车键继续...")

    def _adjust_threshold(self):
        """调整过滤阈值"""
        # 示例实现，需根据实际数据库结构调整
        print("\n⚠️ 该功能需要数据库支持，当前为演示实现")
        current_threshold = 3.0
        print(f"当前垃圾邮件阈值: {current_threshold}")
        try:
            new_value = float(input("请输入新的阈值 (0.0-10.0): "))
            if 0 <= new_value <= 10:
                print(f"✅ 已更新阈值为 {new_value}（演示效果）")
            else:
                print("❌ 阈值超出范围")
        except ValueError:
            print("❌ 请输入有效数字")
        input("按回车键继续...")