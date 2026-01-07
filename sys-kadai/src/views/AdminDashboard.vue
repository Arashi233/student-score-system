<template>
  <div class="dashboard">
    <h1>管理者ユーザーダッシュボード</h1>
    <p>ようこそ、{{ username }}！（管理者ユーザー）</p>
    
    <div class="functions">
      <div class="function-card">
        <h3>学生管理</h3>
        <button @click="showStudentModal = true">学生追加</button>
        
        <!-- 学生追加モーダル -->
        <div v-if="showStudentModal" class="modal-overlay">
          <div class="modal">
            <h3>学生追加</h3>
            <form @submit.prevent="addStudent">
              <div class="form-group">
                <label>氏名：</label>
                <input v-model="newStudent.name" type="text" required />
              </div>
              <div class="form-group">
                <label>学籍番号：</label>
                <input v-model="newStudent.id" type="text" required />
              </div>
              <div class="form-group">
                <label>性別：</label>
                <select v-model="newStudent.sex" required>
                  <option value="">性別を選択してください</option>
                  <option value="male">男</option>
                  <option value="female">女</option>
                </select>
              </div>
              <div class="form-actions">
                <button type="submit" class="btn-primary">追加</button>
                <button type="button" @click="showStudentModal = false" class="btn-cancel">キャンセル</button>
              </div>
            </form>
          </div>
        </div>
        <button @click="showStudentList = true">学生リスト表示</button>
        
        <!-- 学生リスト表示モーダル -->
        <div v-if="showStudentList" class="modal-overlay">
          <div class="modal">
            <h3>学生リスト</h3>
            <table>
              <thead>
                <tr>
                  <th>学籍番号</th>
                  <th>氏名</th>
                  <th>性別</th>
                  <th>状態</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="student in students" :key="student.id">
                  <td>{{ student.id }}</td>
                  <td>{{ student.name }}</td>
                  <td>{{ student.sex === 'male' ? '男' : '女' }}</td>
                  <td>{{ student.status === 1 ? '在籍' : '他' }}</td>
                </tr>
              </tbody>
            </table>
            <button type="button" @click="showStudentList = false" class="btn-cancel">閉じる</button>
          </div>
        </div>
      </div>
      
      <div class="function-card">
        <h3>成績管理</h3>
        <button @click="showScoreModal = true">成績追加</button>
        <!-- 成績追加モーダル -->
        <div v-if="showScoreModal" class="modal-overlay">
          <div class="modal">
            <h3>成績追加</h3>
            <form @submit.prevent="addScore">
              <div class="form-group">
                <label>学生：</label>
                <select v-model="newScore.student_id" required>
                  <option value="">学生を選択してください</option>
                  <option v-for="student in students" :value="student.id">
                    {{ student.name }} ({{ student.id }})
                  </option>
                </select>
              </div>
              <div class="form-group">
                <label>科目：</label>
                <select v-model="newScore.course_id" required>
                  <option value="">科目を選択してください</option>
                  <option v-for="course in courses" :value="course.id">
                    {{ course.name }}
                  </option>
                </select>
              </div>
              <div class="form-group">
                <label>成績：</label>
                <input v-model.number="newScore.score" type="number" min="0" max="100" required />
              </div>
              <div class="form-actions">
                <button type="submit" class="btn-primary">追加</button>
                <button type="button" @click="showScoreModal = false" class="btn-cancel">キャンセル</button>
              </div>
            </form>
          </div>
        </div>
        <button @click="showScoreList = true">成績表示</button>
        
        <!-- 成績表示モーダル -->
        <div v-if="showScoreList" class="modal-overlay">
          <div class="modal">
            <h3>成績一覧</h3>
            <table>
              <thead>
                <tr>
                  <th>学籍番号</th>
                  <th>学生名</th>
                  <th>科目名</th>
                  <th>点数</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="score in scores" :key="score.id">
                  <td>{{ score.student_id }}</td>
                  <td>{{ score.student_name }}</td>
                  <td>{{ score.course_name }}</td>
                  <td>{{ score.score }}</td>
                </tr>
              </tbody>
            </table>
            <button type="button" @click="showScoreList = false" class="btn-cancel">閉じる</button>
          </div>
        </div>
      </div>
      
      <div class="function-card">
        <h3>科目管理</h3>
        <!-- 科目追加モーダル -->
      <button @click="showCourseModal = true" class="btn-secondary">科目追加</button>
      <div v-if="showCourseModal" class="modal-overlay">
        <div class="modal">
          <h3>科目追加</h3>
          <form @submit.prevent="addCourse">
            <div class="form-group">
              <label>科目名：</label>
              <input v-model="newCourse.name" type="text" required />
            </div>
            <div class="form-actions">
              <button type="submit" class="btn-primary">追加</button>
              <button type="button" @click="showCourseModal = false" class="btn-cancel">キャンセル</button>
            </div>
          </form>
        </div>
      </div>
      <button @click="showCourseList = true">科目表示</button>
      
      <!-- 科目表示モーダル -->
      <div v-if="showCourseList" class="modal-overlay">
        <div class="modal">
          <h3>科目一覧</h3>
          <table>
            <thead>
              <tr>
                <th>科目ID</th>
                <th>科目名</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="course in courses" :key="course.id">
                <td>{{ course.id }}</td>
                <td>{{ course.name }}</td>
              </tr>
            </tbody>
          </table>
          <button type="button" @click="showCourseList = false" class="btn-cancel">閉じる</button>
        </div>
      </div>
      </div>
    </div>
    
    <button @click="logout" class="logout-btn">ログアウト</button>
  </div>
</template>

<script>
import { studentAPI } from '@/services/api'
import { courseAPI } from '@/services/api'
import { scoreAPI } from '@/services/api'

export default {
  data() {
    return {
      username: '',
      showStudentModal: false,
      showStudentList: false,
      showScoreModal: false,
      showScoreList: false,
      showCourseModal: false, 
      showCourseList: false,
      newStudent: { name: '', id: '' ,sex: '',status: 1},
      newCourse: { name: '' },
      newScore: { student_id: '', course_id: '', score: null },
      courses: [], 
      students: [],
      scores: [] // 添加成绩列表
    }
  },
  mounted() {
    const user = JSON.parse(localStorage.getItem('user') || '{}')
    this.username = user.name || ''
    this.loadCourses() // 科目をロード
    this.loadStudents() // 学生をロード
  },
  watch: {
    showStudentList(newVal) {
      if (newVal) this.loadStudents(); // モーダルを開く時に学生リストを更新
    },
    showScoreList(newVal) {
      if (newVal) this.loadScores(); // モーダルを開く時に成績リストを更新
    },
    showCourseList(newVal) {
      if (newVal) this.loadCourses(); // モーダルを開く時に科目リストを更新
    }
  },
  methods: {
    async addStudent() {
      try {
        await studentAPI.createStudent(this.newStudent)
        alert('学生追加成功！')
        this.showStudentModal = false
        this.newStudent = { name: '', id: '' ,sex: ''} // フォームをクリア
        this.loadStudents() // 追加後に学生リストを再ロード
      } catch (error) {
        alert(error.response.data.detail||'学生追加に失敗しました。')
      }
    },
    async addCourse() {
      try {
        await courseAPI.createCourse(this.newCourse)
        alert('科目追加成功！')
        this.showCourseModal = false
        this.newCourse = { name: '' }
        this.loadCourses() // 科目リストを再ロード
      } catch (error) {
        alert(error.response.data.detail||'科目追加に失敗しました。')
      }
    },
    async addScore() {
      try {
        await scoreAPI.createScore(this.newScore)
        alert('成績追加成功！')
        this.showScoreModal = false
        this.newScore = { student_id: '', course_id: '', score: null }
        this.loadScores() // 成績リストを再ロード
      } catch (error) {
        alert(error.response.data.detail||'成績追加に失敗しました。')
      }
    },
    async loadCourses() {
      try {
        this.courses = await courseAPI.getCourses()
      } catch (error) {
        this.courses = []
      }
    },
    async loadStudents() {
      try {
        this.students = await studentAPI.getStudents()
      } catch (error) {
        this.students = []
      }
    },
    async loadScores() {
      try {
        const scores = await scoreAPI.getAllScores();
        // Fetch student and course names for each score
        const scoresWithNames = await Promise.all(scores.map(async (score) => {
          const student = await studentAPI.getStudentById(score.student_id);
          const course = await courseAPI.getCourseById(score.course_id);
          return {
            ...score,
            student_name: student ? student.name : '不明',
            course_name: course ? course.name : '不明'
          };
        }));
        this.scores = scoresWithNames;
      } catch (error) {
        this.scores = [];
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
</style>