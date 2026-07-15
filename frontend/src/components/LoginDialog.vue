<template>
  <div class="login-overlay" @click.self="auth.closeLogin()">
    <div class="login-box">
      <div class="login-left">
        <div class="login-logo">数学博物馆</div>
        <div class="login-sub">记录学习轨迹<br>解锁完整功能</div>
        <button class="guest-btn" @click="auth.closeLogin()">游客浏览</button>
      </div>
      <div class="login-right">
        <div class="login-tabs">
          <span :class="['login-tab', { on: auth.loginTab === 'login' }]" @click="auth.loginTab = 'login'">登录</span>
          <span :class="['login-tab', { on: auth.loginTab === 'register' }]" @click="auth.loginTab = 'register'">注册</span>
        </div>
        <div v-if="auth.loginTab === 'login'">
          <input v-model="loginUser" placeholder="用户名" class="login-inp" @keyup.enter="handleLogin">
          <input v-model="loginPass" type="password" placeholder="密码" class="login-inp" @keyup.enter="handleLogin">
          <p v-if="loginErr" class="login-err">{{ loginErr }}</p>
          <button class="login-btn" @click="handleLogin">登录</button>
        </div>
        <div v-else>
          <input v-model="regUser" placeholder="用户名（至少3位）" class="login-inp">
          <input v-model="regEmail" placeholder="邮箱（选填）" class="login-inp">
          <input v-model="regPass" type="password" placeholder="密码（至少6位）" class="login-inp">
          <select v-model="regModel" class="login-inp" style="font-family:monospace;font-size:13px">
            <option value="deepseek-chat">DeepSeek V4 Pro</option>
            <option value="deepseek-chat">DeepSeek V4 Flash</option>
            <option value="deepseek-reasoner">DeepSeek R1</option>
          </select>
          <input v-model="regKey" type="password" placeholder="DeepSeek API Key（sk-...）" class="login-inp" style="font-family:monospace;font-size:12px">
          <p v-if="regErr" class="login-err">{{ regErr }}</p>
          <button class="login-btn" @click="handleRegister">注册</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useAuth } from '@/stores/auth'
const auth = useAuth()

const loginUser = ref(''), loginPass = ref(''), loginErr = ref('')
const regUser = ref(''), regEmail = ref(''), regPass = ref(''), regModel = ref('deepseek-chat'), regKey = ref(''), regErr = ref('')

async function handleLogin() {
  if (!loginUser.value || !loginPass.value) { loginErr.value = '请填写用户名和密码'; return }
  try { await auth.doLogin(loginUser.value, loginPass.value) } catch(e) { loginErr.value = e.message }
}
async function handleRegister() {
  if (!regUser.value || !regPass.value) { regErr.value = '请填写用户名和密码'; return }
  if (regUser.value.length < 3) { regErr.value = '用户名至少3位'; return }
  if (regPass.value.length < 6) { regErr.value = '密码至少6位'; return }
  if (!regKey.value) { regErr.value = '请输入 DeepSeek API Key'; return }
  try { await auth.doRegister(regUser.value, regPass.value, regEmail.value, regModel.value, regKey.value) } catch(e) { regErr.value = e.message }
}
</script>

<style scoped>
.login-overlay { position:fixed; inset:0; background:rgba(0,0,0,0.4); z-index:999; display:flex; align-items:center; justify-content:center; }
.login-box { display:flex; background:var(--bg-card,#fff); border-radius:12px; overflow:hidden; box-shadow:0 8px 40px rgba(0,0,0,0.15); width:480px; max-width:92vw; }
.login-left { width:160px; background:linear-gradient(160deg,#1e2935,#3a5a7c); color:#fff; padding:40px 24px; display:flex; flex-direction:column; justify-content:center; align-items:center; text-align:center; flex-shrink:0; }
.login-logo { font-size:18px; font-weight:700; letter-spacing:2px; margin-bottom:8px; }
.login-sub { font-size:12px; opacity:0.7; line-height:1.6; }
.guest-btn { background:none; border:1px solid rgba(255,255,255,0.3); color:rgba(255,255,255,0.7); padding:6px 14px; border-radius:6px; font-size:12px; cursor:pointer; margin-top:16px; }
.login-right { flex:1; padding:32px 28px; }
.login-tabs { display:flex; gap:20px; margin-bottom:24px; }
.login-tab { font-size:15px; color:#889098; cursor:pointer; padding-bottom:4px; border-bottom:2px solid transparent; transition:all 0.15s; }
.login-tab.on { color:#4a6a8a; border-bottom-color:#4a6a8a; font-weight:600; }
.login-inp { width:100%; padding:10px 12px; margin-bottom:10px; border:1px solid #e2e5e8; border-radius:6px; font-size:14px; background:#f7f8f9; outline:none; }
.login-inp:focus { border-color:#4a6a8a; }
.login-btn { width:100%; padding:10px; background:#4a6a8a; color:#fff; border:none; border-radius:6px; font-size:14px; font-weight:600; cursor:pointer; }
.login-btn:hover { opacity:0.9; }
.login-err { font-size:12px; color:#a45050; text-align:center; margin:0 0 6px; }
</style>
