<template>
  <BaseModal panel-class="login-panel" @close="auth.closeLogin()">
    <div class="login-left">
      <div class="brand-mark">
        <svg width="30" height="30" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M4 19V5"/><path d="M4 19h16"/><path d="M9 19c0-5 3-9 6-11"/><path d="M14 19c0-4 1.5-7 3-9"/></svg>
      </div>
      <div class="login-logo">{{ $t('header.brand') }}</div>
      <div class="login-sub">{{ $t('header.subtitle') }}</div>
      <div class="login-guest">{{ $t('login.guest') }}</div>
      <button class="guest-btn" @click="auth.closeLogin()">→ {{ $t('login.guest') }}</button>
    </div>
    <div class="login-right">
      <div class="login-tabs">
        <span :class="['login-tab', { on: auth.loginTab === 'login' }]" @click="auth.loginTab = 'login'">{{ $t('login.login') }}</span>
        <span :class="['login-tab', { on: auth.loginTab === 'register' }]" @click="auth.loginTab = 'register'">{{ $t('login.register') }}</span>
      </div>
      <div v-if="auth.loginTab === 'login'">
        <div class="field">
          <input v-model="loginUser" :placeholder="$t('login.username')" class="login-inp" @keyup.enter="handleLogin">
        </div>
        <div class="field">
          <input v-model="loginPass" type="password" :placeholder="$t('login.password')" class="login-inp" @keyup.enter="handleLogin">
        </div>
        <p v-if="loginErr" class="login-err">{{ loginErr }}</p>
        <button class="login-btn" @click="handleLogin">{{ $t('login.login') }}</button>
      </div>
      <div v-else>
        <div class="field">
          <input v-model="regUser" ref="regUserInput" :placeholder="$t('login.usernamePlaceholder')" class="login-inp" @blur="checkUser" @input="userCheckMsg=''">
          <span v-if="userCheckMsg" class="login-hint" :class="{ err: userCheckErr }">{{ userCheckMsg }}</span>
        </div>
        <div class="field">
          <input v-model="regEmail" :placeholder="$t('login.emailPlaceholder')" class="login-inp">
        </div>
        <div class="field">
          <input v-model="regPass" type="password" :placeholder="$t('login.passwordPlaceholder')" class="login-inp">
        </div>
        <p v-if="regErr" class="login-err">{{ regErr }}</p>
        <button class="login-btn" @click="handleRegister">{{ $t('login.register') }}</button>
      </div>
    </div>
  </BaseModal>
</template>

<script setup>
import { ref } from 'vue'
import { useI18n } from 'vue-i18n'
import { useAuth } from '@/stores/auth'
import BaseModal from '@/components/BaseModal.vue'
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
.login-panel { display:flex; overflow:hidden; width:580px !important; max-width:94vw; border-radius:16px; }
.login-left {
  width:210px; flex-shrink:0; min-width:210px;
  background:linear-gradient(165deg,#1a2530 0%,#22344a 55%,#3a5a7c 100%);
  color:#fff; padding:40px 26px;
  display:flex; flex-direction:column; justify-content:center; align-items:center; text-align:center;
  position:relative;
}
.login-left::before {
  content:''; position:absolute; inset:0; pointer-events:none;
  background:radial-gradient(circle at 20% 10%, rgba(255,255,255,0.08), transparent 60%);
}
.brand-mark {
  width:52px; height:52px; border-radius:14px;
  background:rgba(255,255,255,0.12); border:1px solid rgba(255,255,255,0.18);
  display:flex; align-items:center; justify-content:center;
  margin-bottom:16px; box-shadow:0 4px 16px rgba(0,0,0,0.2);
}
.login-logo { font-size:17px; font-weight:700; letter-spacing:2px; margin-bottom:6px; font-family:var(--font-heading); }
.login-sub { font-size:11px; opacity:0.65; line-height:1.7; }
.login-guest { font-size:11px; opacity:0.45; margin-top:24px; }
.guest-btn {
  margin-top:8px; background:none; border:1px solid rgba(255,255,255,0.25);
  color:rgba(255,255,255,0.8); padding:6px 16px; border-radius:20px;
  font-size:12px; cursor:pointer; transition:all 0.2s;
}
.guest-btn:hover { background:rgba(255,255,255,0.12); color:#fff; border-color:rgba(255,255,255,0.4); }
.login-right { flex:1; min-width:0; padding:36px 38px; }
.login-tabs { display:flex; gap:24px; margin-bottom:28px; }
.login-tab {
  font-size:14px; color:var(--text-muted); cursor:pointer; padding-bottom:6px;
  border-bottom:2px solid transparent; transition:all 0.15s; letter-spacing:0.5px;
}
.login-tab.on { color:var(--accent); border-bottom-color:var(--accent); font-weight:600; }
.field { margin-bottom:14px; position:relative; }
.login-inp {
  width:100%; padding:11px 14px; border:1px solid var(--border); border-radius:10px;
  font-size:14px; background:var(--bg-input); color:var(--text-primary); outline:none;
  transition:border-color 0.15s, box-shadow 0.15s;
}
.login-inp:focus { border-color:var(--accent); box-shadow:0 0 0 3px rgba(74,106,138,0.12); }
.login-btn {
  width:100%; padding:12px; margin-top:6px;
  background:var(--accent); color:#fff; border:none; border-radius:10px;
  font-size:15px; font-weight:600; cursor:pointer; letter-spacing:1px;
  transition:opacity 0.15s, transform 0.1s;
}
.login-btn:hover { opacity:0.92; transform:translateY(-1px); }
.login-btn:active { transform:translateY(0); }
.login-err { font-size:12px; color:var(--accent-error); text-align:center; margin:0 0 8px; }
.login-hint { font-size:11px; display:block; margin:4px 0 0; padding-left:2px; }
.login-hint.err { color:var(--accent-error); }
.login-hint:not(.err) { color:var(--accent-correct); }
@media(max-width:520px) {
  .login-panel { flex-direction:column; }
  .login-left { width:100%; min-width:0; padding:22px 18px; flex-direction:row; gap:14px; justify-content:flex-start; }
  .login-left::before { display:none; }
  .brand-mark { width:40px; height:40px; margin-bottom:0; flex-shrink:0; }
  .login-logo { margin-bottom:0; font-size:15px; }
  .login-sub, .login-guest { display:none; }
  .guest-btn { margin-top:0; margin-left:auto; padding:5px 14px; }
  .login-right { padding:24px 20px; }
}
</style>
