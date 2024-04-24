// Test homomorphic addition
var paillier = new Paillier();
var a = 10;
var b = 20;
var c_a = paillier.encrypt(a);
var c_b = paillier.encrypt(b);
var c = homomorphicAddition(paillier, [c_a, c_b]);
var result = paillier.decrypt(c);

// Display results on the webpage
document.getElementById("encrypted_a").innerText = "Encrypted a: " + c_a.toString();
document.getElementById("encrypted_b").innerText = "Encrypted b: " + c_b.toString();
document.getElementById("encrypted_sum").innerText = "Encrypted sum: " + c.toString();
document.getElementById("decrypted_sum").innerText = "Decrypted sum: " + result.toString();
