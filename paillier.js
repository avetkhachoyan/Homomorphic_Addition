function Paillier() {
    this.keyLength = 512;
    this.key = generateRSAKeyPair(this.keyLength);
    this.n = this.key.n;
    this.g = this.n.add(1);
    this.nSquared = this.n.multiply(this.n);
    this.lambda = lcm(this.key.p.subtract(1), this.key.q.subtract(1));
    this.mu = inverse(modPow(this.g, this.lambda, this.nSquared).subtract(1).divide(this.n), this.n);
}
