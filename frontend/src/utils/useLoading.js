// Composable: loading state with a wrapper that toggles true/false around an async fn.
import { ref } from 'vue'

export function useLoading(initial = false) {
  const loading = ref(initial)

  async function run(fn) {
    loading.value = true
    try {
      return await fn()
    } finally {
      loading.value = false
    }
  }

  return { loading, run }
}
