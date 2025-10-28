# Cadet Parade Role Planner

by Indiana Daikee


---

## Project Description

This project is a database-driven web application, inteded to simplify the allocation of parade roles at cadets. It has the following features:

- Individual user account registration and login system, with some accounts having admin permissions
- An interface showing all the parade roles for this and next week, allowing users to allocate/deallocate themselves to specific roles, and admins to allocate/deallocate any user
- Database tracking of how many times each user has done each role, and an interface for users to see their personal statistics
- An admin-only interface showing a unit-wide overview of how many times each user has done each role
- Responsive design, meaning the website works on devices of any screen size and with any modern browser
- Dark mode support -  _note that __light mode is forced by default__ as this is what the vast majority of my end-users will use - please delete `data-theme="light"` from line 15 of [base.jinja](app\templates\pages\base.jinja) if you would like to use your system default_


---

## Project Documentation

- [Project requirements](0-requirements.md)
- Development sprints:
    - [Sprint 1](1-sprint-1-prototype.md) - Development of a prototype
    - [Sprint 2](2-sprint-2-mvp.md) - Development of a minimum viable product (MVP)
    - [Sprint 3](3-sprint-3-refinement.md) - Final refinements
- [Final review](4-review.md) 

## Sample Account Login Details

- See [logins.md](logins.md)