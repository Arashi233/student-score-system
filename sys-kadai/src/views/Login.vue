<template>
  <div class="login-container">
    <h1>学生成績管理システム</h1>
    <form @submit.prevent="handleLogin">
      <div class="form-group">
        <label>ユーザー名</label>
        <input v-model="username" type="text" required>
      </div>

      <div class="form-group">
        <label>パスワード</label>
        <input v-model="password" type="password" required>
      </div>

      <div v-if="errorMessage" class="error-message">
        {{ errorMessage }}
      </div>

      <button type="submit" :disabled="loading">
        {{ loading ? 'ログイン中...' : 'ログイン' }}
      </button>
    </form>
  </div>
</template>

<script>
import { authAPI } from '../services/api'

export default {
  data() {
    return {
      username: '',
      password: '',
      errorMessage: '',
      loading: false
    }
  },
  methods: {
    async handleLogin() {
      
      this.errorMessage = ''
      this.loading = true
      
      try {
        const response = await authAPI.login(this.username, this.password)
        localStorage.setItem('token', response.token)
        localStorage.setItem('user', JSON.stringify(response.user))
        
        this.redirectBasedOnUserType(response.user.type)
      } catch (error) {
        if (error.response?.status === 401) {
          this.errorMessage = 'ユーザー名またはパスワードが間違っています'
        } else if (error.response?.data?.detail) {
          this.errorMessage = error.response.data.detail
        } else {
          this.errorMessage = 'ログインに失敗しました。ネットワーク接続を確認してください'
        }
      } finally {
        this.loading = false
      }
    },
    redirectBasedOnUserType(userType) {
      switch(userType) {
        case 1: // Student
          this.$router.push('/student/dashboard')
          break
        case 2: // Admin
          this.$router.push('/admin/dashboard')
          break
        case 3: // Super Admin
          this.$router.push('/super-admin/dashboard')
          break
        default:
          this.errorMessage = '不明なユーザータイプ'
      }
    }
  }
}
</script>

<style scoped>
.login-container {
  max-width: 400px;
  margin: 0 auto;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 5px;
}
.form-group {
  margin-bottom: 15px;
}
label {
  display: block;
  margin-bottom: 5px;
}
input {
  width: 100%;
  padding: 8px;
  box-sizing: border-box;
}
button {
  width: 100%;
  padding: 10px;
  background-color: #42b983;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}
.error-message {
  color: #f56c6c;
  margin-bottom: 15px;
  padding: 10px;
  background-color: #fef0f0;
  border-radius: 4px;
}
</style>