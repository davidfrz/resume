<template>
  <router-view />
</template>

<script setup>
// 主应用组件，使用router-view渲染当前路由对应的组件
</script>

<style>
/* 全局样式可以在这里定义 */
body {
  margin: 0;
  padding: 0;
  font-family: 'Helvetica Neue', Helvetica, 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', Arial, sans-serif;
}

#app {
  width: 100%;
  height: 100%;
}
</style>

methods: {
  async uploadImage() {
    const formData = new FormData();
    formData.append('image', this.selectedImage);
    // 上传图片并获取临时URL
    const response = await fetch('/upload', { method: 'POST', body: formData });
    if (response.ok) {
      const data = await response.json();
      // 设置预览图片的临时URL
      this.previewImageUrl = data.temp_url; // 假设后端返回临时URL为temp_url
      // 保留解析内容展示逻辑
      this.parsedContent = data.data;
    }
  }
},
