<template>
  <router-link :to="to" class="card" :style="{ background: bg }">
    <div class="card-body">
      <h2>{{ title }}</h2>
      <p>{{ desc }}</p>
      <div class="card-meta">{{ meta }}</div>
    </div>
  </router-link>
</template>

<script setup>
defineProps({ to: String, title: String, desc: String, meta: String, bg: String })
</script>

<style scoped>
.card { display:block; border-radius:12px; overflow:hidden; color:#fff; text-decoration:none; min-height:220px; display:flex; flex-direction:column; justify-content:flex-end; transition:transform 0.25s,box-shadow 0.25s; box-shadow:0 1px 2px rgba(26,29,34,0.04); }
.card:hover { transform:translateY(-4px) scale(1.01); box-shadow:0 4px 10px rgba(26,29,34,0.05),0 8px 30px rgba(0,0,0,0.08); text-decoration:none; color:#fff; }
.card-body { padding:24px; background:linear-gradient(transparent,rgba(0,0,0,0.55)); color:#fff; }
.card-body h2 { font-size:20px; margin:0 0 8px; color:#fff; }
.card-body p { font-size:13px; opacity:0.9; margin:0; color:#fff; }
.card-meta { font-size:11px; opacity:0.7; margin-top:8px; color:#fff; }
</style>
