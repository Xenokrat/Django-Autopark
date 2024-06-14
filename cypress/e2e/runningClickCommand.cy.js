describe("Goes to homepage", () => {

    it("Goes to the homepage", () => {
	cy.visit("https://example.cypress.io");
	cy.contains('type').click()

	// Should be on a new URL which
	// includes '/commands/actions'
	cy.url().should('include', '/commands/actions')
    });

    // it("Clicks the Add Element Button", () => {
    //   cy.get('button[onclick="addElement()"]').click();
    // });


});
