import { jsPDF } from 'jspdf'

export function exportProblemToPDF(problem, solution = '', lang = 'en') {
  const doc = new jsPDF()
  const pageWidth = doc.internal.pageSize.getWidth()
  let y = 20

  const labels = lang === 'zh'
    ? { title: '练习题', topic: '主题', difficulty: '难度', solution: '解答' }
    : { title: 'Practice Problem', topic: 'Topic', difficulty: 'Difficulty', solution: 'Solution' }

  doc.setFontSize(16)
  doc.text(labels.title, 10, y)
  y += 12

  doc.setFontSize(10)
  doc.setTextColor(100)
  doc.text(`${labels.topic}: ${problem.topic || ''}  |  ${labels.difficulty}: ${problem.difficulty || ''}`, 10, y)
  y += 10

  doc.setTextColor(0)
  doc.setFontSize(12)
  const statementLines = doc.splitTextToSize(problem.problem_statement || '', pageWidth - 20)
  doc.text(statementLines, 10, y)
  y += statementLines.length * 6 + 10

  if (solution) {
    doc.setFontSize(12)
    doc.text(labels.solution + ':', 10, y)
    y += 8
    const solLines = doc.splitTextToSize(solution, pageWidth - 20)
    doc.text(solLines, 10, y)
  }

  doc.save('practice-problem.pdf')
}
