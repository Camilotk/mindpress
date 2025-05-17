
/**
 * match.js - JavaScript para quizzes de pares (match)
 * Versão final funcionando corretamente com correção para reset após erros
 */
document.addEventListener('DOMContentLoaded', function() {
  // Encontrar todos os quizzes de pares
  var pairQuizzes = document.querySelectorAll('.pair-quiz');
  
  // Para cada quiz de pares
  pairQuizzes.forEach(function(quiz) {
    // Identificar as listas
    var leftList = quiz.querySelector('.pair-left');
    var rightList = quiz.querySelector('.pair-right');
    
    if (!leftList || !rightList) return;
    
    // Variável para rastrear item selecionado
    var selectedLeft = null;
    
    // Função para limpar completamente todos os estados de erro
    // Esta função é chamada quando um novo item da esquerda é selecionado
    function clearAllErrorStates() {
      // Limpar estados de erro de todos os itens (matched mantém as classes)
      leftList.querySelectorAll('li').forEach(function(item) {
        if (!item.classList.contains('matched')) {
          item.classList.remove('selected', 'wrong');
        }
      });
      
      rightList.querySelectorAll('li').forEach(function(item) {
        if (!item.classList.contains('matched')) {
          item.classList.remove('wrong');
        }
      });
    }
    
    // Adicionar evento aos itens da esquerda
    leftList.querySelectorAll('li').forEach(function(leftItem) {
      leftItem.onclick = function() {
        // Se já estiver combinado, ignorar
        if (this.classList.contains('matched')) return;
        
        // IMPORTANTE: Limpar todos os estados de erro primeiro
        clearAllErrorStates();
        
        // Selecionar este item
        this.classList.add('selected');
        selectedLeft = this;
      };
    });
    
    // Adicionar evento aos itens da direita
    rightList.querySelectorAll('li').forEach(function(rightItem) {
      rightItem.onclick = function() {
        // Se não houver item selecionado ou este já estiver combinado, ignorar
        if (!selectedLeft || this.classList.contains('matched')) return;
        
        // Verificar se o par está correto
        var leftId = selectedLeft.getAttribute('data-id').replace('l', '');
        var rightId = this.getAttribute('data-id').replace('r', '');
        var isCorrect = leftId === rightId;
        
        if (isCorrect) {
          // Par correto - marcar ambos como combinados
          selectedLeft.classList.add('matched', 'right');
          this.classList.add('matched', 'right');
          selectedLeft = null;
        } else {
          // Par incorreto - mostrar feedback temporário
          selectedLeft.classList.add('wrong');
          this.classList.add('wrong');
          
          // Remover o feedback após um momento
          var self = this;
          var leftSelected = selectedLeft;
          setTimeout(function() {
            // CORREÇÃO: Remover explicitamente as classes de ambos os elementos
            if (leftSelected) leftSelected.classList.remove('selected', 'wrong');
            if (self) self.classList.remove('wrong');
            
            // Resetar a variável selectedLeft
            if (selectedLeft === leftSelected) {
              selectedLeft = null;
            }
          }, 1000);
        }
      };
    });
  });
});
