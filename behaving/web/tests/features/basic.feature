Feature: Text presence

    Background:
        Given a browser

    Scenario: Text presence
        When I visit "http://localhost:8080"
        Then I should see "Hello world"
        And I should not see "hidden"
        When I reload
        Then I should see "Late text" within 2 seconds
        And I should not see "Very late text" within 2 seconds

    Scenario: Element presence
        When I visit "http://localhost:8080"
        Then I should see an element with id "content"
        And I should see an element with the css selector "div#content"
        And I should not see an element with id "foo"
        And I should not see an element with the css selector "div#foo"
        When I reload
        Then I should see an element with the css selector "span#late" within 2 seconds
        And I should not see an element with the css selector "span#very-late" within 2 seconds