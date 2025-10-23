"""
大考中心國文作文範本評分
處理 PDF 格式的手寫作文，進行 ICR 辨識和評分
"""

import json
import os
from datetime import datetime
from essay_grading_system import EssayGradingSystem, EssayGradingEvaluator

# PDF 處理
try:
    from pdf2image import convert_from_path
    PDF_SUPPORT = True
except ImportError:
    PDF_SUPPORT = False
    print("⚠️  警告：未安裝 pdf2image，無法處理 PDF")
    print("   安裝方式：pip install pdf2image")
    print("   Windows 還需要安裝 poppler")


def pdf_to_image(pdf_path, output_dir='temp'):
    """將 PDF 轉換為圖片"""
    if not PDF_SUPPORT:
        raise ImportError("需要安裝 pdf2image")
    
    os.makedirs(output_dir, exist_ok=True)
    
    # 轉換 PDF 第一頁為圖片
    images = convert_from_path(pdf_path, first_page=1, last_page=1, dpi=300)
    
    if images:
        image_path = os.path.join(output_dir, f"{os.path.basename(pdf_path)}.jpg")
        images[0].save(image_path, 'JPEG')
        return image_path
    
    return None

def process_exam_essays():
    """處理大考中心作文範本"""
    
    print("="*60)
    print("大考中心國文作文範本評分系統")
    print("="*60)
    print()
    
    # 初始化系統
    print("正在初始化 AI 評分系統...")
    system = EssayGradingSystem(languages=['ch_sim', 'en'])
    print("✓ 系統初始化完成")
    print()
    
    # 作文檔案
    essay_files = [
        {
            'id': '001',
            'file': 'data/原卷1-1.pdf',
            'title': '大考中心範本 1-1',
            'description': '114 國語文寫作能力測驗'
        },
        {
            'id': '002',
            'file': 'data/原卷1-2.pdf',
            'title': '大考中心範本 1-2',
            'description': '114 國語文寫作能力測驗'
        },
        {
            'id': '003',
            'file': 'data/原卷1-3.pdf',
            'title': '大考中心範本 1-3',
            'description': '114 國語文寫作能力測驗'
        }
    ]
    
    results = []
    
    # 處理每份作文
    for i, essay_info in enumerate(essay_files, 1):
        print(f"[{i}/3] 正在處理：{essay_info['title']}")
        print("-" * 60)
        
        try:
            # 如果是 PDF，先轉換為圖片
            file_path = essay_info['file']
            if file_path.endswith('.pdf'):
                if not PDF_SUPPORT:
                    print(f"✗ 跳過：需要安裝 pdf2image 才能處理 PDF")
                    print()
                    continue
                
                print(f"  正在轉換 PDF 為圖片...")
                file_path = pdf_to_image(file_path)
                if not file_path:
                    print(f"✗ PDF 轉換失敗")
                    print()
                    continue
                print(f"  ✓ 轉換完成")
            
            # 批改作文
            result = system.grade_essay_from_image(file_path)
            
            # 整理結果
            essay_result = {
                'essay_id': essay_info['id'],
                'title': essay_info['title'],
                'description': essay_info['description'],
                'file_path': essay_info['file'],
                'timestamp': datetime.now().isoformat(),
                
                # ICR 辨識結果
                'icr': {
                    'recognized_text': result['text'][:200] + '...' if len(result['text']) > 200 else result['text'],
                    'confidence': round(result['icr_result']['confidence'], 4),
                    'word_count': result['icr_result']['word_count']
                },
                
                # 作文特徵
                'features': {
                    'char_count': result['features']['char_count'],
                    'sentence_count': result['features']['sentence_count'],
                    'paragraph_count': result['features']['paragraph_count'],
                    'vocabulary_richness': round(result['features']['vocabulary_richness'], 4),
                    'avg_sentence_length': round(result['features']['avg_sentence_length'], 2)
                },
                
                # 評分結果
                'scores': {
                    'content': round(result['scores']['content'], 2),
                    'structure': round(result['scores']['structure'], 2),
                    'grammar': round(result['scores']['grammar'], 2),
                    'vocabulary': round(result['scores']['vocabulary'], 2),
                    'total': round(result['scores']['total'], 2),
                    'grade': result['scores']['grade']
                },
                
                # 評語
                'comments': generate_comments(result['scores'])
            }
            
            results.append(essay_result)
            
            # 顯示摘要
            print(f"✓ 批改完成")
            print(f"  總分：{essay_result['scores']['total']} / 100")
            print(f"  等級：{essay_result['scores']['grade']}")
            print(f"  字數：{essay_result['features']['char_count']}")
            print()
            
        except FileNotFoundError:
            print(f"✗ 錯誤：找不到檔案 {essay_info['file']}")
            print(f"  請確認檔案已放到 data/ 資料夾")
            print()
            continue
            
        except Exception as e:
            print(f"✗ 處理失敗：{str(e)}")
            print()
            continue
    
    # 統計摘要
    print("="*60)
    print("評分統計")
    print("="*60)
    
    if results:
        total_scores = [r['scores']['total'] for r in results]
        grades = [r['scores']['grade'] for r in results]
        
        print(f"\n處理篇數：{len(results)}")
        print(f"平均分數：{sum(total_scores)/len(total_scores):.2f}")
        print(f"最高分：{max(total_scores):.2f}")
        print(f"最低分：{min(total_scores):.2f}")
        print(f"\n等級分布：")
        for grade in set(grades):
            count = grades.count(grade)
            print(f"  {grade}: {count} 篇")
    
    # 儲存結果
    output = {
        'metadata': {
            'title': '大考中心國文作文範本評分結果',
            'description': '使用 AI 作文批改系統對大考中心範本進行評分',
            'system_version': '1.0.0',
            'evaluation_date': datetime.now().isoformat(),
            'total_essays': len(results)
        },
        'essays': results,
        'statistics': {
            'average_score': round(sum([r['scores']['total'] for r in results])/len(results), 2) if results else 0,
            'grade_distribution': {grade: grades.count(grade) for grade in set(grades)} if results else {}
        }
    }
    
    output_file = 'sample.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"\n✓ 評分結果已儲存至：{output_file}")
    print()
    
    return output


def generate_comments(scores):
    """根據分數生成評語"""
    comments = {
        'strengths': [],
        'weaknesses': [],
        'suggestions': []
    }
    
    # 內容評語
    if scores['content'] >= 30:
        comments['strengths'].append('內容充實，論點明確')
    elif scores['content'] >= 25:
        comments['strengths'].append('內容尚可，有基本論述')
    else:
        comments['weaknesses'].append('內容較薄弱，論點不夠明確')
        comments['suggestions'].append('建議加強論點的深度和完整性')
    
    # 結構評語
    if scores['structure'] >= 22:
        comments['strengths'].append('結構完整，段落安排合理')
    elif scores['structure'] >= 18:
        comments['strengths'].append('結構基本完整')
    else:
        comments['weaknesses'].append('結構組織需要改進')
        comments['suggestions'].append('建議注意起承轉合的安排')
    
    # 文法評語
    if scores['grammar'] >= 22:
        comments['strengths'].append('文法正確，表達流暢')
    elif scores['grammar'] >= 18:
        comments['strengths'].append('文法大致正確')
    else:
        comments['weaknesses'].append('文法錯誤較多')
        comments['suggestions'].append('建議加強文法和標點符號的使用')
    
    # 用詞評語
    if scores['vocabulary'] >= 13:
        comments['strengths'].append('用詞豐富，修辭得當')
    elif scores['vocabulary'] >= 10:
        comments['strengths'].append('用詞適當')
    else:
        comments['weaknesses'].append('用詞較為平淡')
        comments['suggestions'].append('建議增加詞彙的多樣性和修辭技巧')
    
    # 總體評語
    total = scores['total']
    if total >= 90:
        comments['overall'] = '優秀作品，各方面表現出色'
    elif total >= 80:
        comments['overall'] = '良好作品，整體表現佳'
    elif total >= 70:
        comments['overall'] = '中等作品，有進步空間'
    elif total >= 60:
        comments['overall'] = '及格作品，需要加強練習'
    else:
        comments['overall'] = '需要大幅改進，建議多加練習'
    
    return comments


if __name__ == "__main__":
    # 確保資料夾存在
    os.makedirs('data', exist_ok=True)
    
    # 執行評分
    output = process_exam_essays()
    
    print("="*60)
    print("完成！")
    print("="*60)
    print()
    print("下一步：")
    print("1. 查看 sample.json 檔案")
    print("2. 執行 git add sample.json")
    print("3. 執行 git commit -m '新增：大考中心作文範本評分結果'")
    print("4. 執行 git push")
    print()
