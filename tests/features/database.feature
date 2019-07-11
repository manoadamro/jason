Feature: Using SQLAlchemy

  Scenario: create and serialise instance
    Given we have postgres running
    And we have a postgres service
    When we create an instance of the model and serialise it
    Then only the defined fields are exposed
