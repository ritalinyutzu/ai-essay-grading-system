"""
答案評分輔助系統
用於比對考生答案與標準答案，並提供評分建議

注意：這是一個輔助工具，不是完整的機器學習模型
真正的自動評分系統需要大量訓練資料（數百到數千份已評分答案）
"""

import re
import math
from typing import Dict, List, Tuple
from dataclasses import dataclass

@dataclass
class Answer:
    """答案資料結構"""
    student_id: str
    values: Dict[str, float]  # 計算結果
    steps: List[str]  # 解題步驟
    has_diagram: bool  # 是否繪製圖表
    
@dataclass
class GradingCriteria:
    """評分標準"""
    item: str
    max_score: float
    tolerance: float  # 容許誤差範圍
    
@dataclass
class GradingResult:
    """評分結果"""
    item: str
    max_score: float
    earned_score: float
    standard_value: float
    student_value: float
    error_rate: float
    feedback: str

class AnswerGrader:
    """答案評分器"""
    
    def __init__(self):
        self.standard_answer = None
        self.criteria = []
        
    def set_standard_answer(self, answer: Dict[str, float]):
        """設定標準答案"""
        self.standard_answer = answer
        
    def add_criterion(self, item: str, max_score: float, tolerance: float = 0.05):
        """新增評分標準
        
        Args:
            item: 評分項目名稱
            max_score: 該項目滿分
            tolerance: 容許誤差（預設5%）
        """
        self.criteria.append(GradingCriteria(item, max_score, tolerance))
        
    def calculate_error_rate(self, standard: float, student: float) -> float:
        """計算誤差率"""
        if standard == 0:
            return float('inf') if student != 0 else 0
        return abs(standard - student) / abs(standard)
    
    def grade_item(self, 
                   item: str, 
                   standard_value: float, 
                   student_value: float,
                   max_score: float,
                   tolerance: float) -> GradingResult:
        """評分單一項目"""
        
        error_rate = self.calculate_error_rate(standard_value, student_value)
        
        # 根據誤差率給分
        if error_rate <= tolerance:
            # 完全正確（誤差在容許範圍內）
            earned_score = max_score
            feedback = f"✅ 完全正確（誤差率: {error_rate*100:.2f}%）"
        elif error_rate <= tolerance * 3:
            # 部分正確（小誤差）
            earned_score = max_score * 0.7
            feedback = f"⚠️ 有小誤差（誤差率: {error_rate*100:.2f}%），給予部分分數"
        elif error_rate <= tolerance * 10:
            # 方法可能對但計算錯誤
            earned_score = max_score * 0.3
            feedback = f"⚠️ 計算錯誤較大（誤差率: {error_rate*100:.2f}%），給予基本分數"
        else:
            # 完全錯誤
            earned_score = 0
            feedback = f"❌ 答案錯誤（誤差率: {error_rate*100:.2f}%）"
            
        return GradingResult(
            item=item,
            max_score=max_score,
            earned_score=earned_score,
            standard_value=standard_value,
            student_value=student_value,
            error_rate=error_rate,
            feedback=feedback
        )
    
    def grade_answer(self, student_answer: Dict[str, float], 
                     has_diagram: bool = False) -> Tuple[List[GradingResult], float]:
        """評分完整答案
        
        Returns:
            評分結果列表, 總分
        """
        results = []
        total_score = 0
        
        for criterion in self.criteria:
            item = criterion.item
            
            if item not in self.standard_answer:
                continue
                
            if item not in student_answer:
                # 未作答
                result = GradingResult(
                    item=item,
                    max_score=criterion.max_score,
                    earned_score=0,
                    standard_value=self.standard_answer[item],
                    student_value=None,
                    error_rate=float('inf'),
                    feedback="❌ 未作答或無法辨識"
                )
            else:
                result = self.grade_item(
                    item=item,
                    standard_value=self.standard_answer[item],
                    student_value=student_answer[item],
                    max_score=criterion.max_score,
                    tolerance=criterion.tolerance
                )
            
            results.append(result)
            total_score += result.earned_score
        
        # 繪製圖表加分
        if has_diagram:
            diagram_bonus = 2.0
            total_score += diagram_bonus
            results.append(GradingResult(
                item="相量圖繪製",
                max_score=2.0,
                earned_score=diagram_bonus,
                standard_value=None,
                student_value=None,
                error_rate=0,
                feedback="✅ 有繪製相量圖，展現理解（加分項）"
            ))
        
        return results, total_score
    
    def generate_report(self, results: List[GradingResult], total_score: float) -> str:
        """生成評分報告"""
        report = "=" * 60 + "\n"
        report += "答案評分報告\n"
        report += "=" * 60 + "\n\n"
        
        max_possible = sum(r.max_score for r in results)
        
        for result in results:
            report += f"項目: {result.item}\n"
            report += f"配分: {result.max_score}分\n"
            report += f"得分: {result.earned_score}分\n"
            
            if result.standard_value is not None:
                report += f"標準答案: {result.standard_value}\n"
            if result.student_value is not None:
                report += f"考生答案: {result.student_value}\n"
                if result.error_rate != float('inf'):
                    report += f"誤差率: {result.error_rate*100:.2f}%\n"
                    
            report += f"評語: {result.feedback}\n"
            report += "-" * 60 + "\n"
        
        report += f"\n總分: {total_score:.1f} / {max_possible:.1f}\n"
        report += f"百分比: {(total_score/max_possible*100):.1f}%\n"
        report += "=" * 60 + "\n"
        
        return report


def example_usage():
    """使用範例：評分本次上傳的答案"""
    
    # 建立評分器
    grader = AnswerGrader()
    
    # 設定標準答案（從orig-2.png）
    grader.set_standard_answer({
        '輸出電流_大小': 114.36275,  # A
        '輸出電流_相角': 10.5,  # degrees
        '輸出實功率': 89591.987,  # W
        '輸出虛功率': 16604.893,  # VAR
        '轉速': 900,  # rpm
        '電磁轉矩': 950.601,  # N-m
    })
    
    # 設定評分標準
    grader.add_criterion('輸出電流_大小', max_score=5.0, tolerance=0.02)
    grader.add_criterion('輸出電流_相角', max_score=1.0, tolerance=0.05)
    grader.add_criterion('輸出實功率', max_score=4.0, tolerance=0.01)
    grader.add_criterion('輸出虛功率', max_score=4.0, tolerance=0.01)
    grader.add_criterion('轉速', max_score=3.0, tolerance=0.01)
    grader.add_criterion('電磁轉矩', max_score=3.0, tolerance=0.01)
    
    # 考生答案（從orig.jpeg手寫答案）
    student_answer = {
        '輸出電流_大小': 66.08,  # A - 錯誤！
        '輸出電流_相角': 0.5,   # degrees - 錯誤！
        '輸出實功率': 89580,    # W - 正確
        '輸出虛功率': 16600,    # VAR - 正確
        '轉速': 900,             # rpm - 正確
        '電磁轉矩': 950.68,      # N-m - 正確
    }
    
    # 評分
    results, total_score = grader.grade_answer(
        student_answer=student_answer,
        has_diagram=True  # 考生有繪製相量圖
    )
    
    # 生成報告
    report = grader.generate_report(results, total_score)
    print(report)
    
    # 分析主要錯誤
    print("\n主要問題分析：")
    print("1. 輸出電流計算錯誤")
    print("   - 考生答案: 66.08∠0.5° A")
    print("   - 標準答案: 114.36∠10.5° A")
    print("   - 可能原因: 標么值轉換或相/線電流混淆")
    print("\n2. 從考生的疑問可見對標么值系統理解有待加強")
    print("   - 需要釐清線電壓與相電壓在標么值計算中的關係")
    

if __name__ == "__main__":
    print("同步發電機答案評分範例\n")
    example_usage()
    
    print("\n" + "="*60)
    print("關於建立完整的自動評分系統：")
    print("="*60)
    print("""
要建立一個機器學習驅動的自動評分系統，需要：

1. 大量訓練資料（建議至少500-1000份已評分答案）
   - 包含各種題型
   - 涵蓋不同分數等級
   - 有詳細的評分標準

2. 特徵工程
   - OCR文字辨識（手寫答案識別）
   - 數學公式解析
   - 計算步驟分析
   - 答案相似度計算

3. 模型訓練
   - 可使用深度學習模型（LSTM、Transformer等）
   - 或傳統ML方法（Random Forest、SVM等）
   - 需要交叉驗證確保模型可靠性

4. 持續優化
   - 收集更多資料
   - 根據教師反饋調整
   - 定期更新模型

本範例提供的是「規則基礎的評分輔助系統」，適合：
- 標準答案明確的計算題
- 小規模評分需求
- 作為教師評分的參考工具

若需要真正的AI自動評分系統，建議：
1. 先收集至少200-500份同類型題目的已評分答案
2. 使用專業的自動評分框架（如AutoEssayGrading）
3. 或考慮使用基於LLM的評分系統（如GPT-4、Claude）
    """)
