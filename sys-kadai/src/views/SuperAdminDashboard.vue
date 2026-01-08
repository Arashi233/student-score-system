<template>
  <div class="dashboard">
    <h1>スーパーユーザーダッシュボード</h1>
    <p>ようこそ、{{ username }}！（スーパーユーザー）</p>
    
    <div class="functions">
      <div class="function-card">
        <h3>ユーザー管理</h3>
        <button @click="showUserModal = true">ユーザー追加</button>
        <button @click="showUserList = true">ユーザー一覧表示</button>
      </div>
    </div>
    
    <!-- ユーザー追加モーダル -->
    <div v-if="showUserModal" class="modal-overlay">
      <div class="modal">
        <h3>ユーザー追加</h3>
        <form @submit.prevent="addUser">
          <div class="form-group">
            <label>氏名：</label>
            <input v-model="newUser.name" type="text" required />
          </div>
          <div class="form-group">
            <label>パスワード：</label>
            <input v-model="newUser.pwd" type="password" required />
          </div>
          <div class="form-group">
            <label>権限：</label>
            <select v-model="newUser.type" required>
              <option value="">権限を選択してください</option>
              <option value=1>学生</option>
              <option value=2>管理員</option>
              <option value=3>スーパー管理員</option>
            </select>
          </div>
          <div class="form-actions">
            <button type="submit" class="btn-primary">追加</button>
            <button type="button" @click="showUserModal = false" class="btn-cancel">キャンセル</button>
          </div>
        </form>
      </div>
    </div>
    
    <!-- ユーザー一覧表示モーダル -->
    <div v-if="showUserList" class="modal-overlay">
      <div class="modal">
        <h3>ユーザー一覧</h3>
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>氏名</th>
              <th>権限</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="user in users" :key="user.id">
              <td>{{ user.id }}</td>
              <td>{{ user.name }}</td>
              <td>
                <select v-model="user.type" @change="updateUserPermission(user.id, user.type)">
                  <option value=1>学生</option>
                  <option value=2>管理員</option>
                  <option value=3>スーパー管理員</option>
                </select>
              </td>
              <td>
                <button @click="deleteUser(user.id)" class="btn-delete">削除</button>
              </td>
            </tr>
          </tbody>
        </table>
        <button type="button" @click="showUserList = false" class="btn-cancel">閉じる</button>
      </div>
    </div>
    
    <button @click="logout" class="logout-btn">ログアウト</button>
  </div>
</template>

<script>
  
import { authAPI } from '@/services/api'
export default {
  data() {
    return {
      username: '',
      showUserModal: false,
      showUserList: false,
      showRoleManagement: false,
      newUser: { name: '', pwd: '', type: '' },
      users: []
    }
  },
  mounted() {
    const user = JSON.parse(localStorage.getItem('user') || '{}')
    this.username = user.name || ''
    this.loadUsers()
  },
  methods: {
    async loadUsers() {
      try {
        this.users = await authAPI.getusers();
        console.log(this.users);
      } catch (error) {
        console.error('ユーザー情報の読み込みに失敗しました:', error);
      }
    },
    async addUser() {
      try {
        await authAPI.create_user(this.newUser.name, this.newUser.pwd, this.newUser.type)
        alert('ユーザー追加成功！')
        this.showUserModal = false
        this.newUser = { name: '', pwd: '', type: '' }
        this.loadUsers() // 追加後にユーザー一覧を再ロード
      } catch (error) {
        alert('ユーザー追加に失敗しました。')
      }
    },
    async updateUserPermission(userId, type) {
      try {
        // API呼び出しをシミュレート
        // 実際には以下のようにAPIを呼び出す
        console.log(`Updating user ${userId} to type ${type}`);
        await authAPI.updateUserType(userId, type);
        
        alert('権限更新成功！')
      } catch (error) {
        alert('権限更新に失敗しました。')
      }
    },
    async deleteUser(userId) {
      if (confirm('本当にこのユーザーを削除しますか？')) {
        try {
          // API呼び出しをシミュレート
          // 実際には以下のようにAPIを呼び出す
          await authAPI.deleteUser(userId);
          alert('ユーザー削除成功！')
          this.loadUsers() // 削除後にユーザー一覧を再ロード
        } catch (error) {
          alert('ユーザー削除に失敗しました。')
        }
      }
    },
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

/* Modal styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal {
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  width: 90%;
  max-width: 600px;
  max-height: 80vh;
  overflow-y: auto;
}

.modal table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 15px;
}

.modal th, .modal td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: left;
}

.modal th {
  background-color: #f5f5f5;
}

.modal .btn-cancel {
  margin-top: 15px;
  background-color: #f56c6c;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}

.form-group input,
.form-group select {
  width: 100%;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
  box-sizing: border-box;
}

.form-actions {
  margin-top: 20px;
}

.btn-primary {
  background-color: #42b983;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 4px;
  cursor: pointer;
}

.btn-delete {
  background-color: #f56c6c;
  color: white;
  border: none;
  padding: 5px 10px;
  border-radius: 4px;
  cursor: pointer;
}
</style>