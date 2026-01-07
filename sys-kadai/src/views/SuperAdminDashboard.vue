<template>
  <div class="dashboard">
    <h1>スーパーユーザーダッシュボード</h1>
    <p>ようこそ、{{ username }}！（スーパーユーザー）</p>
    
    <div class="functions">
      <div class="function-card">
        <h3>ユーザー管理</h3>
        <button @click="showUserModal = true">ユーザー追加</button>
        <button @click="showUserList = true">ユーザー一覧表示</button>
        <button @click="showRoleManagement = true">権限管理</button>
      </div>
    </div>
    
    <button @click="logout" class="logout-btn">ログアウト</button>
  </div>
</template>

<script>
export default {
  data() {
    return {
      username: '',
      showUserModal: false,
      showUserList: false,
      showRoleManagement: false
    }
  },
  mounted() {
    const user = JSON.parse(localStorage.getItem('user') || '{}')
    this.username = user.name || ''
  },
  methods: {
    logout() {
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      this.$router.push('/')
    }
  }
}
</script>

<style scoped>
.dashboard {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.functions {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
  margin: 30px 0;
}

.function-card {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 20px;
  text-align: center;
}

.function-card h3 {
  margin-bottom: 15px;
  color: #333;
}

.function-card button {
  display: block;
  width: 100%;
  margin: 10px 0;
  padding: 10px;
  background-color: #42b983;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.logout-btn {
  margin-top: 30px;
  padding: 10px 20px;
  background-color: #f56c6c;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
</style>