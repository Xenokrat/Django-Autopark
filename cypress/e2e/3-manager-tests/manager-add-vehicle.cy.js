describe('template spec', () => {

    // Начинаем с логирования менедрежа
    beforeEach(() => {
	cy.visit('http://localhost:8000/login/');
	cy.get('input[name="username"]').type('Ivan');
	cy.get('input[name="password"]').type('8XRXF8PpgUr7tNj');
	cy.contains('Логин').click();
	cy.get('a[href*="vehicles/1"]').click()
	cy.get('a[href*="vehicle/create"]').click()
    });

    it('Adds new vehicle', () => {
	cy.get('input[name="VIN"]').type('123');
	cy.get('input[name="year"]').type('1995');
	cy.get('input[name="mileage"]').type('100000');
	cy.get('input[name="cost"]').type('200000');
	cy.get('input[name="color"]').type('Жёлтый');
	cy.get('input[name="purchase_date"]').type('200000');
	cy.get('select[name="enterprise"]')
	    .select(1);
	cy.get("button[type='submit']").click();
	cy.contains('Идентификатор VIN должен состоять из 17 символов, включая только буквы и цифры');
    });


});
