Feature: Forms

    Background:
        Given a browser

    @web
    Scenario: Filling-in fields
        When I visit "http://web/forms.html"
        Then "disabled" should be disabled
        And "name" should be enabled
        When I fill in "name" with "Foo Bar"
        Then field "name" should have the value "Foo Bar"

        When I fill in "passwd" with "hax0r"
        Then field "passwd" should have the value "hax0r" within 1 seconds
        When I choose "male" from "sex"
        And I check "subscribe"
        Then field "subscribe" should have the value "subscribe"
        And the field "digest" should be checked
        When I uncheck "digest"
        Then the field "digest" should be unchecked
        When I toggle "digest"
        Then the field "digest" should be checked
        When I select "no" from "countries"
        And I select by text "Greece" from "countries"
        And I attach the file "test.txt" to "file"
        And I press "register"
        Then the browser's URL should contain "name=Foo+Bar"
        And the browser's URL should contain "passwd=hax0r"
        And the browser's URL should contain "sex=male"
        And the browser's URL should contain "subscribe=subscribe"
        And the browser's URL should contain "digest=digest"
        And the browser's URL should contain "countries=no"
        And the browser's URL should contain "countries=gr"
        And the browser's URL should contain "register=Register"
        And the browser's URL should contain "file=test.txt"

    @web
    Scenario: Checking for enabled/disabled fields
        When I visit "http://web/forms.html"
        Then "disabled" should be disabled
        And "name" should be enabled

    @web
    Scenario: Checking HTML5 validation
        When I visit "http://web/forms.html"
        And I fill in "email" with "foo@"
        Then field "email" should be invalid
        When I fill in "email" with "foo@"
        Then "disabled" should be disabled
        And "name" should be enabled

    @web
    Scenario: Content editable
        When I visit "http://web/forms.html"
        And I set the inner HTML of the element with id "ce" to "<p>Hello foo world</p>"
        Then I should see "Hello foo world"
        When I set the inner HTML of the element with class "ce" to "<p>Hello bar world</p>"
        Then I should see "Hello bar world"

    @web
    Scenario: Checking required fields
        When I visit "http://web/forms.html"
        Then field "name" should be required
        And field "passwd" should not be required
