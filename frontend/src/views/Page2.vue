<template>
  <div class="page-container">
    <h1>PDF文件转换</h1>
    <el-card class="page-card">
      <div class="card-content">
        <el-upload
          class="upload-demo"
          action="http://localhost:8000/api/pdf/upload/"
          :on-success="handleSuccess"
          :before-upload="beforeUpload"
          :show-file-list="false"
          accept=".pdf">
          <el-button type="primary">点击上传PDF文件</el-button>
          <template #tip>
            <div class="el-upload__tip">
              仅支持PDF格式，大小不超过10MB
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
          title="转换结果"
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
import { ElMessage } from 'element-plus'

const previewImage = ref('')
const uploading = ref(false)
const tableData = ref([])

const beforeUpload = (file) => {
  uploading.value = true;
  const isPDF = file.type === 'application/pdf' || file.name.toLowerCase().endsWith('.pdf')
  const isLt10M = file.size / 1024 / 1024 < 10

  if (!isPDF) {
    ElMessage.error('只能上传PDF格式文件!')
    return false
  }
  if (!isLt10M) {
    ElMessage.error('文件大小不能超过10MB!')
    return false
  }
  return true
}

const handleSuccess = (response) => {
  uploading.value = false
  if (response.code === 200) {
    previewImage.value = response.data.pdf_url
    tableData.value = Object.entries(response.data).filter(([name]) => name!== 'pdf_url').map(([name, value]) => ({name, value}))
  } else {
    ElMessage.error('转换失败: ' + response.message)
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