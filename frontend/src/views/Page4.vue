<template>
  <div class="page-container">
    <h1>PDF文件上传</h1>
    <el-card class="page-card">
      <div class="card-content">
        <el-input
          v-model="inputText"
          placeholder="请输入内容"
          style="margin-bottom: 20px;"
        />
        <el-upload
          class="upload-demo"
          :http-request="customUpload"
          :before-upload="beforeUpload"
          :show-file-list="false"
          multiple
          accept=".pdf"
        >
          <el-button type="primary">点击上传PDF文件</el-button>
          <template #tip>
            <div class="el-upload__tip">
              仅支持PDF格式，大小不超过10MB
            </div>
          </template>
        </el-upload>

        <el-alert
          v-if="tableData.length > 0"
          title="上传结果"
          type="success"
          :closable="false"
          style="margin-bottom: 20px;"
        />

        <el-table :data="tableData" v-loading="uploading" style="width: 100%">
          <el-table-column prop="name" label="项目" width="180" />
          <el-table-column label="合格简历编号">
            <template #default="{ row }">
              <div v-if="row.ids && row.ids.length > 0">
                <el-tag
                  v-for="(id, index) in row.ids"
                  :key="index"
                  type="success"
                  style="margin-right: 5px; margin-bottom: 5px"
                >
                  {{ id }}
                </el-tag>
              </div>
              <el-empty v-else description="暂无合格简历" :image-size="80" />
            </template>
          </el-table-column>
        </el-table>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import axios from 'axios';
import { ElMessage } from 'element-plus';

const uploading = ref(false);
const tableData = ref([]);
const inputText = ref('');

const beforeUpload = (file) => {
  uploading.value = true;
  const isPDF = file.type === 'application/pdf' || file.name.toLowerCase().endsWith('.pdf');
  const isLt10M = file.size / 1024 / 1024 < 10;

  if (!isPDF) {
    ElMessage.error('只能上传PDF格式文件!');
    return false;
  }
  if (!isLt10M) {
    ElMessage.error('文件大小不能超过10MB!');
    return false;
  }
  return true;
};

const customUpload = (uploadFile) => {
  const formData = new FormData();
  // 处理多文件上传
  if (Array.isArray(uploadFile.file)) {
    uploadFile.file.forEach(file => formData.append('files', file));
  } else if (uploadFile.file) {
    formData.append('files', uploadFile.file);
  }
  formData.append('inputText', inputText.value);

  axios
    .post('http://localhost:8000/api/upload-multiple-pdfs/', formData, {
      
    })
    .then((response) => handleSuccess(response.data))
    .catch(() => {
      ElMessage.error('上传失败');
      uploading.value = false;
    });
};

const handleSuccess = (response) => {
  uploading.value = false;
  console.log('完整响应：', response);
  
  if (response.code === 200) {
    // 解析 {1,2} 格式数据
    const parseData = (data) => {
      if (typeof data === 'string' && data.startsWith('{') && data.endsWith('}')) {
        return data.slice(1, -1).split(',').map(Number);
      }
      return data;
    };
    // 兼容数组和单对象格式
    const dataArray = Array.isArray(response.data) ? response.data : [response.data];
    tableData.value = dataArray.map(item => {
      const parsedIds = parseData(item.qualifiedIds);
      return {
        name: item.fileName,
        ids: parsedIds || []
      };
    });
  } else {
    ElMessage.error('上传失败: ' + response.message);
  }
};// 修复：添加缺失的右括号，以闭合 try...catch 块和 submitFiles 函数
</script>

<style scoped>
/* 这里可以添加页面的样式 */
</style>