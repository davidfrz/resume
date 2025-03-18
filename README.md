# 项目启动指南

## 前端启动步骤

### 前提条件
- 确保你已经安装了 Node.js 和 npm（Node Package Manager）。你可以通过以下命令检查是否安装：
```bash
node -v
npm -v
```

### 前端启动步骤
1. 进入前端项目目录：
```bash
cd frontend # 假设前端项目目录为frontend
```
2. 安装依赖：
```bash
npm install
```
3. 启动开发服务器：
```bash
npm run dev
```

### 后端启动步骤
#### 前提条件
- 确保你已经安装了 Python 和 pip。你可以通过以下命令检查是否安装：
```bash
python --version
pip --version
```

#### 步骤
1. 创建并激活虚拟环境：
这步请选择你舒服的方式，也可以使用conda虚拟环境
```bash
# python -m venv venv
# # Windows 系统
# venv\Scripts\activate
# # Linux/Mac 系统
# source venv/bin/activate
```
2. 进入后端项目目录：
```bash
cd backend # 假设后端项目目录为backend
```
3. 安装依赖：
```bash
pip install -r requirements.txt # 如果有requirements.txt文件
```
4. 进行数据库迁移：
```bash
python manage.py makemigrations
python manage.py migrate
```
5. 启动开发服务器：
```bash
python manage.py runserver
```
