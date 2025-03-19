<template>
    <div class="page-container">
      <h1>PDF文件转换</h1>
      <el-card class="page-card">
        <div class="card-content">
          <!-- 自定义实体类型输入框和按钮 -->
          
  
          <!-- 实体类型选择框 -->
          
  
          <!-- 上传组件，使用自定义上传方法 -->
          <el-upload
            class="upload-demo"
            :http-request="customUpload"
            :before-upload="beforeUpload"
            :show-file-list="false"
            accept=".pdf"
          >
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
          <el-table-column label="内容">
            <template #default="{ row }">
              <div v-if="typeof row.value === 'object' && row.value!== null">
                <div v-for="(value, key) in row.value" :key="key">
                  {{ key }}: {{ typeof value === 'object'? JSON.stringify(value, null, 2) : value }}
                </div>
              </div>
              <div v-else>{{ row.value }}</div>
            </template>
          </el-table-column>
        </el-table>
        </div>
      </el-card>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue'
  import axios from 'axios'
  import { ElMessage } from 'element-plus'
  
  // 预定义的实体类型（不可删除）
  const predefinedEntities = ['姓名', '出生日期', '电话', '邮箱', '地址']
  
  // 自定义实体类型输入
  const customEntity = ref('')
  
  // 实体类型选项（包括预定义和自定义）
  const entityOptions = ref([
    { value: '姓名', label: '姓名' },
    { value: '出生日期', label: '出生日期' },
    { value: '电话', label: '电话' },
    { value: '邮箱', label: '邮箱' },
    { value: '地址', label: '地址' },
  ])
  
  const selectedEntities = ref([]) // 用户选择的实体类型
  const previewImage = ref('')
  const uploading = ref(false)
  const tableData = ref([])
  
  // 添加自定义标签
  const addCustomEntity = () => {
    const entity = customEntity.value.trim()
    if (!entity) {
      ElMessage.warning('请输入标签名称')
      return
    }
    if (entityOptions.value.some(item => item.value === entity)) {
      ElMessage.warning('该标签已存在')
      return
    }
    entityOptions.value.push({ value: entity, label: entity })
    customEntity.value = '' // 清空输入框
    ElMessage.success('自定义标签已添加')
  }
  
  // 删除自定义标签
  const removeCustomEntity = (value) => {
    entityOptions.value = entityOptions.value.filter(item => item.value !== value)
    selectedEntities.value = selectedEntities.value.filter(item => item !== value)
    ElMessage.success('自定义标签已删除')
  }
  
  // 文件上传前校验
  const beforeUpload = (file) => {
    uploading.value = true
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
  
  // 自定义上传方法
  const customUpload = (uploadFile) => {
    const formData = new FormData()
    formData.append('file', uploadFile.file)
    formData.append('entities', selectedEntities.value.join(',')) // 选择的标签
  
    axios
      .post('http://localhost:8000/api/pdf/upload/', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      })
      .then((response) => handleSuccess(response.data))
      .catch(() => {
        ElMessage.error('上传失败')
        uploading.value = false
      })
  }
  
  // 处理上传成功的响应
  const handleSuccess = (response) => {
    uploading.value = false
    if (response.code === 200) {
      previewImage.value = response.data.pdf_url
      tableData.value = Object.entries(response.data)
        .filter(([name]) => name !== 'pdf_url')
        .map(([name, value]) => ({ name, value }))
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
  </style>