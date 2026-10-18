# Manual Test Cases

Execute these scenarios in a browser and record the actual result, Pass/Fail, tester, date and screenshot evidence before submission.

| ID | Scenario | Steps | Expected result |
|---|---|---|---|
| MT-01 | Home page | Visit / while logged out | Landing page appears |
| MT-02 | Register valid user | Use unique email and password 8+ characters | Dashboard opens |
| MT-03 | Short password | Register with password under 8 characters | Validation message |
| MT-04 | Duplicate email | Register an existing email | Duplicate warning |
| MT-05 | Valid login | Enter correct credentials | Dashboard opens |
| MT-06 | Invalid login | Enter incorrect password | Error appears |
| MT-07 | Login guard | Visit dashboard logged out | Redirect to login |
| MT-08 | Create test | Submit all required fields | Test appears in list |
| MT-09 | Execute Pass | Change test status to Pass | Result is saved |
| MT-10 | Execute Fail | Change test status to Fail | Result is saved |
| MT-11 | Report bug | Enter title, description and steps | Bug appears in list |
| MT-12 | Update defect | Change bug lifecycle status | New status is saved |
| MT-13 | Search tests | Search by title/module | Matching tests appear |
| MT-14 | Search bugs | Search by title | Matching bugs appear |
| MT-15 | Empty report | Open report without tests | Pass rate is 0% |
| MT-16 | Invalid test status | Submit unsupported status | HTTP 400 response |
| MT-17 | Data isolation | Attempt to access another user's record | Record is not disclosed |
| MT-18 | Logout | Log out and revisit dashboard | Login is required |
