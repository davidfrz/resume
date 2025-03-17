<template>
  <div class="page-container">
    <h1>页面二</h1>
    <el-card class="page-card">
      <div class="card-content">
        <p>这是页面二的内容区域</p>
        <p>您可以在这里添加简历管理相关的功能</p>
        <el-divider></el-divider>
        <el-empty description="暂无数据"></el-empty>
      </div>
    </el-card>
  </div>
</template>

<script setup>
// 页面二的逻辑可以在这里添加
</script>

<style scoped>
.page-container {
  padding: 20px;
}

h1 {
  margin-bottom: 20px;
  color: #409EFF;
}

.page-card {
  margin-top: 20px;
}

.card-content {
  padding: 10px;
  text-align: center;
}

p {
  font-size: 16px;
  color: #606266;
  margin: 10px 0;
}
</style>