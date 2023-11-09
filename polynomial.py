class Polynomial:
    def __init__(self, c_list, in_order=True):
        """
        Initial method

        Parameters
        ----------
        c_list : list of coefficients of polynomial
        in_order : whether or not polynomial coefficients are needing to be ordered or not.
            The default is True.

        Returns
        -------
        None. Sets self.degree, the polynomial's degree.
        Also sets self.coeffs, the ordered coefficients of the polynomial.

        """
        if in_order:
            self.coeffs = c_list[::-1]  # Reverse the list to store coefficients in the expected order
        
        else:
            self.coeffs = c_list
            
        self.strcoeffs = c_list

        while len(self.coeffs) > 1 and self.coeffs[-1] == 0:
            self.coeffs.pop()

        # Determine the degree by finding the index of the last non-zero coefficient
        self.degree = len(self.coeffs) - 1
        

    def __str__(self):
        """
        Returns user friendly string object representing the polynomial.

        Returns
        -------
        polynomial_str : example: 6x^2 + 1x^1 + 2
        """
        polynomial_str = ""
        for i, coeff in enumerate(self.coeffs[::-1]):
            if coeff != 0:
                if i == self.degree:
                    term = f"+ {str(coeff)}"
                else:
                    term = f"{coeff}x^{self.degree - i}"
                    if coeff > 0 and i > 0:
                        term = f"+ {term}"
                polynomial_str += term + " "
        return polynomial_str

    def at(self, c):
        """
        Takes a number, c, and returns the value of the polynomial at x = c.

        Parameters
        ----------
        c : integer or float number

        Returns
        -------
        value : integer/float number value of polynomial at x = c.

        """
        value = 0
        for i, coeff in enumerate(self.coeffs):
            value += coeff * (c ** i)
        return value

    def __eq__(self, other):
        """
        Checks for equality of 2 polynomial objects.

        Parameters
        ----------
        other : Polynomial object to be compared to

        Returns
        -------
        Boolean object (true or false)

        """
        if not isinstance(other, Polynomial):
            return False

        # Consider trailing zeros by comparing only the relevant coefficients
        relevant_coeffs_self = self.coeffs[: self.degree + 1]
        relevant_coeffs_other = other.coeffs[: other.degree + 1]

        # Compare coefficients up to the maximum degree
        result = relevant_coeffs_self == relevant_coeffs_other and self.degree == other.degree

        return result

    def __ne__(self, other):
        """
        Checks if two polynomial objects are NOT equal to one another.

        Parameters
        ----------
        other : Polynomial object to compare to.

        Returns
        -------
        Boolean object (true, polynomials not equal, or false)

        """
        return not self == other

    def __add__(self, other):
        """
        a Polynomial object can be added to another Polynomial object or 
        to a number (integer or float).

        Parameters
        ----------
        other : Polynomial object to add to self (initial) polynomial.

        Returns
        -------
        Returns new polynomial object.

        """
        if isinstance(other, Polynomial):
            max_degree = max(self.degree, other.degree)
            new_coeffs = [0] * (max_degree + 1)
        
            for i in range(max_degree + 1):
                if i <= self.degree:
                    new_coeffs[i] += self.coeffs[i]
                if i <= other.degree:
                    new_coeffs[i] += other.coeffs[i]
                
            new_coeffs.reverse()
        
            return Polynomial(new_coeffs)
        else:
            new_coeffs = self.strcoeffs.copy()  # Make a copy of the coefficients list
            new_coeffs[-1] += other  # Add 'other' to the last coefficient
        
            return Polynomial(new_coeffs)


    def __sub__(self, other):
        """
        a Polynomial object can be subtracted from another Polynomial object 
        or a number (integer or float) can be subtracted off a Polynomial object

        Parameters
        ----------
        other : Polynomial object to be subtracted.

        Returns
        -------
        New polynomial object.

        """
        if isinstance(other, Polynomial):
            degree_result = max(self.degree, other.degree)
            new_coeffs = [0] * (degree_result + 1)
            for i in range(self.degree + 1):
                new_coeffs[i] += self.coeffs[i]
            for i in range(other.degree + 1):
                new_coeffs[i] -= other.coeffs[i]
            return Polynomial(new_coeffs, in_order = False)

        else:
            new_coeffs = self.coeffs.copy()
            new_coeffs[0] -= other
            return Polynomial(new_coeffs, in_order = False)

    def __mul__(self, other):
        """
        a Polynomial object can be multiplied to another Polynomial object or 
        to a number (integer or float)

        Parameters
        ----------
        other : Other polynomial object to be multiplied

        Returns
        -------
        New polynomial object.

        """
        if isinstance(other, Polynomial):
            max_degree = self.degree + other.degree
            new_coeffs = [0] * (max_degree + 1)

            for i in range(self.degree + 1):
                for j in range(other.degree + 1):
                    new_coeffs[i + j] += self.coeffs[i] * other.coeffs[j]

            new_coeffs.reverse()

            return Polynomial(new_coeffs)
        else:
            new_coeffs = [0] * (self.degree + 1)
            for i in range(self.degree + 1):
                new_coeffs[i] += self.coeffs[i] * other
                
            new_coeffs.reverse()
            return Polynomial(new_coeffs)
        
    def __pow__(self, n):
        """
        Takes an integer object say n as argument. The method must return a 
        new Polynomial object which is the polynomial raised to the power of n.

        Parameters
        ----------
        n : power to raise polynomial to.

        Returns
        -------
        New polynomial object, example:
            Polynomial p: 6x^1 + 2
            Results
            Case 1 p^0: 1
            Case 2 p^1: 6x^1 + 2
            Case 3 p^2: 36x^2 + 24x^1 + 4
            <class 'polynomial.Polynomial'>

        """
        if n == 0:
            return Polynomial([1])
        elif n == 1:
            return self
        else:
            result = Polynomial([1])  # Initialize result as the constant polynomial 1

            for _ in range(n): #variable doesn't matter, just needs to loop
                result = result * self  # Use the * operator to multiply polynomials

            return result
    
    def __or__(self, other):
        """
        It returns the result of composition operation. Example: f(g(x))

        Parameters
        ----------
        other : Polynomial object self is to be composed with.

        Returns
        -------
        New polynomial object.
        Example:
        When a(x) = x2 + 2x + 7 is composed with b(x) = x, the result of the 
        operation is just a ◦ b = a.

        """
        if not isinstance(other, Polynomial):
            return TypeError("The value must be a Polynomial")
            
        result = Polynomial([0])

        for i, coeff in enumerate(self.coeffs):
            if isinstance(other, int):
                result += (other ** i) * coeff
                    
            else:
                result += (other ** i) * coeff

        return result
        
    def derivative(self, m):
        """
        accepts a positive integer m > 0 as input and computes the mth 
        derivative of the polynomial, valid for m > 0.

        Parameters
        ----------
        m : mth derivative of polynomial.

        Returns
        -------
        new polynomial object

        """
        if m < 0:
            raise ValueError("m must be a positive integer")

        if m > self.degree:
            return Polynomial([0])

        # Compute the mth derivative
        new_coeffs = self.coeffs.copy()
        for _ in range(m):
            new_coeffs = [coeff * i for i, coeff in enumerate(new_coeffs)]
            new_coeffs.pop(0)

        return Polynomial(new_coeffs[::-1])



