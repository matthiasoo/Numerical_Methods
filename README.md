# 📊 Numerical Methods in Python

This repository contains Python implementations of various **numerical methods** used to solve mathematical problems. It is structured into the following categories:

---

## 📌 1. Root-Finding Methods

### 🔹 Bisection Method  
Finds a root of a function in a given interval \([a, b]\) by repeatedly halving the interval and selecting the subinterval where the sign of the function changes.

### 🔹 Regula Falsi (False Position) Method  
Like the bisection method, but uses **linear interpolation** between the endpoints to estimate the root more efficiently.

---

## 📌 2. Solving Systems of Linear Equations

### 🔹 Gaussian Elimination  
Solves systems of linear equations by converting the matrix to **upper triangular form** using row operations. Then, it uses **back substitution** to find the solution.

---

## 📌 3. Interpolation Methods

### 🔹 Newton's Interpolation (for Unequal Intervals)  
Constructs a polynomial that passes through a set of points with non-uniform \(x\)-coordinates using **divided differences**. Efficient for adding new points without recalculating everything.

---

## 📌 4. Numerical Integration Methods

### 🔹 Newton-Cotes Quadrature (Simpson's Rule)
Approximates the value of a definite integral using **quadratic polynomials** over subintervals. Iteratively increases accuracy based on user-defined error tolerance. Works well even with functions that have singularities in the weight.

### 🔹 Gauss-Chebyshev Quadrature  
Evaluates integrals of the form:

∫ from -1 to 1 of f(x) / √(1 - x²) dx

Uses **Chebyshev nodes and weights** (typically 2–5 nodes) to efficiently compute the integral, taking advantage of Chebyshev polynomial properties.

---

More numerical methods will be added soon!