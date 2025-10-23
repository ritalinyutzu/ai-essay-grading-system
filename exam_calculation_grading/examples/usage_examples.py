"""
AI 自動評分系統 - 使用範例
示範如何使用本系統進行答案評分
"""

import sys
sys.path.append('../tools')
from grading_system import AnswerGrader

def example_1_basic_grading():
    """範例1: 基本評分"""
    print("=" * 60)
    print("範例1: 基本評分")
    print("=" * 60)
    
    # 建立評分器
    grader = AnswerGrader()
    
    # 設定標準答案
    grader.set_standard_answer({
        '電流': 100.0,
        '電壓': 220.0,
        '功率': 22000.0,
    })
    
    # 設定評分標準
    grader.add_criterion('電流', max_score=10.0, tolerance=0.02)
    grader.add_criterion('電壓', max_score=5.0, tolerance=0.01)
    grader.add_criterion('功率', max_score=10.0, tolerance=0.02)
    
    # 學生答案
    student_answer = {
        '電流': 99.5,   # 0.5% 誤差 - OK
        '電壓': 220.0,  # 完全正確
        '功率': 22500.0,  # 2.3% 誤差 - 部分分數
    }
    
    # 評分
    results, total_score = grader.grade_answer(student_answer)
    
    # 顯示結果
    report = grader.generate_report(results, total_score)
    print(report)


def example_2_with_diagram():
    """範例2: 包含圖表的評分"""
    print("\n" + "=" * 60)
    print("範例2: 包含圖表加分")
    print("=" * 60)
    
    grader = AnswerGrader()
    
    grader.set_standard_answer({
        '答案A': 50.0,
        '答案B': 75.0,
    })
    
    grader.add_criterion('答案A', max_score=8.0, tolerance=0.05)
    grader.add_criterion('答案B', max_score=7.0, tolerance=0.05)
    
    student_answer = {
        '答案A': 51.0,
        '答案B': 74.5,
    }
    
    # 學生有繪製圖表，給予加分
    results, total_score = grader.grade_answer(
        student_answer,
        has_diagram=True  # 有圖表加分
    )
    
    report = grader.generate_report(results, total_score)
    print(report)


def example_3_custom_tolerance():
    """範例3: 自定義容許誤差"""
    print("\n" + "=" * 60)
    print("範例3: 不同項目的容許誤差")
    print("=" * 60)
    
    grader = AnswerGrader()
    
    grader.set_standard_answer({
        '精確計算': 1.234567,
        '近似值': 100.0,
    })
    
    # 精確計算要求誤差 < 0.1%
    grader.add_criterion('精確計算', max_score=10.0, tolerance=0.001)
    
    # 近似值容許誤差 < 5%
    grader.add_criterion('近似值', max_score=5.0, tolerance=0.05)
    
    student_answer = {
        '精確計算': 1.235,    # 0.035% 誤差
        '近似值': 102.0,      # 2% 誤差
    }
    
    results, total_score = grader.grade_answer(student_answer)
    report = grader.generate_report(results, total_score)
    print(report)


if __name__ == "__main__":
    print("AI 自動評分系統 - 使用範例\n")
    
    # 執行所有範例
    example_1_basic_grading()
    example_2_with_diagram()
    example_3_custom_tolerance()
    
    print("\n" + "=" * 60)
    print("如需更多資訊，請參閱:")
    print("- docs/complete_guide.md : 完整使用指南")
    print("- docs/answer_analysis.md : 評分分析範例")
    print("- tools/grading_system.py : 評分系統原始碼")
    print("=" * 60)
