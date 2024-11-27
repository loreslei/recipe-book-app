describe('Página Inicial do FoodWriter', () => {
  beforeEach(() => {
      cy.visit('http://localhost:5000'); 
  });

  it('Deve exibir o cabeçalho principal corretamente', () => {
      cy.get('#Header').should('contain.text', 'Bem-vindo ao F🥨');
  });

  it('Deve exibir os botões Cadastrar-se e Login para usuários não autenticados', () => {
      cy.get('#CaixaBotoes').should('exist');
      cy.get('#CaixaBotoes a').contains('Cadastrar-se').should('have.attr', 'href', '/register');
      cy.get('#CaixaBotoes a').contains('Login').should('have.attr', 'href', '/login');
  });

  it('Deve permitir a navegação pelo carrossel', () => {
      cy.get('.carousel-inner .carousel-item').should('have.length', 3); 
      cy.get('.carousel-control-next').click();
      cy.get('.carousel-item.active').should('not.have.class', 'carousel-item:first-child');
  });
});
