# 🎓 AI 作文自動批改系統

基於 ICR (Intelligent Character Recognition) 和 NLP 技術的智慧作文批改系統

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 📋 目錄

- [系統簡介](#系統簡介)
- [主要功能](#主要功能)
- [技術架構](#技術架構)
- [安裝說明](#安裝說明)
- [快速開始](#快速開始)
- [使用教學](#使用教學)
- [評估指標](#評估指標)
- [專案結構](#專案結構)
- [開發路線圖](#開發路線圖)
- [貢獻指南](#貢獻指南)
- [授權條款](#授權條款)

---

## 🎯 系統簡介

AI 作文自動批改系統能夠：
1. 📸 **讀取作文圖片**（手寫或打字）
2. 🔍 **ICR 文字辨識**（準確率 > 90%）
3. 📊 **智慧評分**（多維度評估）
4. 📈 **效能評估**（Confusion Matrix, F1, Precision, Recall）

### 核心優勢

✅ **快速**：10-30 秒完成批改（vs 人工 5-10 分鐘）  
✅ **便宜**：$0.1-0.5/篇（vs 人工 $5-10/篇）  
✅ **一致**：標準化評分，避免主觀偏差  
✅ **可擴展**：無限批改，不受人力限制  

---

## 🚀 主要功能

### 1. ICR 文字辨識

```python
from essay_grading_system import EssayGradingSystem

system = EssayGradingSystem()
result = system.icr_recognize('essay.jpg')
print(result['text'])  # 辨識出的文字
print(result['confidence'])  # 信心度
```

### 2. 多維度評分

評分維度：
- 📝 **內容**（35%）- 主題切合度、論點完整性、論證充分性
- 🏗️ **結構**（25%）- 結構完整性、段落安排、邏輯連貫性
- ✏️ **文法**（25%）- 文法正確性、標點使用、錯別字
- 📚 **用詞**（15%）- 詞彙豐富度、用詞準確性、修辭技巧

### 3. 評估指標

自動計算：
- 🎯 **Confusion Matrix**（混淆矩陣）
- 📊 **Precision**（精確率）
- 📈 **Recall**（召回率）
- ⭐ **F1 Score**（F1 分數）

---

## 🏗️ 技術架構

```
輸入圖片 → 前處理 → ICR 辨識 → NLP 分析 → 評分 → 輸出結果
                                              ↓
                                         評估指標
```

### 技術棧

| 組件 | 技術 |
|------|------|
| **ICR** | EasyOCR / PaddleOCR |
| **影像處理** | OpenCV, PIL |
| **NLP** | NLTK, spaCy |
| **機器學習** | scikit-learn |
| **視覺化** | Matplotlib, Seaborn |

---

## 💻 安裝說明

### 環境需求

- Python 3.8+
- pip
- （可選）CUDA（GPU 加速）

### 步驟 1：Clone 專案

```bash
git clone https://github.com/ritalinyutzu/ai-essay-grading-system.git
cd ai-essay-grading-system
```

### 步驟 2：建立虛擬環境（建議）

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 步驟 3：安裝依賴套件

```bash
pip install -r requirements.txt
```

**注意：** 首次安裝 EasyOCR 會自動下載語言模型（約 1-2 GB），需要一些時間。

### 步驟 4：驗證安裝

```bash
python test_installation.py
```

如果看到 `✓ 所有套件安裝成功！`，表示安裝完成。

---

## 🎬 快速開始

### 批改單篇作文

```python
from essay_grading_system import EssayGradingSystem

# 初始化系統
system = EssayGradingSystem()

# 批改作文
result = system.grade_essay_from_image('examples/essay_sample.jpg')

# 查看結果
print(f"總分：{result['scores']['total']}")
print(f"等級：{result['scores']['grade']}")
```

### 批次批改作文

```python
import glob
from essay_grading_system import EssayGradingSystem

system = EssayGradingSystem()

# 批次處理資料夾中的所有圖片
image_files = glob.glob('essays/*.jpg')

results = []
for image_path in image_files:
    result = system.grade_essay_from_image(image_path)
    results.append(result)
    print(f"{image_path}: {result['scores']['grade']}")
```

### 評估系統效能

```python
from essay_grading_system import EssayGradingEvaluator

# 建立評估器
evaluator = EssayGradingEvaluator()

# 添加評分結果（預測值 vs 實際值）
evaluator.add_result('A+', 'A+')
evaluator.add_result('A', 'A')
evaluator.add_result('B', 'A')  # 預測錯誤
# ... 更多結果

# 計算評估指標
metrics = evaluator.calculate_metrics()

# 列印報告
evaluator.print_summary(metrics)

# 繪製圖表
evaluator.plot_confusion_matrix(metrics, 'confusion_matrix.png')
evaluator.plot_metrics_comparison(metrics, 'metrics_comparison.png')
```

---

## 📖 使用教學

### 教學 1：基本使用

**輸入：** 作文圖片（JPG, PNG）

```python
from essay_grading_system import EssayGradingSystem

system = EssayGradingSystem(languages=['ch_sim', 'en'])
result = system.grade_essay_from_image('my_essay.jpg')
```

**輸出：**

```
==============================================================
評分結果
==============================================================

【ICR 辨識】
  辨識信心度：92.45%
  辨識字數：856

【作文特徵】
  總字數：856
  句子數：18
  段落數：5
  詞彙豐富度：58.32%
  平均句長：47.6 字

【評分結果】
  內容分數：32.0 / 35
  結構分數：23.0 / 25
  文法分數：22.0 / 25
  用詞分數：12.0 / 15
  ───────────────────
  總分：89.0 / 100
  等級：A

==============================================================
```

---

### 教學 2：自訂評分權重

```python
system = EssayGradingSystem()

# 修改評分權重
system.weights = {
    'content': 0.40,      # 內容 40%
    'structure': 0.30,    # 結構 30%
    'grammar': 0.20,      # 文法 20%
    'vocabulary': 0.10    # 用詞 10%
}

result = system.grade_essay_from_image('essay.jpg')
```

---

### 教學 3：批次評估（含真實標籤）

假設你有一個 CSV 檔案包含真實評分：

**essays_ground_truth.csv**
```csv
image_path,true_grade
essays/001.jpg,A+
essays/002.jpg,A
essays/003.jpg,B
essays/004.jpg,C
```

```python
import pandas as pd
from essay_grading_system import EssayGradingSystem, EssayGradingEvaluator

# 讀取真實標籤
df = pd.read_csv('essays_ground_truth.csv')

# 初始化
system = EssayGradingSystem()
evaluator = EssayGradingEvaluator()

# 批次處理
for _, row in df.iterrows():
    # 批改作文
    result = system.grade_essay_from_image(row['image_path'])
    predicted_grade = result['scores']['grade']
    
    # 添加到評估器
    evaluator.add_result(predicted_grade, row['true_grade'])

# 計算指標
metrics = evaluator.calculate_metrics()

# 顯示結果
evaluator.print_summary(metrics)
evaluator.plot_confusion_matrix(metrics, 'results/confusion_matrix.png')
evaluator.plot_metrics_comparison(metrics, 'results/metrics_comparison.png')
```

---

### 教學 4：API 模式（Web 服務）

建立簡單的 Flask API：

```python
# api.py
from flask import Flask, request, jsonify
from essay_grading_system import EssayGradingSystem
import os

app = Flask(__name__)
system = EssayGradingSystem()

@app.route('/grade', methods=['POST'])
def grade_essay():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400
    
    # 儲存上傳的圖片
    image = request.files['image']
    image_path = f'temp/{image.filename}'
    image.save(image_path)
    
    # 批改作文
    result = system.grade_essay_from_image(image_path)
    
    # 刪除暫存檔案
    os.remove(image_path)
    
    return jsonify({
        'total_score': result['scores']['total'],
        'grade': result['scores']['grade'],
        'content': result['scores']['content'],
        'structure': result['scores']['structure'],
        'grammar': result['scores']['grammar'],
        'vocabulary': result['scores']['vocabulary'],
        'features': result['features']
    })

if __name__ == '__main__':
    os.makedirs('temp', exist_ok=True)
    app.run(debug=True, port=5000)
```

使用方式：

```bash
curl -X POST -F "image=@essay.jpg" http://localhost:5000/grade
```

---

## 📊 評估指標

### Confusion Matrix（混淆矩陣）

顯示實際等級 vs 預測等級的分布：

```
              預測
實際    A+   A    B    C    D    F
A+      50   3    0    0    0    0
A        2  45    5    0    0    0
B        0   4   40    3    0    0
C        0   0    5   38    2    0
D        0   0    0    3   35    2
F        0   0    0    0    2   28
```

### 評估指標公式

**Precision（精確率）：**
```
Precision = TP / (TP + FP)
```
意義：在預測為某等級的作文中，實際為該等級的比例

**Recall（召回率）：**
```
Recall = TP / (TP + FN)
```
意義：在實際為某等級的作文中，被正確預測的比例

**F1 Score（F1 分數）：**
```
F1 = 2 × (Precision × Recall) / (Precision + Recall)
```
意義：Precision 和 Recall 的調和平均數

**Accuracy（準確率）：**
```
Accuracy = (TP + TN) / Total
```
意義：所有預測中，正確預測的比例

---

## 📁 專案結構

```
ai-essay-grading-system/
│
├── essay_grading_system.py    # 主程式
├── requirements.txt            # 依賴套件列表
├── test_installation.py        # 安裝測試腳本
├── README.md                   # 說明文件（本檔案）
├── ARCHITECTURE.md             # 架構設計文件
├── LICENSE                     # MIT 授權
├── .gitignore                  # Git 忽略檔案
│
├── examples/                   # 範例
│   ├── basic_usage.py         # 基本使用範例
│   ├── batch_grading.py       # 批次批改範例
│   ├── evaluation_demo.py     # 評估示範
│   └── essay_sample.jpg       # 範例作文圖片
│
├── data/                       # 資料目錄（不上傳到 Git）
│   ├── essays/                # 作文圖片
│   └── ground_truth.csv       # 真實標籤
│
├── results/                    # 結果輸出
│   ├── confusion_matrix.png   # 混淆矩陣圖
│   └── metrics_comparison.png # 指標比較圖
│
├── models/                     # 模型檔案（不上傳到 Git）
│   └── .gitkeep
│
└── docs/                       # 文件
    ├── API.md                 # API 文件
    ├── TUTORIAL.md            # 詳細教學
    └── FAQ.md                 # 常見問題
```

---

## 🛠️ 開發路線圖

### ✅ Phase 1：核心功能（已完成）
- [x] ICR 文字辨識
- [x] 基礎評分系統
- [x] 評估指標計算
- [x] 視覺化圖表

### 🚧 Phase 2：功能增強（進行中）
- [ ] 更精確的文法檢查
- [ ] 深度學習評分模型（BERT）
- [ ] 詳細評語生成
- [ ] Web UI 介面

### 📋 Phase 3：擴展（計劃中）
- [ ] 多語言支援（英文、日文）
- [ ] 手寫辨識優化
- [ ] RESTful API
- [ ] 線上 Demo 網站

### 🌟 Phase 4：進階（未來）
- [ ] 個性化學習建議
- [ ] 作文風格分析
- [ ] 抄襲檢測
- [ ] 行動 App

---

## 🤝 貢獻指南

歡迎貢獻！請遵循以下步驟：

1. Fork 這個專案
2. 建立你的功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交你的改變 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 開啟 Pull Request

### 開發環境設定

```bash
# 安裝開發依賴
pip install -r requirements-dev.txt

# 執行測試
pytest tests/

# 程式碼格式化
black essay_grading_system.py

# 型別檢查
mypy essay_grading_system.py
```

---

## 📝 授權條款

本專案採用 MIT License。詳見 [LICENSE](LICENSE) 檔案。

---

## 📧 聯絡方式

**專案負責人：** Rita Lin  
**Email：** msmile09@hotmail.com  
**GitHub：** [@ritalinyutzu](https://github.com/ritalinyutzu)

---

## 🙏 致謝

- [EasyOCR](https://github.com/JaidedAI/EasyOCR) - ICR 文字辨識
- [OpenCV](https://opencv.org/) - 影像處理
- [scikit-learn](https://scikit-learn.org/) - 機器學習工具

---

## 📈 引用

如果這個專案對你的研究有幫助，請引用：

```bibtex
@software{ai_essay_grading_system,
  author = {Lin, Rita},
  title = {AI Essay Grading System},
  year = {2025},
  url = {https://github.com/ritalinyutzu/ai-essay-grading-system}
}
```

---

## ⭐ Star History

如果這個專案對你有幫助，請給我們一個 ⭐！

[![Star History Chart](https://api.star-history.com/svg?repos=ritalinyutzu/ai-essay-grading-system&type=Date)](https://star-history.com/#ritalinyutzu/ai-essay-grading-system&Date)

---

**Made with ❤️ by Rita Lin**
