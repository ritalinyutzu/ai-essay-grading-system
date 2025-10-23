"""
AI 作文自動批改系統
包含 ICR 辨識、評分、評估指標計算
"""

import cv2
import numpy as np
from PIL import Image
import easyocr
from typing import Dict, List, Tuple
import re
from sklearn.metrics import confusion_matrix, classification_report
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

class EssayGradingSystem:
    """AI 作文批改系統"""
    
    def __init__(self, languages=['ch_sim', 'en']):
        """
        初始化系統
        languages: 支援的語言列表
        """
        print("正在載入 ICR 模型...")
        self.reader = easyocr.Reader(languages, gpu=True)
        print("✓ ICR 模型載入完成")
        
        # 評分權重
        self.weights = {
            'content': 0.35,
            'structure': 0.25,
            'grammar': 0.25,
            'vocabulary': 0.15
        }
        
        # 等級定義
        self.grade_thresholds = {
            'A+': 90,
            'A': 80,
            'B': 70,
            'C': 60,
            'D': 50,
            'F': 0
        }
    
    def preprocess_image(self, image_path: str) -> np.ndarray:
        """
        前處理圖片
        
        步驟：
        1. 讀取圖片
        2. 灰階轉換
        3. 去噪
        4. 二值化
        5. 傾斜校正
        """
        # 讀取圖片
        img = cv2.imread(image_path)
        
        if img is None:
            raise ValueError(f"無法讀取圖片：{image_path}")
        
        # 灰階轉換
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # 去噪（高斯模糊）
        denoised = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # 自適應二值化
        binary = cv2.adaptiveThreshold(
            denoised, 255, 
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
            cv2.THRESH_BINARY, 11, 2
        )
        
        # 傾斜校正（簡化版）
        corrected = self._deskew(binary)
        
        return corrected
    
    def _deskew(self, image: np.ndarray) -> np.ndarray:
        """傾斜校正"""
        coords = np.column_stack(np.where(image > 0))
        angle = cv2.minAreaRect(coords)[-1]
        
        if angle < -45:
            angle = -(90 + angle)
        else:
            angle = -angle
        
        # 旋轉圖片
        (h, w) = image.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        rotated = cv2.warpAffine(
            image, M, (w, h),
            flags=cv2.INTER_CUBIC, 
            borderMode=cv2.BORDER_REPLICATE
        )
        
        return rotated
    
    def icr_recognize(self, image_path: str) -> Dict:
        """
        ICR 文字辨識
        
        返回：
        {
            'text': 辨識的文字,
            'confidence': 平均信心度,
            'details': 詳細辨識結果
        }
        """
        print(f"正在辨識圖片：{image_path}")
        
        # 前處理
        processed_img = self.preprocess_image(image_path)
        
        # ICR 辨識
        results = self.reader.readtext(processed_img, detail=1)
        
        # 提取文字和信心度
        recognized_text = []
        confidences = []
        details = []
        
        for (bbox, text, confidence) in results:
            recognized_text.append(text)
            confidences.append(confidence)
            details.append({
                'text': text,
                'confidence': confidence,
                'bbox': bbox
            })
        
        # 組合完整文字
        full_text = ' '.join(recognized_text)
        
        # 後處理：修正常見錯誤
        full_text = self._post_process_text(full_text)
        
        avg_confidence = np.mean(confidences) if confidences else 0
        
        print(f"✓ 辨識完成，平均信心度：{avg_confidence:.2%}")
        
        return {
            'text': full_text,
            'confidence': avg_confidence,
            'details': details,
            'word_count': len(full_text)
        }
    
    def _post_process_text(self, text: str) -> str:
        """後處理：修正常見 OCR 錯誤"""
        # 移除多餘空格
        text = re.sub(r'\s+', ' ', text)
        
        # 常見錯誤修正字典（可擴充）
        corrections = {
            '0': 'O',  # 數字 0 → 字母 O
            '1': 'I',  # 數字 1 → 字母 I
            # 可以加入更多規則
        }
        
        # 這裡可以加入更複雜的拼寫檢查邏輯
        
        return text.strip()
    
    def analyze_essay(self, text: str) -> Dict:
        """
        分析作文內容
        
        提取特徵：
        - 字數
        - 句子數
        - 段落數
        - 詞彙豐富度
        - 平均句長
        - 錯字估計
        """
        # 基本統計
        char_count = len(text)
        word_count = len(text.split())
        
        # 句子分割（簡化版）
        sentences = re.split(r'[。！？.!?]', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        sentence_count = len(sentences)
        
        # 段落分割
        paragraphs = text.split('\n')
        paragraphs = [p.strip() for p in paragraphs if p.strip()]
        paragraph_count = len(paragraphs)
        
        # 詞彙豐富度（TTR = Type-Token Ratio）
        words = text.split()
        unique_words = set(words)
        ttr = len(unique_words) / len(words) if words else 0
        
        # 平均句長
        avg_sentence_length = char_count / sentence_count if sentence_count > 0 else 0
        
        return {
            'char_count': char_count,
            'word_count': word_count,
            'sentence_count': sentence_count,
            'paragraph_count': paragraph_count,
            'vocabulary_richness': ttr,
            'avg_sentence_length': avg_sentence_length
        }
    
    def score_essay(self, text: str, features: Dict) -> Dict:
        """
        評分
        
        評分維度：
        1. 內容（Content）
        2. 結構（Structure）
        3. 文法（Grammar）
        4. 用詞（Vocabulary）
        """
        scores = {}
        
        # 1. 內容評分（0-35）
        scores['content'] = self._score_content(text, features)
        
        # 2. 結構評分（0-25）
        scores['structure'] = self._score_structure(features)
        
        # 3. 文法評分（0-25）
        scores['grammar'] = self._score_grammar(text, features)
        
        # 4. 用詞評分（0-15）
        scores['vocabulary'] = self._score_vocabulary(features)
        
        # 總分
        scores['total'] = sum(scores.values())
        
        # 等級
        scores['grade'] = self._get_grade(scores['total'])
        
        return scores
    
    def _score_content(self, text: str, features: Dict) -> float:
        """
        內容評分（0-35）
        
        評估要點：
        - 字數是否充足
        - 論點是否完整
        - 內容是否豐富
        """
        score = 0
        
        # 字數評分（0-15）
        char_count = features['char_count']
        if char_count >= 800:
            score += 15
        elif char_count >= 600:
            score += 12
        elif char_count >= 400:
            score += 9
        elif char_count >= 200:
            score += 6
        else:
            score += 3
        
        # 論點完整性（0-10）
        # 簡化版：根據段落數量
        paragraph_count = features['paragraph_count']
        if paragraph_count >= 5:
            score += 10
        elif paragraph_count >= 4:
            score += 8
        elif paragraph_count >= 3:
            score += 6
        else:
            score += 4
        
        # 內容豐富度（0-10）
        # 根據詞彙豐富度
        ttr = features['vocabulary_richness']
        if ttr >= 0.6:
            score += 10
        elif ttr >= 0.5:
            score += 8
        elif ttr >= 0.4:
            score += 6
        else:
            score += 4
        
        return min(score, 35)
    
    def _score_structure(self, features: Dict) -> float:
        """
        結構評分（0-25）
        
        評估要點：
        - 段落安排
        - 邏輯順序
        - 起承轉合
        """
        score = 0
        
        # 段落數量（0-10）
        paragraph_count = features['paragraph_count']
        if 4 <= paragraph_count <= 6:
            score += 10
        elif 3 <= paragraph_count <= 7:
            score += 8
        else:
            score += 5
        
        # 句子數量分布（0-10）
        sentence_count = features['sentence_count']
        if sentence_count >= 15:
            score += 10
        elif sentence_count >= 10:
            score += 8
        elif sentence_count >= 5:
            score += 6
        else:
            score += 4
        
        # 平均句長（0-5）
        avg_len = features['avg_sentence_length']
        if 15 <= avg_len <= 30:
            score += 5
        elif 10 <= avg_len <= 40:
            score += 4
        else:
            score += 3
        
        return min(score, 25)
    
    def _score_grammar(self, text: str, features: Dict) -> float:
        """
        文法評分（0-25）
        
        評估要點：
        - 標點符號使用
        - 文法錯誤
        - 錯別字
        """
        score = 25  # 從滿分開始扣分
        
        # 標點符號檢查（簡化版）
        punctuation_count = sum(text.count(p) for p in '，。！？、；：')
        sentence_count = features['sentence_count']
        
        # 標點使用率
        if sentence_count > 0:
            punct_ratio = punctuation_count / sentence_count
            if punct_ratio < 0.5:
                score -= 5
        
        # 這裡可以加入更複雜的文法檢查
        # 例如：使用 LanguageTool 或其他文法檢查工具
        
        return max(score, 0)
    
    def _score_vocabulary(self, features: Dict) -> float:
        """
        用詞評分（0-15）
        
        評估要點：
        - 詞彙豐富度
        - 用詞準確性
        - 修辭技巧
        """
        score = 0
        
        # 詞彙豐富度（0-10）
        ttr = features['vocabulary_richness']
        if ttr >= 0.6:
            score += 10
        elif ttr >= 0.5:
            score += 8
        elif ttr >= 0.4:
            score += 6
        elif ttr >= 0.3:
            score += 4
        else:
            score += 2
        
        # 用詞複雜度（0-5）
        # 簡化版：根據平均字數
        word_count = features['word_count']
        if word_count >= 500:
            score += 5
        elif word_count >= 300:
            score += 4
        elif word_count >= 200:
            score += 3
        else:
            score += 2
        
        return min(score, 15)
    
    def _get_grade(self, total_score: float) -> str:
        """根據總分返回等級"""
        for grade, threshold in self.grade_thresholds.items():
            if total_score >= threshold:
                return grade
        return 'F'
    
    def grade_essay_from_image(self, image_path: str) -> Dict:
        """
        完整流程：從圖片到評分
        
        返回完整結果
        """
        print("\n" + "="*60)
        print("開始批改作文")
        print("="*60)
        
        # 1. ICR 辨識
        icr_result = self.icr_recognize(image_path)
        text = icr_result['text']
        
        print(f"\n辨識文字預覽：")
        print(f"{text[:100]}..." if len(text) > 100 else text)
        
        # 2. 分析作文
        print("\n分析作文特徵...")
        features = self.analyze_essay(text)
        
        # 3. 評分
        print("進行評分...")
        scores = self.score_essay(text, features)
        
        # 4. 組合結果
        result = {
            'image_path': image_path,
            'icr_result': icr_result,
            'features': features,
            'scores': scores,
            'text': text
        }
        
        # 5. 列印結果
        self._print_result(result)
        
        return result
    
    def _print_result(self, result: Dict):
        """列印評分結果"""
        print("\n" + "="*60)
        print("評分結果")
        print("="*60)
        
        scores = result['scores']
        features = result['features']
        icr_result = result['icr_result']
        
        print(f"\n【ICR 辨識】")
        print(f"  辨識信心度：{icr_result['confidence']:.2%}")
        print(f"  辨識字數：{icr_result['word_count']}")
        
        print(f"\n【作文特徵】")
        print(f"  總字數：{features['char_count']}")
        print(f"  句子數：{features['sentence_count']}")
        print(f"  段落數：{features['paragraph_count']}")
        print(f"  詞彙豐富度：{features['vocabulary_richness']:.2%}")
        print(f"  平均句長：{features['avg_sentence_length']:.1f} 字")
        
        print(f"\n【評分結果】")
        print(f"  內容分數：{scores['content']:.1f} / 35")
        print(f"  結構分數：{scores['structure']:.1f} / 25")
        print(f"  文法分數：{scores['grammar']:.1f} / 25")
        print(f"  用詞分數：{scores['vocabulary']:.1f} / 15")
        print(f"  ───────────────────")
        print(f"  總分：{scores['total']:.1f} / 100")
        print(f"  等級：{scores['grade']}")
        
        print("\n" + "="*60)


class EssayGradingEvaluator:
    """評估系統效能"""
    
    def __init__(self):
        self.predictions = []
        self.ground_truth = []
    
    def add_result(self, predicted_grade: str, true_grade: str):
        """添加一筆評分結果"""
        self.predictions.append(predicted_grade)
        self.ground_truth.append(true_grade)
    
    def calculate_metrics(self) -> Dict:
        """
        計算評估指標
        
        返回：
        - Confusion Matrix
        - Precision (每個類別 + 平均)
        - Recall (每個類別 + 平均)
        - F1 Score (每個類別 + 平均)
        - Accuracy
        """
        from sklearn.metrics import (
            confusion_matrix, 
            classification_report,
            accuracy_score,
            precision_recall_fscore_support
        )
        
        # 等級列表
        labels = ['A+', 'A', 'B', 'C', 'D', 'F']
        
        # Confusion Matrix
        cm = confusion_matrix(
            self.ground_truth, 
            self.predictions, 
            labels=labels
        )
        
        # Precision, Recall, F1
        precision, recall, f1, support = precision_recall_fscore_support(
            self.ground_truth,
            self.predictions,
            labels=labels,
            average=None,
            zero_division=0
        )
        
        # 平均指標
        precision_macro = precision_recall_fscore_support(
            self.ground_truth,
            self.predictions,
            average='macro',
            zero_division=0
        )[0]
        
        recall_macro = precision_recall_fscore_support(
            self.ground_truth,
            self.predictions,
            average='macro',
            zero_division=0
        )[1]
        
        f1_macro = precision_recall_fscore_support(
            self.ground_truth,
            self.predictions,
            average='macro',
            zero_division=0
        )[2]
        
        # Accuracy
        accuracy = accuracy_score(self.ground_truth, self.predictions)
        
        # Classification Report
        report = classification_report(
            self.ground_truth,
            self.predictions,
            labels=labels,
            target_names=labels,
            zero_division=0
        )
        
        return {
            'confusion_matrix': cm,
            'labels': labels,
            'precision': precision,
            'recall': recall,
            'f1': f1,
            'support': support,
            'precision_macro': precision_macro,
            'recall_macro': recall_macro,
            'f1_macro': f1_macro,
            'accuracy': accuracy,
            'classification_report': report
        }
    
    def plot_confusion_matrix(self, metrics: Dict, save_path: str = None):
        """繪製混淆矩陣"""
        cm = metrics['confusion_matrix']
        labels = metrics['labels']
        
        plt.figure(figsize=(10, 8))
        sns.heatmap(
            cm, 
            annot=True, 
            fmt='d', 
            cmap='Blues',
            xticklabels=labels,
            yticklabels=labels,
            cbar_kws={'label': '數量'}
        )
        plt.title('Confusion Matrix - 作文評分系統', fontsize=16, pad=20)
        plt.xlabel('預測等級', fontsize=12)
        plt.ylabel('實際等級', fontsize=12)
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"✓ 混淆矩陣已儲存：{save_path}")
        
        plt.show()
    
    def plot_metrics_comparison(self, metrics: Dict, save_path: str = None):
        """繪製各等級的 Precision, Recall, F1 比較圖"""
        labels = metrics['labels']
        precision = metrics['precision']
        recall = metrics['recall']
        f1 = metrics['f1']
        
        x = np.arange(len(labels))
        width = 0.25
        
        fig, ax = plt.subplots(figsize=(12, 6))
        
        bars1 = ax.bar(x - width, precision, width, label='Precision', color='skyblue')
        bars2 = ax.bar(x, recall, width, label='Recall', color='lightcoral')
        bars3 = ax.bar(x + width, f1, width, label='F1 Score', color='lightgreen')
        
        ax.set_xlabel('等級', fontsize=12)
        ax.set_ylabel('分數', fontsize=12)
        ax.set_title('各等級評估指標比較', fontsize=16)
        ax.set_xticks(x)
        ax.set_xticklabels(labels)
        ax.legend()
        ax.set_ylim([0, 1.1])
        ax.grid(axis='y', alpha=0.3)
        
        # 在柱狀圖上標註數值
        def autolabel(bars):
            for bar in bars:
                height = bar.get_height()
                ax.annotate(f'{height:.2f}',
                          xy=(bar.get_x() + bar.get_width() / 2, height),
                          xytext=(0, 3),
                          textcoords="offset points",
                          ha='center', va='bottom',
                          fontsize=8)
        
        autolabel(bars1)
        autolabel(bars2)
        autolabel(bars3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"✓ 指標比較圖已儲存：{save_path}")
        
        plt.show()
    
    def print_summary(self, metrics: Dict):
        """列印評估摘要"""
        print("\n" + "="*60)
        print("系統評估報告")
        print("="*60)
        
        print(f"\n【整體指標】")
        print(f"  準確率（Accuracy）: {metrics['accuracy']:.4f} ({metrics['accuracy']*100:.2f}%)")
        print(f"  平均精確率（Precision）: {metrics['precision_macro']:.4f}")
        print(f"  平均召回率（Recall）: {metrics['recall_macro']:.4f}")
        print(f"  平均 F1 分數（F1 Score）: {metrics['f1_macro']:.4f}")
        
        print(f"\n【各等級詳細指標】")
        labels = metrics['labels']
        precision = metrics['precision']
        recall = metrics['recall']
        f1 = metrics['f1']
        support = metrics['support']
        
        print(f"{'等級':<8} {'Precision':<12} {'Recall':<12} {'F1 Score':<12} {'樣本數':<8}")
        print("-" * 60)
        for i, label in enumerate(labels):
            print(f"{label:<8} {precision[i]:<12.4f} {recall[i]:<12.4f} {f1[i]:<12.4f} {support[i]:<8}")
        
        print("\n【分類報告】")
        print(metrics['classification_report'])
        
        print("="*60)


# 使用範例
if __name__ == "__main__":
    # 初始化系統
    print("初始化 AI 作文批改系統...")
    system = EssayGradingSystem(languages=['ch_sim', 'en'])
    
    # 批改單篇作文
    result = system.grade_essay_from_image('essay_sample.jpg')
    
    # 批次評估（模擬）
    print("\n開始批次評估...")
    evaluator = EssayGradingEvaluator()
    
    # 模擬資料（實際應該從真實資料載入）
    test_data = [
        ('A+', 'A+'),
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'B'),
        ('D', 'D'),
        ('F', 'F'),
        # ... 更多測試資料
    ]
    
    for predicted, actual in test_data:
        evaluator.add_result(predicted, actual)
    
    # 計算評估指標
    metrics = evaluator.calculate_metrics()
    
    # 列印報告
    evaluator.print_summary(metrics)
    
    # 繪製圖表
    evaluator.plot_confusion_matrix(metrics, 'confusion_matrix.png')
    evaluator.plot_metrics_comparison(metrics, 'metrics_comparison.png')
