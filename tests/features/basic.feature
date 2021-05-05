Feature: PyBee Basic Test
    In order to play with Lettuce
    As beginners
    We'll implement some stuff


    Background:
      Given This is a test

    Scenario: Factorial of 7
        Given I have the number 7
        When I compute its factorial
        Then I see the number 5040

    Scenario: Test Horizontal DataTable Conversion
        Given I have the following:
        | apples | banannas | pears |
        |  1     |   2      |  3    |
        | 2      |   4      |  6    |
        Then I can convert it to a horizontal dictonary of lists
        And I can convert it to a horizontal dictonary of coordinates
        * I can convert it to a horizontal dictonary of ints
        * I can convert it to a horizontal lists of dictonarys
        * I can convert it to a horizontal lists of lists

    Scenario: Test Vertical Datatable Conversion
        Given I have the following:
        | apples   | 1 | 2 |
        | banannas | 2 | 4 |
        | pears    | 3 | 6 |
        Then I can convert it to a vertical dictonary of lists
        And I can convert it to a vertical dictonary of coordinates
        * I can convert it to to vertical dictonary of ints
        * I can convert it to a vertical lists of dictonarys
        * I can convert it to a vertical lists of lists

    Scenario: Test Doc String
        Given I have the following markup:
        """
        Some Test
        ============
        Lorem ipsum facto
        """
        Then check markup length is 40