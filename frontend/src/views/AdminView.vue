<template>
  <div class="admin-page">
    <h1>{{ $t('admin.title') }}</h1>
    <p class="sub">{{ $t('admin.subtitle') }}</p>
    <div v-if="!authenticated" class="login-box">
      <input v-model="secret" type="password" :placeholder="$t('admin.secretPlaceholder')" class="inp" @keyup.enter="auth">
      <button @click="auth" class="btn-primary">{{ $t('admin.enter') }}</button>
    </div>
    <div v-else>
      <div class="tabs">
        <button :class="{ active: filter === 'pending' }" @click="filter='pending';load()">{{ $t('admin.pending') }}</button>
        <button :class="{ active: filter === 'active' }" @click="filter='active';load()">{{ $t('admin.approved') }}</button>
        <button :class="{ active: filter === 'rejected' }" @click="filter='rejected';load()">{{ $t('admin.rejected') }}</button>
        <button :class="{ active: filter === 'all' }" @click="filter='all';load()">{{ $t('admin.all') }}</button>
      </div>
      <table v-if="users.length">
        <thead><tr><th>{{ $t('admin.colUsername') }}</th><th>{{ $t('admin.colEmail') }}</th><th>{{ $t('admin.colStatus') }}</th><th>{{ $t('admin.colTime') }}</th><th>{{ $t('admin.colActions') }}</th></tr></thead>
        <tbody>
          <tr v-for="u in users" :key="u.id">
            <td>{{ u.username }}</td>
            <td>{{ u.email }}</td>
            <td :class="'status-'+u.status">{{ statusLabel(u.status) }}</td>
            <td>{{ formatDate(u.created_at) }}</td>
            <td class="actions">
              <button v-if="u.status==='pending'" @click="approve(u.id)" class="btn-approve">{{ $t('admin.approve') }}</button>
              <button v-if="u.status==='pending'" @click="reject(u.id)" class="btn-reject">{{ $t('admin.reject') }}</button>
              <button v-if="u.status==='rejected'" @click="approve(u.id)" class="btn-approve">{{ $t('admin.reattach') }}</button>
            </td>
          </tr>
        </tbody>
      </table>
      <p v-else class="empty">{{ $t('admin.empty') }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useI18n } from 'vue-i18n'
import { useToast } from '@/utils/toast'
const { t, locale } = useI18n()
const { show: showToast } = useToast()

const secret = ref('')
const authenticated = ref(false)
const filter = ref('pending')
const users = ref([])

function auth() {
  load()
}
function statusLabel(s) {
  return t('admin.status' + s.charAt(0).toUpperCase() + s.slice(1))
}
function formatDate(d) { return d ? new Date(d).toLocaleDateString(locale.value === 'en' ? 'en-US' : 'zh-CN') : '' }

async function load() {
  try {
    const r = await fetch(`/api/admin/users?secret=${secret.value}&status=${filter.value}`)
    if (!r.ok) { showToast(t('admin.loadFail')); return }
    const d = await r.json()
    users.value = d.users || []
    authenticated.value = true
  } catch(e) { console.warn('Failed to load users', e); showToast(t('admin.loadFail')) }
}

async function approve(id) {
  try {
    const r = await fetch(`/api/admin/users/${id}/approve?secret=${secret.value}`, { method: 'POST' })
    if (!r.ok) { showToast(t('admin.actionFail')); return }
    load()
  } catch(e) { console.warn('Failed to approve user', e); showToast(t('admin.actionFail')) }
}

async function reject(id) {
  try {
    const r = await fetch(`/api/admin/users/${id}/reject?secret=${secret.value}`, { method: 'POST' })
    if (!r.ok) { showToast(t('admin.actionFail')); return }
    load()
  } catch(e) { console.warn('Failed to reject user', e); showToast(t('admin.actionFail')) }
}
</script>

<style scoped>
.admin-page { max-width:900px; margin:0 auto; padding:32px 20px 64px; }
.admin-page h1 { text-align:center; }
.sub { text-align:center; color:var(--text-secondary); }
.login-box { max-width:300px; margin:40px auto; text-align:center; }
.inp { width:100%; padding:10px; border:1px solid var(--border); border-radius:6px; font-size:14px; margin-bottom:8px; background:var(--bg-input); color:var(--text-primary); }
.inp:focus { border-color:var(--accent); outline:none; }
.btn-primary { padding:10px 24px; background:var(--accent); color:#fff; border:none; border-radius:6px; cursor:pointer; }
.tabs { display:flex; gap:8px; margin:16px 0; }
.tabs button { padding:6px 16px; border:1px solid var(--border); border-radius:20px; background:var(--bg-card); color:var(--text-secondary); cursor:pointer; font-size:13px; }
.tabs button.active { background:var(--accent); color:#fff; }
table { width:100%; border-collapse:collapse; }
th, td { padding:10px 14px; text-align:left; border-bottom:1px solid var(--border); }
th { font-size:12px; color:var(--text-muted); }
.status-pending { color:var(--accent-warm); font-weight:600; }
.status-active { color:var(--accent-correct); }
.status-rejected { color:var(--accent-error); }
.actions { display:flex; gap:6px; }
.btn-approve { padding:4px 12px; background:var(--accent-correct); color:#fff; border:none; border-radius:4px; cursor:pointer; font-size:12px; }
.btn-reject { padding:4px 12px; background:var(--accent-error); color:#fff; border:none; border-radius:4px; cursor:pointer; font-size:12px; }
.empty { text-align:center; padding:40px; color:var(--text-muted); }
</style>
