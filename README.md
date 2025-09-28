# ResumeDoctor.ai

ResumeDoctor.ai 是一个基于 AI 的简历分析和岗位推荐应用，帮助用户提升求职效率。用户可以上传简历，系统将自动分析简历质量，生成优化建议，并推荐匹配职位。

## 🌟 项目功能亮点

- 📝 简历上传：支持文本简历或 PDF 文件上传
- 🤖 AI 分析建议：调用书生模型生成个性化优化建议
- 🔍 向量匹配推荐：基于向量模型和 Elasticsearch 推荐相似职位
- 📊 自动评分与反馈：评估简历完成度、亮点和潜力

---

## 📁 项目结构

```
resume-doctor/
├── README.md                      # 项目说明文档
├── frontend/                      # 前端 React 应用
│   ├── public/
│   └── src/
│       └── App.js                # 前端主界面
├── backend/                       # 后端 Flask 服务
│   └── app.py
├── init/                          # 初始化脚本
│   ├── init_mysql.sql            # 建表 SQL 脚本
│   └── init_es.py                # Elasticsearch 初始化
└── .github/workflows/            # 自动部署配置
    └── deploy.yml
```

---

## ⚙️ 技术栈

| 层级    | 技术                   | 描述                        |
| ------- | ---------------------- | --------------------------- |
| 前端    | React                  | 用户交互界面                |
| 后端    | Flask                  | 路由与 API 服务             |
| 数据库  | MySQL                  | 简历信息存储                |
| 检索    | Elasticsearch          | 职位匹配索引                |
| AI 模型 | 向量模型 + 书生模型    | 向量化表示与文本生成        |
| 部署    | Nginx + GitHub Actions | 自动上线到 demo02.2brain.ai |

---

## 🚀 快速开始

### 1. 克隆仓库
```bash
git clone https://github.com/ywuwuwu/resume-doctor.git
cd resume-doctor
```

### 2. 后端环境配置（Flask）
```bash
cd backend
python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

### 3. 前端运行（React）
```bash
cd frontend
npm install
npm start
```

### 4. 配置服务器部署（Nginx & Actions）
- 修改 nginx 配置指向 Flask 和 React build
- 设置 GitHub Secrets 实现服务器自动登录和部署

---

## 🔐 模型与数据库配置

- 向量模型 
- 书生模型 
- MySQL
- ES 地址

