describe('Starting With Tests', () => {
    it('Does 2+2 equal 4?', () => {
	expect(2 + 2).to.equal(4);
    });
    it('Does 4+4 return 10?', () => {
	expect(4 + 5).to.equal(10);
    });
    it('Confirm if 5+5 does NOT give 100', () => {
	expect(5 + 5).to.not.equal(100);
    });

    it("Simple object test", () => {
	const person = {
	    name: "Hussain",
	    age: 19,
	};
	assert.isObject(person, "value is object");
    });

    it("Simple string test", () => {
	const name = "Hussain";
	assert.isString(name, "is a String");
    });

    it("Simple not integer test", () => {
	const name = "Ali";
	assert.isNotNumber(name, "is not an integer");
    });
});
