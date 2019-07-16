Feature: Using SQLAlchemy

  Scenario: create row
    Given we have postgres running
    And we have a postgres service
    When we create a row
    Then we can select the row again
