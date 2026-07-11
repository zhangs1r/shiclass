/* ShiClass 课程交互脚本 */

window.lessonKit = {
  answer: function(btn, quizId) {
    const feedback = document.getElementById(quizId);
    if (!feedback) return;
    
    const isCorrect = btn.dataset.correct === 'yes';
    const explanation = btn.dataset.explanation || '';
    
    // Reset all buttons in this quiz
    const options = btn.closest('.quiz-options');
    if (options) {
      options.querySelectorAll('button').forEach(b => {
        b.classList.remove('correct', 'wrong');
      });
    }
    
    if (isCorrect) {
      btn.classList.add('correct');
      feedback.className = 'quiz-feedback show correct';
      feedback.innerHTML = '✅ 正确！' + (explanation ? ' ' + explanation : '');
    } else {
      btn.classList.add('wrong');
      feedback.className = 'quiz-feedback show wrong';
      feedback.innerHTML = '❌ ' + (explanation || '再想想？');
    }
  }
};
