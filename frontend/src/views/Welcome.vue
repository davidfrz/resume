<template>
  <div class="welcome-container">
    <transition name="fade">
      <el-card class="welcome-card">
        <div class="welcome-header">
          <h1>欢迎使用简历筛选系统</h1>
          <p>智能、高效、精准的简历信息提取筛选工具</p>
        </div>
        <el-divider></el-divider>
        <div class="welcome-content">
          <!-- <p>这是一个基于 Vue 和 Django 的前后端分离项目，旨在帮助您快速解析简历中的关键信息。</p>
          <p>通过左侧导航栏，您可以访问以下功能：</p> -->
          <ul class="feature-list">
            <li><i class="el-icon-document"></i> 简历图片解析</li>
            <li><i class="el-icon-files"></i> PDF 文件转换</li>
            <li><i class="el-icon-user"></i> 简历筛选</li>
          </ul>
          <div class="stats">
            <!-- <el-tag type="success">已解析 10 万份简历</el-tag>
            <el-tag type="success">用户好评率 95%</el-tag> -->
          </div>
        </div>
        <el-divider></el-divider>
        <div class="welcome-footer">
          <el-button type="primary" @click="goToPage('/home/page1')">简历解析</el-button>
          <el-button type="text" @click="goToPage('/home/page3')">简历筛选</el-button>
        </div>
      </el-card>
    </transition>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

const goToPage = (path) => {
  router.push(path)
}
</script>

<style scoped>
.welcome-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}

.welcome-card {
  width: 600px;
  padding: 40px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  border-radius: 10px;
  background: #fff;
  transition: all 0.3s ease;
}

.welcome-card:hover {
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
}

.welcome-header h1 {
  font-size: 28px;
  color: #409EFF;
  margin-bottom: 10px;
}

.welcome-header p {
  font-size: 16px;
  color: #606266;
}

.welcome-content p {
  font-size: 16px;
  color: #606266;
  margin: 10px 0;
}

.feature-list {
  list-style: none;
  padding: 0;
  margin: 20px 0;
}

.feature-list li {
  font-size: 16px;
  color: #606266;
  margin: 10px 0;
  display: flex;
  align-items: center;
}

.feature-list i {
  margin-right: 10px;
  color: #409EFF;
}

.stats {
  margin-top: 20px;
  display: flex;
  justify-content: center;
  gap: 20px;
}

.welcome-footer {
  display: flex;
  justify-content: center;
  gap: 20px;
}

.fade-enter-active, .fade-leave-active {
  transition: opacity 0.5s;
}

.fade-enter, .fade-leave-to {
  opacity: 0;
}
</style>