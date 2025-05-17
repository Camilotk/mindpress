/**
 * quiz.js - Versão robusta para quizzes de múltipla escolha
 * Resolve problemas com botão ausente e opções não selecionáveis
 */
(function() {
  // Espera a página estar completamente carregada antes de processar os quizzes
  window.addEventListener('load', function() {
    console.log('Quiz.js inicializado');
    
    // Processa todos os quizzes de múltipla escolha
    const quizzes = document.querySelectorAll('.quiz[data-type="single"]');
    console.log('Número de quizzes encontrados:', quizzes.length);
    
    // Para cada quiz encontrado
    quizzes.forEach(function(quiz, quizIndex) {
      console.log('Processando quiz #' + (quizIndex + 1));
      
      // Garante que a explicação esteja oculta inicialmente
      const explanation = quiz.querySelector('.explanation');
      if (explanation) {
        explanation.style.display = 'none';
      }
      
      // Verifica se existe um botão de submissão e adiciona se não existir
      let submitButton = quiz.querySelector('.quiz-submit');
      if (!submitButton) {
        console.log('Botão não encontrado, criando novo botão');
        
        // Cria novo botão
        submitButton = document.createElement('button');
        submitButton.className = 'quiz-submit';
        submitButton.textContent = 'Enviar';
        
        // Adiciona o botão ao final do quiz
        quiz.appendChild(submitButton);
      }
      
      // Obtém todas as opções do quiz
      const options = quiz.querySelectorAll('li');
      console.log('Opções encontradas:', options.length);
      
      // Variável para rastrear qual opção está selecionada
      let selectedOption = null;
      
      // Adiciona números/letras às opções e configura o comportamento de clique
      options.forEach(function(option, index) {
        // Adiciona letras (a, b, c, ...) se não existirem
        if (!option.querySelector('strong')) {
          const letter = String.fromCharCode(97 + index);
          option.innerHTML = '<strong>' + letter + ')</strong> ' + option.innerHTML;
        }
        
        // Adiciona manipulador de evento para clicar na opção
        option.onclick = function() {
          console.log('Opção clicada:', index);
          
          // Remove seleção de todas as opções
          options.forEach(function(opt) {
            opt.classList.remove('selected', 'right', 'wrong');
          });
          
          // Seleciona esta opção
          this.classList.add('selected');
          selectedOption = this;
          
          // Garante que a explicação permanece oculta
          if (explanation) {
            explanation.style.display = 'none';
          }
        };
      });
      
      // Adiciona manipulador de evento para o botão de envio
      submitButton.onclick = function() {
        console.log('Botão Enviar clicado');
        
        if (!selectedOption) {
          console.log('Nenhuma opção selecionada');
          return;
        }
        
        // Remove a classe de seleção
        selectedOption.classList.remove('selected');
        
        // Verifica se a resposta está correta
        const isCorrect = selectedOption.getAttribute('data-correct') === 'true';
        console.log('Resposta correta?', isCorrect);
        
        // Adiciona a classe apropriada
        selectedOption.classList.add(isCorrect ? 'right' : 'wrong');
        
        // Mostra a explicação
        if (explanation) {
          explanation.style.display = 'block';
          console.log('Explicação mostrada');
        }
      };
    });
  });
})();
