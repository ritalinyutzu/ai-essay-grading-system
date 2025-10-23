"""
評估示範 - 計算系統效能指標
包含 Confusion Matrix, Precision, Recall, F1 Score
"""

import pandas as pd
from essay_grading_system import EssayGradingSystem, EssayGradingEvaluator

def main():
    print("="*60)
    print("範例 3：系統效能評估")
    print("="*60)
    
    # 初始化
    system = EssayGradingSystem(languages=['ch_sim', 'en'])
    evaluator = EssayGradingEvaluator()
    
    # 方式 1：從 CSV 讀取真實標籤
    print("\n選項 1：從 CSV 讀取真實標籤")
    print("需要的檔案格式：data/ground_truth.csv")
    print("欄位：image_path, true_grade")
    
    csv_file = 'data/ground_truth.csv'
    
    try:
        # 讀取真實標籤
        df = pd.read_csv(csv_file)
        print(f"\n✓ 讀取 {len(df)} 筆資料")
        
        # 批次批改並評估
        print("\n正在批改作文並收集評估資料...")
        
        for idx, row in df.iterrows():
            try:
                # 批改作文
                result = system.grade_essay_from_image(row['image_path'])
                predicted_grade = result['scores']['grade']
                
                # 添加到評估器
                evaluator.add_result(predicted_grade, row['true_grade'])
                
                print(f"  [{idx+1}/{len(df)}] {row['image_path']}: "
                      f"預測={predicted_grade}, 實際={row['true_grade']}")
                
            except Exception as e:
                print(f"  ⚠️  跳過 {row['image_path']}: {str(e)}")
        
    except FileNotFoundError:
        print(f"\n⚠️  找不到 {csv_file}")
        print("\n使用方式 2：手動模擬資料")
        
        # 方式 2：模擬資料（用於測試）
        print("\n正在使用模擬資料...")
        
        # 模擬 100 筆評分結果
        import random
        grades = ['A+', 'A', 'B', 'C', 'D', 'F']
        
        for i in range(100):
            # 真實等級
            true_grade = random.choice(grades)
            
            # 預測等級（90% 準確率）
            if random.random() < 0.9:
                predicted_grade = true_grade
            else:
                # 10% 機率預測錯誤（通常是相鄰等級）
                grade_idx = grades.index(true_grade)
                if grade_idx > 0 and random.random() < 0.5:
                    predicted_grade = grades[grade_idx - 1]
                elif grade_idx < len(grades) - 1:
                    predicted_grade = grades[grade_idx + 1]
                else:
                    predicted_grade = true_grade
            
            evaluator.add_result(predicted_grade, true_grade)
    
    # 計算評估指標
    print("\n" + "="*60)
    print("正在計算評估指標...")
    print("="*60)
    
    metrics = evaluator.calculate_metrics()
    
    # 列印詳細報告
    evaluator.print_summary(metrics)
    
    # 繪製圖表
    print("\n正在生成視覺化圖表...")
    
    try:
        # 混淆矩陣
        evaluator.plot_confusion_matrix(
            metrics, 
            save_path='results/confusion_matrix.png'
        )
        
        # 指標比較圖
        evaluator.plot_metrics_comparison(
            metrics,
            save_path='results/metrics_comparison.png'
        )
        
        print("\n✅ 圖表已儲存！")
        print("  • results/confusion_matrix.png")
        print("  • results/metrics_comparison.png")
        
    except Exception as e:
        print(f"\n⚠️  繪製圖表時發生錯誤：{str(e)}")
    
    # 分析結果
    print("\n" + "="*60)
    print("結果分析")
    print("="*60)
    
    accuracy = metrics['accuracy']
    f1_macro = metrics['f1_macro']
    
    print(f"\n📊 整體表現：")
    if accuracy >= 0.9:
        print(f"  ✅ 優秀！準確率 {accuracy:.2%} 已達到高水準")
    elif accuracy >= 0.8:
        print(f"  ✓ 良好！準確率 {accuracy:.2%} 符合預期")
    elif accuracy >= 0.7:
        print(f"  ⚠️  尚可。準確率 {accuracy:.2%} 需要改進")
    else:
        print(f"  ❌ 較差。準確率 {accuracy:.2%} 需要大幅優化")
    
    print(f"\n💡 建議：")
    if f1_macro < 0.75:
        print("  • 增加訓練資料")
        print("  • 優化評分規則")
        print("  • 考慮使用深度學習模型")
    elif f1_macro < 0.85:
        print("  • 微調評分權重")
        print("  • 加強文法檢查")
        print("  • 收集更多樣化的訓練資料")
    else:
        print("  • 系統表現良好！")
        print("  • 可以考慮部署到生產環境")

if __name__ == "__main__":
    main()
