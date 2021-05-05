Feature: PyBee Rule Test

    Rule: Factorial rules

        Scenario: Factorial of three
            Given I have the number 3
            When I compute its factorial
            Then I have the number 6

        Scenario: Factorial of four
            Given I have the number 4
            When I compute its factorial
            Then I have the number 24

        Scenario Outline: Factorial of numbers
             Given there are <start> cucumbers
             When I eat <eat> cucumbers
             Then I should have <left> cucumbers

            Examples:
            | start | eat | left |
            |    12 |   5 |    7 |
            |    20 |   5 |   15 |
            |    30 |   3 |   27 |