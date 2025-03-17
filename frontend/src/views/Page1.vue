<template>
  <div class="page-container">
    <h1>简历图片解析</h1>
    <el-card class="page-card">
      <div class="card-content">
        <el-upload
          class="upload-demo"
          action="http://localhost:8000/api/users/upload/"
          :on-success="handleSuccess"
          :before-upload="beforeUpload"
          :show-file-list="false"
          accept=".jpg,.png">
          <el-button type="primary">点击上传简历图片</el-button>
          <template #tip>
            <div class="el-upload__tip">
              支持JPG/PNG格式，大小不超过5MB
            </div>
          </template>
        </el-upload>

        <el-image 
          v-if="previewImage"
          :src="previewImage"
          :preview-src-list="[previewImage]"
          style="margin-top: 20px; max-width: 600px;"
        />

        <el-divider></el-divider>

        <el-alert 
          v-if="tableData.length > 0"
          title="解析结果"
          type="success"
          :closable="false"
          style="margin-bottom: 20px;"
        />

        <el-table :data="tableData" v-loading="uploading" style="width: 100%">
          <el-table-column prop="name" label="项目" width="180" />
          <el-table-column prop="value" label="内容" />
        </el-table>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { ElMessage } from 'element-plus'

const previewImage = ref('')
const uploading = ref(false)
const tableData = ref([])

const beforeUpload = (file) => {
  const isImage = file.type === 'image/jpeg' || file.type === 'image/png'
  const isLt5M = file.size / 1024 / 1024 < 5

  if (!isImage) {
    ElMessage.error('只能上传JPG/PNG格式文件!')
  }
  if (!isLt5M) {
    ElMessage.error('文件大小不能超过5MB!')
  }
  return isImage && isLt5M
}

const handleSuccess = (response) => {
  uploading.value = false
  if (response.code === 200) {
    previewImage.value = response.data.image_url
    tableData.value = Object.entries(response.data).map(([name, value]) => ({
      name,
      value
    }))
  } else {
    ElMessage.error('解析失败: ' + response.message)
  }
}
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
