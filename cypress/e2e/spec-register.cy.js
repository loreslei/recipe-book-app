describe('Página de Cadastro', () => {
  beforeEach(() => {
      cy.visit('http://localhost:5000/register'); // Substitua pela URL correta http://127.0.0.1:5000/register
  });

  it('Deve exibir o cabeçalho de cadastro', () => {
      cy.get('header').should('contain.text', 'Faça o Seu Cadastro');
  });

  it('Deve conter todos os campos obrigatórios', () => {
      cy.get('input#username').should('exist');
      cy.get('input#email').should('exist');
      cy.get('input#password').should('exist');
      cy.get('input#password_repeat').should('exist');
  });

  it('Deve exibir mensagens de erro ao enviar dados inválidos', () => {
      cy.get('#LoginBtn').click(); // Submete sem preencher os campos
  });

  it('Deve submeter o formulário corretamente com dados válidos', () => {
      cy.get('#username').type('TesteUsuario');
      cy.get('#email').type('teste@exemplo.com');
      cy.get('#password').type('SenhaForte123');
      cy.get('#password_repeat').type('SenhaForte123');

      cy.get('#LoginBtn').click();
  });
});
