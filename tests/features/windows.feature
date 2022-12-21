Feature: Windows

    @web
    Scenario: It can open a new window and switch to it
        Given a browser
        When I visit "http://web/window1.html"
        Then I should see "I'm window 1"
        But I should not see "I'm window 2"

        When I open a new window named "window2" at "http://web/window2.html"
        Then I should see "I'm window 2"
        But I should not see "I'm window 1"

    Scenario: It can switch back to a named window
        Given a browser
        When I visit "http://web/window1.html"
        And I name the current window "window1"
        Then I should see "I'm window 1"
        But I should not see "I'm window 2"

        When I open a new window named "window2" at "http://web/window2.html"
        Then I should see "I'm window 2"
        But I should not see "I'm window 1"

        When I switch to the window named "window1"
        Then I should see "I'm window 1"
        But I should not see "I'm window 2"

    Scenario: It can open a new window with relative urls when base_url is set.
        Given a browser
        Given the base url "http://web"
        When I open a new window named "window1" at "/window1.html"
        Then I should see "I'm window 1"
        When I open a new window named "window2" at "http://web/window2.html"
        Then I should see "I'm window 2"
