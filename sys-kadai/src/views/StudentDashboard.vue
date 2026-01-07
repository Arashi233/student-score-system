<template>
  <div class="dashboard">
    <h1>学生成績照会システム</h1>
    <p>ようこそ、{{ username }}！</p>
    
    <div class="search-section">
      <h2>成績照会</h2>
      <div class="search-form">
        <select v-model="queryType" class="query-type-select">
          <option value="all">すべて</option>
          <option value="course_name">科目</option>
          <option value="student_name">氏名</option>
          <option value="student_id">学籍番号</option>
        </select>
        <input
            v-model="searchQuery"
            type="text"
            placeholder="照会キーワードを入力してください..."
            @keyup.enter="searchScores"
          />
        <div class="input-with-clear">
          <button
            v-if="searchQuery"
            @click="clearSearch"
            class="clear-btn"
            aria-label="検索クリア"
          >
            ×
          </button>
        </div>
        <button @click="searchScores">照会</button>
      </div>
      
      <div v-if="scores.length > 0" class="results">
        <h3>照会結果</h3>
        <table>
          <thead>
            <tr>
              <th>学籍番号</th>
              <th>学生氏名</th>
              <th>科目</th>
              <th>成績</th>
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
      </div>
    </div>
    
    <button @click="logout" class="logout-btn">ログアウト</button>
  </div>
</template>

<script>
import { scoreAPI } from '../services/api'
import { studentAPI } from '../services/api'
import { courseAPI } from '../services/api'

export default {
  data() {
    return {
      username: '',
      searchQuery: '',
      queryType: 'all', 
      scores: [],
      students: [] 
    }
  },
  mounted() {
    const user = JSON.parse(localStorage.getItem('user') || '{}')
    console.log('Logged in user:', user)
    this.username = user.name || user.username || ''
    // ページロード時にすべてのデータを表示
    this.searchScores()
  },
  methods: {    
    async searchScores() {
      try {
        let studentId = null
        let courseId = null
        if (this.queryType === 'all') {
          const response = await scoreAPI.getAllScores()
          for (const score of response) {
            // 学生名をstudentAPIから取得
            const student = await studentAPI.getStudentById(score.student_id)
            score.student_name = student ? student.name : '不明'
            // 科目名をcourseAPIから取得
            const course = await courseAPI.getCourseById(score.course_id);
            score.course_name = course ? course.name : '不明';
          }
          
        }
        if (this.queryType === 'student_id' && this.searchQuery) {
          const student = await studentAPI.getStudentById(Number(this.searchQuery))
          if (!student) {
            this.scores = []
            return
          }
          studentId = student.id
        }

        else if (this.queryType === 'student_name' && this.searchQuery) {
          const student = await studentAPI.getStudentByName(this.searchQuery)
          if (!student) {
            this.scores = []
            return
          }
          studentId = student.id
        }
        else if (this.queryType === 'course_name' && this.searchQuery) {
          const course = await courseAPI.getCourseByName(this.searchQuery)
          if (!course) {
            this.scores = []
            return
          }
          courseId = course.id
        }
        else {
          const response = await scoreAPI.getAllScores()
          for (const score of response) {
            // 学生名をstudentAPIから取得
            const student = await studentAPI.getStudentById(score.student_id)
            score.student_name = student ? student.name : '不明'
            // 科目名をcourseAPIから取得
            const course = await courseAPI.getCourseById(score.course_id);
            score.course_name = course ? course.name : '不明';
          }
          this.scores = response;
          return;
        }
        const response = await scoreAPI.getScores(studentId, courseId)

        console.log(response)
        for (const score of response) {
          // 学生名をstudentAPIから取得
          const student = await studentAPI.getStudentById(score.student_id)
          score.student_name = student ? student.name : '不明'
          // 科目名をcourseAPIから取得
          const course = await courseAPI.getCourseById(score.course_id);
          score.course_name = course ? course.name : '不明';
        }
        this.scores = response;
      } catch (error) {
        console.error('照会1失敗:', error);
        this.scores = []; // エラー時結果をクリア
      }
    },

    clearSearch() {
      this.searchQuery = '';
      this.searchScores(); // すべてのデータを再読み込み
    },
    logout() {
      localStorage.clear()
      this.$router.replace('/')
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

.search-section {
  margin: 30px 0;
}

.search-form {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}

.search-form input {
  flex: 1;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.search-form button {
  padding: 10px 20px;
  background-color: #42b983;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
}

th, td {
  border: 1px solid #ddd;
  padding: 12px;
  text-align: left;
}

th {
  background-color: #f5f5f5;
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