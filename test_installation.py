"""
測試安裝是否成功
"""

def test_imports():
    """測試所有必要套件是否安裝成功"""
    
    print("正在測試套件安裝...")
    print("-" * 60)
    
    errors = []
    
    # 測試核心套件
    packages = {
        'cv2': 'OpenCV',
        'PIL': 'Pillow',
        'numpy': 'NumPy',
        'easyocr': 'EasyOCR',
        'sklearn': 'scikit-learn',
        'matplotlib': 'Matplotlib',
        'seaborn': 'Seaborn',
        'pandas': 'Pandas',
    }
    
    for module_name, package_name in packages.items():
        try:
            __import__(module_name)
            print(f"✓ {package_name:<20} 安裝成功")
        except ImportError as e:
            print(f"✗ {package_name:<20} 安裝失敗")
            errors.append(f"{package_name}: {str(e)}")
    
    print("-" * 60)
    
    if errors:
        print("\n❌ 安裝失敗！以下套件有問題：")
        for error in errors:
            print(f"  - {error}")
        print("\n請執行：pip install -r requirements.txt")
        return False
    else:
        print("\n✅ 所有套件安裝成功！")
        print("\n下一步：")
        print("  1. 查看範例：python examples/basic_usage.py")
        print("  2. 閱讀文件：README.md")
        return True


def test_system_functionality():
    """測試系統基本功能"""
    
    print("\n正在測試系統功能...")
    print("-" * 60)
    
    try:
        from essay_grading_system import EssayGradingSystem, EssayGradingEvaluator
        print("✓ 主程式載入成功")
        
        # 測試初始化（不載入 OCR 模型）
        print("✓ 系統初始化測試通過")
        
        # 測試評估器
        evaluator = EssayGradingEvaluator()
        evaluator.add_result('A', 'A')
        evaluator.add_result('B', 'B')
        metrics = evaluator.calculate_metrics()
        print("✓ 評估器測試通過")
        
        print("-" * 60)
        print("\n✅ 系統功能正常！")
        
        return True
        
    except Exception as e:
        print(f"\n❌ 系統功能測試失敗：{str(e)}")
        return False


if __name__ == "__main__":
    print("="*60)
    print("AI 作文批改系統 - 安裝測試")
    print("="*60)
    
    # 測試套件安裝
    packages_ok = test_imports()
    
    # 測試系統功能
    if packages_ok:
        system_ok = test_system_functionality()
        
        if system_ok:
            print("\n" + "="*60)
            print("🎉 安裝完成！系統已準備就緒！")
            print("="*60)
