<template>
  <div class="reset-page">
    <div class="reset-card">
      <h1>{{ $t('reset.title') }}</h1>
      <p class="sub">{{ $t('reset.subtitle') }}</p>

      <div v-if="!done" class="reset-form">
        <div class="field">
          <input v-model="pass1" type="password" :placeholder="$t('reset.newPassword')" class="inp" @keyup.enter="submit">
        </div>
        <div class="field">
          <input v-model="pass2" type="password" :placeholder="$t('reset.confirmPassword')" class="inp" @keyup.enter="submit">
        </div>
        <p v-if="err" class="err">{{ err }}</p>
        <button class="btn-primary" :disabled="sending" @click="submit">{{ sending ? '…' : $t('reset.submit') }}</button>
      </div>

      <div v-else class="reset-done">
        <p class="ok">{{ $t('reset.success') }}</p>
        <router-link to="/" class="btn-primary">{{ $t('reset.goLogin') }}</router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { useAuth } from '@/stores/auth'

const route = useRoute()
const { t } = useI18n()
const auth = useAuth()

const token = ref(route.query.token || '')
const pass1 = ref('')
const pass2 = ref('')
const err = ref('')
const sending = ref(false)
const done = ref(false)

onMounted(() => {
  if (!token.value) err.value = t('reset.missingToken')
})

async function submit() {
  if (!token.value) { err.value = t('reset.missingToken'); return }
  if (pass1.value.length < 6) { err.value = t('reset.tooShort'); return }
  if (pass1.value !== pass2.value) { err.value = t('reset.mismatch'); return }
  sending.value = true
  err.value = ''
  try {
    const r = await fetch('/api/auth/reset-password', {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ token: token.value, password: pass1.value }),
    })
    const d = await r.json().catch(() => ({}))
    if (!r.ok) { err.value = d.detail || t('reset.fail'); return }
    done.value = true
    // If a stale session exists, drop it so the user logs in fresh.
    auth.logout()
  } catch (e) {
    err.value = t('reset.fail')
  } finally {
    sending.value = false
  }
}
</script>

<style scoped>
.reset-page { max-width:420px; margin:0 auto; padding:80px 20px; }
.reset-card { background:var(--bg-card); border:1px solid var(--border); border-radius:14px; padding:36px 32px; text-align:center; box-shadow:var(--shadow-elevated); }
.reset-card h1 { margin:0 0 6px; font-family:var(--font-heading); font-size:22px; }
.sub { color:var(--text-secondary); font-size:13px; margin:0 0 24px; }
.field { margin-bottom:12px; }
.inp { width:100%; padding:11px 14px; border:1px solid var(--border); border-radius:10px; font-size:14px; background:var(--bg-input); color:var(--text-primary); outline:none; box-sizing:border-box; }
.inp:focus { border-color:var(--accent); }
.err { font-size:12px; color:var(--accent-error); margin:0 0 8px; }
.ok { color:var(--accent-correct); font-size:14px; margin:0 0 20px; }
.btn-primary { display:inline-block; width:100%; padding:12px; background:var(--accent); color:#fff; border:none; border-radius:10px; font-size:15px; font-weight:600; cursor:pointer; text-decoration:none; box-sizing:border-box; }
.btn-primary:disabled { opacity:0.5; cursor:not-allowed; }
</style>
