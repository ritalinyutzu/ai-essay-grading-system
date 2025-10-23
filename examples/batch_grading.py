"""
批次批改範例 - 批改多篇作文
"""

import glob
import pandas as pd
from essay_grading_system import EssayGradingSystem
from tqdm import tqdm

def main():
    print("="*60)
    print("範例 2：批次批改作文")
    print("="*60)
    
    # 初始化系統
    print("\n正在初始化系統...")
    system = EssayGradingSystem(languages=['ch_sim', 'en'])
    
    # 取得所有作文圖片
    essay_folder = 'data/essays/'
    image_files = glob.glob(essay_folder + '*.jpg') + glob.glob(essay_folder + '*.png')
    
    if not image_files:
        print(f"\n❌ 錯誤：在 '{essay_folder}' 中找不到任何圖片")
        print(f"\n請將作文圖片放到 '{essay_folder}' 資料夾中")
        return
    
    print(f"\n找到 {len(image_files)} 篇作文")
    print("開始批次批改...\n")
    
    # 批次處理
    results = []
    
    for image_path in tqdm(image_files, desc="批改進度"):
        try:
            result = system.grade_essay_from_image(image_path)
            
            # 儲存結果
            results.append({
                'file': image_path,
                'total_score': result['scores']['total'],
                'grade': result['scores']['grade'],
                'content': result['scores']['content'],
                'structure': result['scores']['structure'],
                'grammar': result['scores']['grammar'],
                'vocabulary': result['scores']['vocabulary'],
                'char_count': result['features']['char_count'],
                'sentence_count': result['features']['sentence_count'],
            })
            
        except Exception as e:
            print(f"\n⚠️  批改 {image_path} 時發生錯誤：{str(e)}")
            continue
    
    # 轉換為 DataFrame
    df = pd.DataFrame(results)
    
    # 顯示統計
    print("\n" + "="*60)
    print("批改完成！")
    print("="*60)
    
    print(f"\n📊 統計摘要：")
    print(f"  • 總篇數：{len(df)}")
    print(f"  • 平均分數：{df['total_score'].mean():.2f}")
    print(f"  • 最高分：{df['total_score'].max():.2f}")
    print(f"  • 最低分：{df['total_score'].min():.2f}")
    
    print(f"\n📈 等級分布：")
    grade_counts = df['grade'].value_counts()
    for grade, count in grade_counts.items():
        percentage = count / len(df) * 100
        print(f"  • {grade}: {count} 篇 ({percentage:.1f}%)")
    
    # 儲存結果
    output_file = 'results/batch_results.csv'
    df.to_csv(output_file, index=False, encoding='utf-8-sig')
    print(f"\n💾 結果已儲存至：{output_file}")
    
    # 顯示前 5 名
    print(f"\n🏆 前 5 名作文：")
    top_5 = df.nlargest(5, 'total_score')
    for i, (idx, row) in enumerate(top_5.iterrows(), 1):
        print(f"  {i}. {row['file']}: {row['total_score']:.1f} ({row['grade']})")

if __name__ == "__main__":
    main()
