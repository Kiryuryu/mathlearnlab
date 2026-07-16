<template>
  <div class="login-overlay" @click.self="auth.closeLogin()">
    <div class="login-box">
      <div class="login-left">
        <div class="login-logo">{{ $t('header.brand') }}</div>
        <div class="login-sub">{{ $t('login.guest') }}</div>
        <button class="guest-btn" @click="auth.closeLogin()">{{ $t('login.guest') }}</button>
      </div>
      <div class="login-right">
        <div class="login-tabs">
          <span :class="['login-tab', { on: auth.loginTab === 'login' }]" @click="auth.loginTab = 'login'">{{ $t('login.login') }}</span>
          <span :class="['login-tab', { on: auth.loginTab === 'register' }]" @click="auth.loginTab = 'register'">{{ $t('login.register') }}</span>
        </div>
        <div v-if="auth.loginTab === 'login'">
          <input v-model="loginUser" :placeholder="$t('login.username')" class="login-inp" @keyup.enter="handleLogin">
          <input v-model="loginPass" type="password" :placeholder="$t('login.password')" class="login-inp" @keyup.enter="handleLogin">
          <p v-if="loginErr" class="login-err">{{ loginErr }}</p>
          <button class="login-btn" @click="handleLogin">{{ $t('login.login') }}</button>
        </div>
        <div v-else>
          <div class="login-field">
            <input v-model="regUser" ref="regUserInput" :placeholder="$t('login.usernamePlaceholder')" class="login-inp" @blur="checkUser" @input="userCheckMsg=''">
            <span v-if="userCheckMsg" class="login-hint" :class="{ err: userCheckErr }">{{ userCheckMsg }}</span>
          </div>
          <input v-model="regEmail" :placeholder="$t('login.emailPlaceholder')" class="login-inp">
          <input v-model="regPass" type="password" :placeholder="$t('login.passwordPlaceholder')" class="login-inp">
          <p v-if="regErr" class="login-err">{{ regErr }}</p>
          <button class="login-btn" @click="handleRegister">{{ $t('login.register') }}</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useI18n } from 'vue-i18n'
import { useAuth } from '@/stores/auth'
const auth = useAuth()
const { t } = useI18n()

const loginUser = ref(''), loginPass = ref(''), loginErr = ref('')
const regUser = ref(''), regEmail = ref(''), regPass = ref(''), regErr = ref('')
const regUserInput = ref(null)
const userCheckMsg = ref('')
const userCheckErr = ref(false)
let checkTimer = null

async function checkUser() {
  const u = regUser.value.trim()
  userCheckMsg.value = ''
  userCheckErr.value = false
  if (u.length < 3) { userCheckMsg.value = t('login.usernameTooShort'); userCheckErr.value = true; return }
  try {
    const r = await fetch(`/api/auth/check-username?username=${encodeURIComponent(u)}`)
    const d = await r.json()
    if (!d.available) {
      userCheckMsg.value = t('login.usernameTaken')
      userCheckErr.value = true
    } else {
      userCheckMsg.value = t('login.usernameAvailable')
      userCheckErr.value = false
    }
  } catch(e) { console.warn('Username check failed', e) }
}

async function handleLogin() {
  if (!loginUser.value || !loginPass.value) { loginErr.value = t('login.fillRequired'); return }
  try { await auth.doLogin(loginUser.value, loginPass.value) } catch(e) { loginErr.value = e.message }
}
async function handleRegister() {
  if (!regUser.value || !regPass.value) { regErr.value = t('login.fillRequired'); return }
  if (regUser.value.length < 3) { regErr.value = t('login.usernameTooShort'); return }
  if (regPass.value.length < 6) { regErr.value = t('login.passwordTooShort'); return }
  try {
    const msg = await auth.doRegister(regUser.value, regPass.value, regEmail.value)
    regErr.value = ''
    regUser.value = ''; regPass.value = ''; regEmail.value = ''
    auth.loginTab = 'login'
    loginErr.value = msg + ' — ' + t('login.pendingApproval')
  } catch(e) { regErr.value = e.message }
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
.login-tab { font-size:15px; color:var(--text-muted); cursor:pointer; padding-bottom:4px; border-bottom:2px solid transparent; transition:all 0.15s; }
.login-tab.on { color:var(--accent); border-bottom-color:var(--accent); font-weight:600; }
.login-inp { width:100%; padding:10px 12px; margin-bottom:10px; border:1px solid var(--border); border-radius:6px; font-size:14px; background:var(--bg-input); color:var(--text-primary); outline:none; }
.login-inp:focus { border-color:var(--accent); }
.login-btn { width:100%; padding:10px; background:var(--accent); color:#fff; border:none; border-radius:6px; font-size:14px; font-weight:600; cursor:pointer; }
.login-btn:hover { opacity:0.9; }
.login-err { font-size:12px; color:var(--accent-error); text-align:center; margin:0 0 6px; }
.login-field { position:relative; }
.login-hint { font-size:11px; display:block; margin:-6px 0 8px; padding-left:2px; }
.login-hint.err { color:var(--accent-error); }
.login-hint:not(.err) { color:var(--accent-correct); }
</style>
