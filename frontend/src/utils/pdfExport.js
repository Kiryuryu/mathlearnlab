import { jsPDF } from 'jspdf'

export function exportProblemToPDF(problem, solution = '') {
  const doc = new jsPDF()
  const pageWidth = doc.internal.pageSize.getWidth()
  let y = 20

  doc.setFontSize(16)
  doc.text('Practice Problem', 10, y)
  y += 12

  doc.setFontSize(10)
  doc.setTextColor(100)
  doc.text(`Topic: ${problem.topic || ''}  |  Difficulty: ${problem.difficulty || ''}`, 10, y)
  y += 10

  doc.setTextColor(0)
  doc.setFontSize(12)
  const statementLines = doc.splitTextToSize(problem.problem_statement || '', pageWidth - 20)
  doc.text(statementLines, 10, y)
  y += statementLines.length * 6 + 10

  if (solution) {
    doc.setFontSize(12)
    doc.text('Solution:', 10, y)
    y += 8
    const solLines = doc.splitTextToSize(solution, pageWidth - 20)
    doc.text(solLines, 10, y)
  }

  doc.save('practice-problem.pdf')
}
