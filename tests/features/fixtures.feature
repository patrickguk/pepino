Feature: PyTest Features
    Test pytest fictures pytest can be injected

    Scenario: Caplog injection
        Given I log the following: 'Hello world from pytest'
        Then The message 'Hello world from pytest' is logged