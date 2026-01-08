import axios from 'axios'

// 创建axios实例
const api = axios.create({
  baseURL: 'http://localhost:8000/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// 响应拦截器
api.interceptors.response.use(
  response => response.data,
  error => {
    const status = error.response?.status
    const url = error.config?.url || ''

    if (status === 401 && url.includes('/login')) {
      return Promise.reject(error)
    }

    if (status === 401) {
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      window.location.href = '/'
    }

    return Promise.reject(error)
  }
)

export const authAPI = {
  login: (username, password) => api.post('/login', { username, password }),
  getusers: () => api.get('/users'),
  create_user: (name, pwd, type) => api.post('/users', { name, pwd, type }),
  getMe: () => api.get('/users/me'),
  updateUserType: (id, type) => api.put(`/users`, {id, type}),
  deleteUser: (id) => api.delete(`/users/${id}`)
}

export const studentAPI = {
  getStudents: () => api.get('/students'),
  getStudentById: (id) => api.get(`/studentsById/${id}`),
  getStudentByName: (name) => api.get(`/studentsByName/${name}`),
  createStudent: (student) => api.post('/students', student),
  updateStudent: (id, student) => api.put(`/students/${id}`, student)
}

export const courseAPI = {
  getCourses: () => api.get('/courses'),
  getCourseById: (id) => api.get(`/courseById/${id}`),
  getCourseByName: (name) => api.get(`/courseByName/${name}`),
  createCourse: (course) => api.post('/courses', course),
  updateCourse: (id, course) => api.put(`/courses/${id}`, course)
}

export const scoreAPI = {
  getScores: (studentId, courseId) => api.get('/scores', { 
    params: { student_id: studentId, course_id: courseId } 
  }),
  getAllScores: () => api.get('/scores'),
  createScore: (score) => api.post('/scores', score),
  updateScore: (id, score) => api.put(`/scores/${id}`, score)
}

export default api