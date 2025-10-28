# Navy Cadet Parade Role Planner

by Indiana Daikee

---

## Project Description

At Navy Cadets, we have parade roles that need to be fulfilled by different people each week. Tracking how many times people have done each role, and allocating roles weekly, are tasks we struggle to manage effectively. As such, this database-driven web app solves these problems with the following features:

- Individual user account registration and login system, with some accounts having admin permissions
- An interface showing all the parade roles for this and next week, allowing users to allocate/deallocate themselves to specific roles, and admins to allocate/deallocate any user
- Database tracking of how many times each user has done each role, and an interface for users to see their personal statistics
- An admin-only interface showing a unit-wide overview of how many times each user has done each role
- Responsive design, meaning the website works on devices of any screen size and with any modern browser
- Dark mode support -  _note that __light mode is forced by default__ as this is what the vast majority of my end-users will use. To use your system default, please delete `data-theme="light"` from line 15 of [base.jinja](app\templates\pages\base.jinja)_


---

## Project Links

- [GitHub repo for the project](https://github.dev/waimea-igdaikee/300dtd-cadet-planner-website/)
- [Project documentation](https://waimea-igdaikee.github.io/300dtd-cadet-planner-website/)
- [Live web app](https://waimea-igdaikee.github.io/300dtd-cadet-planner-website/)


---

## Project Files

- Program source code can be found in the [app](app/) folder
- Project documentation is in the [docs](docs/) folder, including:
   - [Project requirements](docs/0-requirements.md)
   - Development sprints:
      - [Sprint 1](docs/1-sprint-1-prototype.md) - Development of a prototype
      - [Sprint 2](docs/2-sprint-2-mvp.md) - Development of a minimum viable product (MVP)
      - [Sprint 3](docs/3-sprint-3-refinement.md) - Final refinements
   - [Final review](docs/4-review.md)
   - [Setup guide](docs/setup.md) - Project and hosting setup

---

## Project Details

This is a digital media and database project for **NCEA Level 3**, assessed against standards [91902](docs/as91902.pdf) and [91903](docs/as91903.pdf).

The project is a web app that uses [Flask](https://flask.palletsprojects.com) for the server back-end, connecting to a SQLite database. The final deployment of the app is on [Render](https://render.com/), with the database hosted at [Turso](https://turso.tech/).

The app uses [Jinja2](https://jinja.palletsprojects.com/templates/) templating for structuring pages and data, and [PicoCSS](https://picocss.com/) as the starting point for styling the web front-end.

The project demonstrates a number of **complex database techniques**:
- Structuring the data using multiple tables
- Creating queries which insert, update or delete to modify data
- Creating customised data displays from multiple tables (e.g. web pages)
- Dynamically linking data between the database and a front-end display
- Applying data access permissions as appropriate to the outcome

The project demonstrates a number of **complex digital media (web) techniques**:
- Using non-core functionality
- Applying industry standards or guidelines
- Using responsive design for use on multiple devices
- Using dynamic data handling and interactivity
- Automation through scripts

