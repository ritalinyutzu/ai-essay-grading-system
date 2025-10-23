"""
基本使用範例 - 批改單篇作文
"""

from essay_grading_system import EssayGradingSystem

def main():
    print("="*60)
    print("範例 1：批改單篇作文")
    print("="*60)
    
    # 初始化系統
    print("\n正在初始化系統...")
    system = EssayGradingSystem(languages=['ch_sim', 'en'])
    
    # 批改作文
    # 注意：請將 'essay_sample.jpg' 替換為你的作文圖片路徑
    image_path = 'examples/essay_sample.jpg'
    
    print(f"\n正在批改：{image_path}")
    
    try:
        result = system.grade_essay_from_image(image_path)
        
        # 顯示結果
        print("\n" + "="*60)
        print("批改完成！")
        print("="*60)
        
        # 取得分數
        scores = result['scores']
        features = result['features']
        
        print(f"\n📊 評分結果：")
        print(f"  • 總分：{scores['total']:.1f} / 100")
        print(f"  • 等級：{scores['grade']}")
        print(f"\n📝 分項分數：")
        print(f"  • 內容：{scores['content']:.1f} / 35")
        print(f"  • 結構：{scores['structure']:.1f} / 25")
        print(f"  • 文法：{scores['grammar']:.1f} / 25")
        print(f"  • 用詞：{scores['vocabulary']:.1f} / 15")
        
        print(f"\n📈 作文特徵：")
        print(f"  • 字數：{features['char_count']}")
        print(f"  • 句數：{features['sentence_count']}")
        print(f"  • 段落：{features['paragraph_count']}")
        print(f"  • 詞彙豐富度：{features['vocabulary_richness']:.2%}")
        
    except FileNotFoundError:
        print(f"\n❌ 錯誤：找不到檔案 '{image_path}'")
        print("\n請先準備一張作文圖片，並將路徑更新到程式中。")
        print("圖片格式：JPG, PNG")
        print("建議解析度：300 DPI 以上")
    
    except Exception as e:
        print(f"\n❌ 發生錯誤：{str(e)}")

if __name__ == "__main__":
    main()
