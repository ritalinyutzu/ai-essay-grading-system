# Git 操作指令指南

## 📋 在你的 MacBook 上操作

### 步驟 1: 下載並解壓縮專案檔案

從 Claude.ai 下載 `ai-essay-grading-system.zip`，解壓縮到你想要的位置。

```bash
# 進入專案資料夾
cd ai-essay-grading-system
```

### 步驟 2: 初始化 Git（首次使用）

如果這是全新的資料夾：

```bash
# 初始化 git repository
git init

# 設定遠端 repository
git remote add origin https://github.com/ritalinyutzu/ai-essay-grading-system.git
```

如果資料夾已經有 .git：

```bash
# 確認遠端設定
git remote -v

# 如果沒有設定，則新增
git remote add origin https://github.com/ritalinyutzu/ai-essay-grading-system.git
```

### 步驟 3: 設定 Git 使用者資訊（首次使用）

```bash
# 設定你的名字
git config user.name "Your Name"

# 設定你的 email
git config user.email "your.email@example.com"

# 或使用 --global 設定全域
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

### 步驟 4: 查看變更

```bash
# 查看目前的狀態
git status

# 查看所有檔案變更
git diff
```

### 步驟 5: 提交變更

```bash
# 加入所有新檔案
git add .

# 或只加入特定檔案
git add README.md tools/grading_system.py

# 提交變更（請修改 commit message）
git commit -m "Add AI grading system v1.0

- 新增核心評分系統
- 新增評分分析範例
- 新增完整使用指南
- 新增使用範例"
```

### 步驟 6: 推送到 GitHub

第一次推送（如果是新的 main branch）：

```bash
# 推送到 main branch（首次）
git push -u origin main

# 如果 main branch 不存在，可能需要創建
git branch -M main
git push -u origin main
```

之後的推送：

```bash
# 直接推送
git push
```

### 步驟 7: 處理衝突（如果遠端有其他變更）

```bash
# 先拉取遠端變更
git pull origin main

# 如果有衝突，解決衝突後
git add .
git commit -m "Merge remote changes"
git push
```

---

## 🔐 處理 GitHub 認證

### 方法 1: 使用 Personal Access Token (PAT)

1. 前往 GitHub Settings → Developer settings → Personal access tokens
2. 生成新的 token
3. 推送時輸入 token 作為密碼

```bash
Username: your-github-username
Password: ghp_your_personal_access_token
```

### 方法 2: 使用 SSH Key（推薦）

```bash
# 1. 生成 SSH key（如果還沒有）
ssh-keygen -t ed25519 -C "your.email@example.com"

# 2. 複製公鑰
cat ~/.ssh/id_ed25519.pub

# 3. 前往 GitHub Settings → SSH and GPG keys
#    新增 SSH key，貼上公鑰內容

# 4. 測試連線
ssh -T git@github.com

# 5. 修改 remote URL 為 SSH
git remote set-url origin git@github.com:ritalinyutzu/ai-essay-grading-system.git

# 6. 推送
git push
```

### 方法 3: 使用 GitHub CLI（最簡單）

```bash
# 安裝 GitHub CLI
brew install gh  # macOS

# 登入
gh auth login

# 之後就可以直接 push，不需要輸入密碼
git push
```

---

## 📝 常用 Git 指令

### 查看狀態
```bash
git status              # 查看變更狀態
git log                 # 查看提交歷史
git log --oneline       # 簡潔的歷史
```

### 管理變更
```bash
git add <file>          # 加入特定檔案
git add .               # 加入所有變更
git reset <file>        # 取消暫存特定檔案
git checkout <file>     # 放棄檔案變更
```

### 分支管理
```bash
git branch              # 列出分支
git branch <name>       # 創建新分支
git checkout <name>     # 切換分支
git checkout -b <name>  # 創建並切換分支
```

### 遠端操作
```bash
git remote -v           # 查看遠端設定
git fetch               # 取得遠端變更
git pull                # 拉取並合併
git push                # 推送變更
```

---

## 🚨 常見問題

### Q1: push 時出現 "Permission denied"
**解決方法**：設定 SSH key 或使用 Personal Access Token

### Q2: push 時出現 "rejected"
**原因**：遠端有你本地沒有的變更  
**解決方法**：
```bash
git pull origin main --rebase
git push
```

### Q3: 想要放棄所有本地變更
```bash
git reset --hard HEAD
git clean -fd
```

### Q4: 想要修改最後一次 commit message
```bash
git commit --amend
```

### Q5: 不小心 commit 了不該 commit 的檔案
```bash
# 取消最後一次 commit（保留變更）
git reset --soft HEAD~1

# 或移除特定檔案後重新 commit
git reset HEAD~1
git add <correct_files>
git commit -m "Fixed commit"
```

---

## 📋 完整流程範例

```bash
# 1. 進入專案目錄
cd ai-essay-grading-system

# 2. 查看狀態
git status

# 3. 加入所有變更
git add .

# 4. 提交
git commit -m "Update grading system with new features"

# 5. 推送
git push origin main

# 完成！
```

---

## 🎯 建議的工作流程

### 日常開發

```bash
# 1. 開始工作前，先更新
git pull

# 2. 進行開發...

# 3. 提交變更
git add .
git commit -m "描述你的變更"

# 4. 推送到 GitHub
git push
```

### 大型功能開發

```bash
# 1. 創建功能分支
git checkout -b feature/new-feature

# 2. 開發和提交
git add .
git commit -m "Add new feature"

# 3. 推送分支
git push -u origin feature/new-feature

# 4. 在 GitHub 上創建 Pull Request

# 5. 合併後，切回 main 並更新
git checkout main
git pull
```

---

## 📞 需要幫助？

- Git 官方文件：https://git-scm.com/doc
- GitHub 指南：https://docs.github.com/
- Git 教學：https://gitbook.tw/

---

*最後更新：2025-10-23*
