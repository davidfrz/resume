<template>
  <div class="common-layout">
    <el-container class="container">
      <el-aside width="200px" class="aside">
        <div class="logo-container">
          <h3>简历解析系统</h3>
        </div>
        <el-menu
          :default-active="activeIndex"
          class="el-menu-vertical"
          router
          background-color="#304156"
          text-color="#fff"
          active-text-color="#ffd04b"
        >
          <el-menu-item index="/home">
            <el-icon><HomeFilled /></el-icon>
            <span>首页</span>
          </el-menu-item>
          <el-menu-item index="/home/page1">
            <el-icon><Document /></el-icon>
            <span>图片解析</span>
          </el-menu-item>
          <el-menu-item index="/home/page2">
            <el-icon><Setting /></el-icon>
            <span>PDF解析</span>
          </el-menu-item>
          <!-- <el-menu-item index="/home/page3">
            <el-icon><User /></el-icon>
            <span>页面三</span>
          </el-menu-item> -->
        </el-menu>
      </el-aside>
      <el-container>
        <el-header class="header">
          <div class="header-right">
            <el-dropdown @command="handleCommand">
              <span class="el-dropdown-link">
                {{ username }}<el-icon class="el-icon--right"><arrow-down /></el-icon>
              </span>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item command="logout">退出登录</el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </div>
        </el-header>
        <el-main>
          <router-view />
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { HomeFilled, Document, Setting, User, ArrowDown } from '@element-plus/icons-vue'
import axios from 'axios'

const router = useRouter()
const route = useRoute()

const activeIndex = computed(() => route.path)
const username = ref('')

onMounted(() => {
  const userInfo = JSON.parse(localStorage.getItem('user') || '{}')
  username.value = userInfo.username || '用户'
})

const handleCommand = (command) => {
  if (command === 'logout') {
    ElMessageBox.confirm('确定要退出登录吗?', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }).then(async () => {
      try {
        await axios.post('http://localhost:8000/api/users/logout/')
        localStorage.removeItem('user')
        ElMessage.success('退出成功')
        router.push('/login')
      } catch (error) {
        console.error('退出失败:', error)
        ElMessage.error('退出失败')
      }
    }).catch(() => {})
  }
}
</script>

<style scoped>
.container {
  height: 100vh;
}

.aside {
  background-color: #304156;
  color: white;
}

.logo-container {
  height: 60px;
  display: flex;
  justify-content: center;
  align-items: center;
  color: #fff;
}

.header {
  background-color: #fff;
  color: #333;
  line-height: 60px;
  border-bottom: 1px solid #ddd;
  display: flex;
  justify-content: flex-end;
  align-items: center;
}

.header-right {
  margin-right: 20px;
}

.el-dropdown-link {
  cursor: pointer;
  color: #409EFF;
  display: flex;
  align-items: center;
}
</style>