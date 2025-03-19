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
          :auto-upload="true"
          ref="uploadRef"
        >
          <el-button type="primary">选择PDF文件上传</el-button>
          <template #tip>
            <div class="el-upload__tip">
              仅支持PDF格式，大小不超过10MB
            </div>
          </template>
        </el-upload>
        <el-button 
          type="success" 
          style="margin-top: 10px;"
          @click="submitFiles"
        >
          开始上传
        </el-button>

        <el-alert
          v-if="tableData.length > 0"
          title="上传结果"
          type="success"
          :closable="false"
          style="margin-bottom: 20px;"
        />

        <!-- 已选择但未上传的文件列表 -->
        <div v-if="selectedFiles.length > 0" style="margin-top: 20px; margin-bottom: 20px;">
          <el-alert
            title="已选择的文件"
            type="info"
            :closable="false"
            style="margin-bottom: 10px;"
          />
          <div>
            <el-tag
              v-for="(file, index) in selectedFiles"
              :key="index"
              type="info"
              style="margin-right: 5px; margin-bottom: 5px"
            >
              {{ file.name }}
            </el-tag>
          </div>
        </div>

        <!-- 上传成功的文件列表 -->
        <el-table :data="[tableData]" v-loading="uploading" style="width: 100%">
          <el-table-column label="合格文件">
            <template #default="{ row }">
              <div v-if="row.length > 0">
                <el-tag
                  v-for="(fileName, index) in row"
                  :key="index"
                  type="success"
                  style="margin-right: 5px; margin-bottom: 5px"
                >
                  {{ fileName }}
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
const selectedFiles = ref([]);

const beforeUpload = (file) => {
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

const uploadRef = ref(null);

const customUpload = (uploadFile) => {
  // 不立即上传，而是将文件添加到selectedFiles数组中
  selectedFiles.value.push(uploadFile.file);
  ElMessage.success(`已选择文件: ${uploadFile.file.name}`);
  // 阻止自动上传
  return false;
};

const submitFiles = () => {
  if (selectedFiles.value.length === 0) {
    ElMessage.warning('请先选择要上传的PDF文件');
    return;
  }
  
  uploading.value = true;
  const formData = new FormData();
  
  // 添加所有选择的文件到formData
  selectedFiles.value.forEach(file => {
    formData.append('files', file);
  });
  
  // 添加输入文本
  formData.append('inputText', inputText.value);
  
  axios
    .post('http://localhost:8000/api/upload-multiple-pdfs/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
    .then((response) => {
      handleSuccess(response.data);
      // 上传成功后清空已选择的文件
      selectedFiles.value = [];
    })
    .catch((error) => {
      console.error('上传错误：', error);
      ElMessage.error('上传失败：' + (error.response?.data?.message || '请稍后重试'));
      uploading.value = false;
    });
};

const handleSuccess = (response) => {
  uploading.value = false;
  console.log('完整响应：', response);
  
  if (response.code === 200) {
    // 直接使用合格文件列表作为表格数据
    if (Array.isArray(response.data)) {
      // 如果返回的是数组，处理每个项目的合格文件
      tableData.value = response.data.flatMap(item => item.qualified || []);
    } else {
      // 如果返回的是单个对象
      tableData.value = response.data.qualified || [];
    }
    ElMessage.success('文件上传成功');
  } else {
    ElMessage.error('上传失败: ' + response.message);
  }
};
</script>

<style scoped>
/* 这里可以添加页面的样式 */
</style>