<template>
  <div class="admin-page">
    <h1>用户审核</h1>
    <p class="sub">管理用户注册申请</p>
    <div v-if="!authenticated" class="login-box">
      <input v-model="secret" type="password" placeholder="管理密钥" class="inp" @keyup.enter="auth">
      <button @click="auth" class="btn-primary">进入</button>
    </div>
    <div v-else>
      <div class="tabs">
        <button :class="{ active: filter === 'pending' }" @click="filter='pending';load()">待审核</button>
        <button :class="{ active: filter === 'active' }" @click="filter='active';load()">已通过</button>
        <button :class="{ active: filter === 'rejected' }" @click="filter='rejected';load()">已拒绝</button>
        <button :class="{ active: filter === 'all' }" @click="filter='all';load()">全部</button>
      </div>
      <table v-if="users.length">
        <thead><tr><th>用户名</th><th>邮箱</th><th>状态</th><th>时间</th><th>操作</th></tr></thead>
        <tbody>
          <tr v-for="u in users" :key="u.id">
            <td>{{ u.username }}</td>
            <td>{{ u.email }}</td>
            <td :class="'status-'+u.status">{{ statusLabel(u.status) }}</td>
            <td>{{ formatDate(u.created_at) }}</td>
            <td class="actions">
              <button v-if="u.status==='pending'" @click="approve(u.id)" class="btn-approve">通过</button>
              <button v-if="u.status==='pending'" @click="reject(u.id)" class="btn-reject">拒绝</button>
              <button v-if="u.status==='rejected'" @click="approve(u.id)" class="btn-approve">重新通过</button>
            </td>
          </tr>
        </tbody>
      </table>
      <p v-else class="empty">暂无数据</p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const secret = ref('')
const authenticated = ref(false)
const filter = ref('pending')
const users = ref([])

function auth() {
  authenticated.value = true
  load()
}
function statusLabel(s) { return { pending: '待审核', active: '已通过', rejected: '已拒绝' }[s] || s }
function formatDate(d) { return d ? new Date(d).toLocaleDateString('zh-CN') : '' }

async function load() {
  try {
    const r = await fetch(`/api/admin/users?secret=${secret.value}&status=${filter.value}`)
    users.value = (await r.json()).users || []
  } catch(e) {}
}

async function approve(id) {
  await fetch(`/api/admin/users/${id}/approve?secret=${secret.value}`, { method: 'POST' })
  load()
}

async function reject(id) {
  await fetch(`/api/admin/users/${id}/reject?secret=${secret.value}`, { method: 'POST' })
  load()
}
</script>

<style scoped>
.admin-page { max-width:900px; margin:0 auto; padding:32px 20px 64px; }
.admin-page h1 { text-align:center; }
.sub { text-align:center; color:#505560; }
.login-box { max-width:300px; margin:40px auto; text-align:center; }
.inp { width:100%; padding:10px; border:1px solid #e2e5e8; border-radius:6px; font-size:14px; margin-bottom:8px; }
.btn-primary { padding:10px 24px; background:#4a6a8a; color:#fff; border:none; border-radius:6px; cursor:pointer; }
.tabs { display:flex; gap:8px; margin:16px 0; }
.tabs button { padding:6px 16px; border:1px solid #e2e5e8; border-radius:20px; background:#fff; color:#505560; cursor:pointer; font-size:13px; }
.tabs button.active { background:#4a6a8a; color:#fff; }
table { width:100%; border-collapse:collapse; }
th, td { padding:10px 14px; text-align:left; border-bottom:1px solid #e2e5e8; }
th { font-size:12px; color:#889098; }
.status-pending { color:#6b5e4a; font-weight:600; }
.status-active { color:#3d6b4f; }
.status-rejected { color:#a45050; }
.actions { display:flex; gap:6px; }
.btn-approve { padding:4px 12px; background:#3d6b4f; color:#fff; border:none; border-radius:4px; cursor:pointer; font-size:12px; }
.btn-reject { padding:4px 12px; background:#a45050; color:#fff; border:none; border-radius:4px; cursor:pointer; font-size:12px; }
.empty { text-align:center; padding:40px; color:#889098; }
</style>
