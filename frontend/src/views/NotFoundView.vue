<template>
  <div class="not-found">
    <div class="nf-code">404</div>
    <h1>{{ $t('notFound.title') }}</h1>
    <p>{{ $t('notFound.subtitle') }}</p>
    <router-link to="/" class="btn-primary">{{ $t('notFound.back') }}</router-link>
  </div>
</template>

<style scoped>
.not-found { max-width:500px; margin:0 auto; padding:120px 20px; text-align:center; }
.nf-code { font-size:96px; font-weight:800; color:var(--accent); opacity:0.3; line-height:1; }
.not-found h1 { margin:16px 0 8px; }
.not-found p { color:var(--text-secondary); margin-bottom:32px; }
.btn-primary { display:inline-block; padding:10px 28px; background:var(--accent); color:#fff; border:none; border-radius:6px; text-decoration:none; cursor:pointer; font-size:15px; }
</style>
