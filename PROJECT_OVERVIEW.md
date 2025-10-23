# 📦 AI 作文批改系統 - 完整專案包

## 📋 專案內容

這個專案包含了完整的 AI 作文自動批改系統，包括：

### ✅ 核心程式

- **essay_grading_system.py** - 主程式（21 KB）
  - ICR 文字辨識
  - 多維度評分系統
  - 評估指標計算（Confusion Matrix, F1, Precision, Recall）

### 📚 文件

- **README.md** - 完整說明文件（12 KB）
- **ARCHITECTURE.md** - 系統架構設計（10 KB）
- **DEPLOYMENT_GUIDE.md** - GitHub 部署完整指南（9 KB）
- **QUICKSTART.md** - 5 分鐘快速開始
- **LICENSE** - MIT 開源授權

### 🎯 範例程式

- **examples/basic_usage.py** - 基本使用範例
- **examples/batch_grading.py** - 批次批改範例
- **examples/evaluation_demo.py** - 評估示範

### 🛠️ 配置檔案

- **requirements.txt** - Python 套件依賴清單
- **test_installation.py** - 安裝測試腳本
- **.gitignore** - Git 忽略檔案配置

### 🚀 部署工具

- **deploy.bat** - Windows 一鍵部署腳本
- **deploy.sh** - Linux/macOS 一鍵部署腳本

### 📁 目錄結構

```
ai-essay-grading-system/
├── 📄 README.md                    # 主要說明文件
├── 📄 ARCHITECTURE.md              # 架構設計
├── 📄 DEPLOYMENT_GUIDE.md          # 部署指南
├── 📄 QUICKSTART.md                # 快速開始
├── 📄 LICENSE                      # MIT 授權
├── 📄 requirements.txt             # 套件清單
├── 📄 test_installation.py         # 測試腳本
├── 📄 essay_grading_system.py      # 主程式
├── 📄 deploy.bat                   # Windows 部署
├── 📄 deploy.sh                    # Linux/macOS 部署
├── 📁 examples/                    # 範例程式
│   ├── basic_usage.py
│   ├── batch_grading.py
│   └── evaluation_demo.py
├── 📁 data/                        # 資料目錄
│   └── essays/                    # 作文圖片
├── 📁 results/                     # 結果輸出
├── 📁 models/                      # 模型檔案
└── 📁 docs/                        # 額外文件
```

---

## 🚀 快速開始

### 方法 1：自動安裝（推薦）

#### Windows:
```cmd
# 雙擊執行
install.bat

# 或在 PowerShell 執行
.\deploy.bat
```

#### Linux/macOS:
```bash
chmod +x deploy.sh
./deploy.sh
```

---

### 方法 2：手動安裝

#### 步驟 1：安裝依賴

```bash
pip install -r requirements.txt
```

#### 步驟 2：測試安裝

```bash
python test_installation.py
```

#### 步驟 3：執行範例

```bash
python examples/basic_usage.py
```

---

## 📖 文件閱讀順序

**第一次使用：**
1. 📄 **QUICKSTART.md** - 5 分鐘快速開始
2. 📄 **README.md** - 完整功能介紹
3. 📁 **examples/** - 查看範例程式

**想要部署到 GitHub：**
1. 📄 **DEPLOYMENT_GUIDE.md** - 手把手部署教學
2. 🚀 **deploy.bat / deploy.sh** - 一鍵部署

**深入了解技術：**
1. 📄 **ARCHITECTURE.md** - 系統架構設計
2. 📄 **essay_grading_system.py** - 閱讀源碼

---

## 💡 核心功能

### 1. ICR 文字辨識
```python
from essay_grading_system import EssayGradingSystem

system = EssayGradingSystem()
result = system.icr_recognize('essay.jpg')
print(result['text'])  # 辨識的文字
print(result['confidence'])  # 信心度
```

### 2. 智慧評分
```python
result = system.grade_essay_from_image('essay.jpg')
print(f"總分：{result['scores']['total']}")
print(f"等級：{result['scores']['grade']}")
```

### 3. 效能評估
```python
from essay_grading_system import EssayGradingEvaluator

evaluator = EssayGradingEvaluator()
evaluator.add_result('A', 'A')  # 預測, 實際
metrics = evaluator.calculate_metrics()
evaluator.print_summary(metrics)
```

---

## 🎯 評分維度

- **內容**（35%）- 主題切合度、論點完整性
- **結構**（25%）- 結構完整性、段落安排
- **文法**（25%）- 文法正確性、標點使用
- **用詞**（15%）- 詞彙豐富度、用詞準確性

---

## 📊 評估指標

- ✅ **Confusion Matrix** - 混淆矩陣
- ✅ **Precision** - 精確率
- ✅ **Recall** - 召回率
- ✅ **F1 Score** - F1 分數
- ✅ **Accuracy** - 準確率

---

## 🌟 特色

- ⚡ **快速**：10-30 秒完成批改
- 💰 **便宜**：$0.1-0.5/篇
- 📊 **科學**：量化評估指標
- 🎯 **準確**：目標準確率 85-90%
- 🔧 **可擴展**：模組化設計

---

## 📦 檔案大小

- 完整專案：約 50 KB（不含模型）
- 壓縮檔：約 22 KB
- 首次安裝需下載：約 1-2 GB（EasyOCR 模型）

---

## 🔧 系統需求

- Python 3.8+
- 記憶體：4 GB+（建議 8 GB+）
- 硬碟：5 GB+（含模型）
- GPU：可選（加速辨識）

---

## 🚀 部署到 GitHub

### 簡易方式（一鍵部署）

#### Windows:
```cmd
deploy.bat
```

#### Linux/macOS:
```bash
./deploy.sh
```

### 完整指南

查看 **DEPLOYMENT_GUIDE.md** 獲得完整的部署教學。

---

## 🤝 如何使用這個專案

### 1. 學習使用
- 閱讀 README.md
- 執行範例程式
- 理解評分邏輯

### 2. 實際應用
- 批改作文
- 批次處理
- 評估系統效能

### 3. 客製化開發
- 修改評分權重
- 新增評分維度
- 整合到自己的系統

### 4. 分享展示
- 部署到 GitHub
- 加入個人履歷
- 在社群分享

---

## 📈 應用場景

### 教育機構
- 學校考試自動批改
- 作業快速評分
- 學生能力追蹤

### 補習班
- 大量作文批改
- 個性化學習建議
- 寫作進步分析

### 線上教育平台
- 即時作文評分
- 自適應學習系統
- 大規模線上考試

### 個人學習
- 練習作文
- 自我評估
- 寫作能力提升

---

## 🎓 學習資源

### 技術文件
- [EasyOCR](https://github.com/JaidedAI/EasyOCR)
- [OpenCV](https://opencv.org/)
- [scikit-learn](https://scikit-learn.org/)

### 相關論文
- Automated Essay Scoring
- OCR Technology
- NLP Evaluation Metrics

---

## 📞 聯絡資訊

**專案負責人：** Rita Lin  
**Email：** msmile09@hotmail.com  
**GitHub：** [@ritalinyutzu](https://github.com/ritalinyutzu)

---

## 🙏 致謝

感謝以下開源專案：
- EasyOCR - 文字辨識
- OpenCV - 影像處理
- scikit-learn - 機器學習
- Matplotlib - 視覺化

---

## 📝 授權

本專案採用 MIT License。  
詳見 LICENSE 檔案。

---

## ⭐ 支持專案

如果這個專案對你有幫助：

1. ⭐ 在 GitHub 給專案一個 Star
2. 🔗 分享給需要的朋友
3. 💬 提供反饋和建議
4. 🤝 參與貢獻開發

---

## 🎉 祝你使用愉快！

**Have fun with AI essay grading!** 🚀

---

**Last Updated:** 2025-10-23  
**Version:** 1.0.0  
**Status:** Production Ready ✅
