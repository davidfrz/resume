<template>
  <div class="welcome-container">
    <h1>欢迎使用简历管理系统</h1>
    <p>这是一个基于Vue和Django的前后端分离项目</p>
    <el-divider></el-divider>
    <p>您可以通过左侧导航栏访问系统的各个功能</p>
  </div>
</template>

<script setup>
// 欢迎页面不需要特殊逻辑
</script>

<style scoped>
.welcome-container {
  padding: 20px;
  text-align: center;
}

h1 {
  margin-bottom: 20px;
  color: #409EFF;
}

p {
  font-size: 16px;
  color: #606266;
  margin: 10px 0;
}
</style>