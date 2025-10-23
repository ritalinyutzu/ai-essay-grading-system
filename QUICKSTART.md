# ⚡ 5 分鐘快速開始指南

## 🎯 目標

5 分鐘內完成：
1. ✅ 下載專案
2. ✅ 安裝環境
3. ✅ 執行第一個範例

---

## 步驟 1：下載專案（30 秒）

### 選項 A：下載壓縮檔

1. 點擊下載：**ai-essay-grading-system.tar.gz** 或 **ai-essay-grading-system.zip**
2. 解壓縮到任意資料夾

### 選項 B：從 GitHub Clone（如果已部署）

```bash
git clone https://github.com/你的使用者名稱/ai-essay-grading-system.git
cd ai-essay-grading-system
```

---

## 步驟 2：安裝環境（2 分鐘）

打開終端機（PowerShell / Terminal），進入專案目錄：

```bash
# 建立虛擬環境（建議）
python -m venv venv

# 啟動虛擬環境
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 安裝套件
pip install -r requirements.txt
```

**注意：** 首次安裝 EasyOCR 會下載語言模型（約 1-2 GB），請耐心等待。

---

## 步驟 3：測試安裝（30 秒）

```bash
python test_installation.py
```

看到 `✅ 所有套件安裝成功！` 就 OK 了！

---

## 步驟 4：執行第一個範例（1 分鐘）

### 準備作文圖片

1. 找一張作文圖片（手寫或打字都可以）
2. 命名為 `my_essay.jpg`
3. 放到專案根目錄

### 執行批改

```bash
python -c "
from essay_grading_system import EssayGradingSystem
system = EssayGradingSystem()
result = system.grade_essay_from_image('my_essay.jpg')
print(f'總分：{result[\"scores\"][\"total\"]}')
print(f'等級：{result[\"scores\"][\"grade\"]}')
"
```

---

## 🎉 完成！

你已經成功：
- ✅ 安裝 AI 作文批改系統
- ✅ 批改了第一篇作文
- ✅ 獲得評分結果

---

## 下一步

### 📖 查看範例

```bash
# 基本使用
python examples/basic_usage.py

# 批次批改
python examples/batch_grading.py

# 評估系統效能
python examples/evaluation_demo.py
```

### 📚 閱讀文件

- **完整說明：** README.md
- **架構設計：** ARCHITECTURE.md
- **部署指南：** DEPLOYMENT_GUIDE.md

### 🚀 部署到 GitHub

查看 **DEPLOYMENT_GUIDE.md**，手把手教你部署！

---

## ⚠️ 常見問題

### Q: 安裝 EasyOCR 很慢？

**A:** 第一次安裝需要下載模型，約 1-2 GB，請耐心等待。

### Q: 找不到作文圖片？

**A:** 確認圖片路徑正確，建議使用絕對路徑：
```python
result = system.grade_essay_from_image('C:/Users/.../my_essay.jpg')
```

### Q: GPU 支援？

**A:** 安裝 CUDA 和 PyTorch GPU 版本可以加速：
```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

---

## 📞 需要幫助？

- 📧 Email: msmile09@hotmail.com
- 💬 GitHub Issues: 提交問題
- 📖 查看完整文件: README.md

---

**享受 AI 批改作文的樂趣！** 🎓
