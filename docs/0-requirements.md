# Project Requirements

## Identified Problem or Need

At Navy Cadets each week we have certian parade roles (e.g. parade commander, quartermaster, bosun's mate) that need to be fulfilled. Every week, the roles are the same, but should ideally be taken by different people so that each role's work is spread roughly equally across the unit over the course of a term. People can volunteer for a role, however if no-one has put themselves forward for a role by Monday (we parade on Tuesday), then that role gets allocated to someone.

Currently, this process of volunteering / allocating involves long-winded WhatsApp message chains to figure out who wants to do what. In order to distribute the roles fairly, we rely on people remembering how many times they've done each role recently - and unfortunately, people's memories aren't quite as reliable as we need.

The problem we have is that it's quite difficult:
- To quickly know who is doing what this current week
- For people to volunteer for a role
- For senior rates / officers to allocate someone a role
- To track how many often each person has done each role


## End-User Requirements

The end users for this website would be everyone that attends the local Navy Cadet unit. This can be split into two main categories of end users, each with different expectations and requirements of the site:

**Junior Rates**

- Have an individual login
- Expect an obvious, clean, and easy-to-use interface that showing which roles are free or taken (and who by) for the current and next week. This interface will mostly be used on mobile phones but must still be desktop compatible
- Need a way to easily accept a role for the current or next week
- Need an obvious way to see if when they've been allocated a role
- Should be able to see an overview / description of each role in case they've forgotten
- Can see their stats over the past term i.e. how many times they've done each role

**Seniors Rates and Officers**

- All of the above needs for Junior rates (everyone does parade roles, not just junior rates), plus:
- The ability to see a chart / graph / figure of some kind showing who is 'pulling their load' over the term with respect to fulfilling roles
- The ability to assign people roles
- The ability to add, edit, and remove roles - though the roles are the same each week, we might make changes to the parade format two or three times a year, meaning the roles would have to be changed.


## Proposed Solution

A database-driven web application that meets the above needs by having:
- A user account login system. This will be linked up to the database, which records when each person has done each role
- Two simple main interfaces for everyone:
    - One showing all the parade roles for this and next week, along with who has taken this role. If no-one has taken that role, there should be a button for the logged-in user to volunteer for that role.
    - Another showing that user's statistics over the past 10 weeks - how many times they have done each role.
- An aditional interface for senior rates and officers, showing a unit-wide overview of who is 'pulling their load' in regard to doing each role
- Some way for senior rates and officers to allocate an untaken role to someone.


---

# Relevant Implications

## Accessiblity

Accesibility means ensuring my website is availiable to, and can be used by, all end-users, regardless of their abilities. 

### Relevance to the System

Everyone that uses this site needs to be able to do so easily; if some people arenn't able to use my site (e.g. they can't read low contrast text or have an old phone), then it won't be able to serve it's purpose - to make cadets easier for *everyone*. It would also be borderline discriminatory, as everyone should be able to use my website, regardless of accessibility concerns.

### Impact / Considerations

To ensure my website is accessible to all my end-users, I need to make my website function properly on all devices - mobile phones and computers - of all screen sizes. This may be a responsive, mobile-first design, or I may have seperate layouts for the desktop and mobile versions. I also need to ensure the content of my site is viewable and usable by everyone - this will include:
- Selecting a good colour scheme to ensure that people with colour-blindness or impaired vision can read the text,
- Selecting a readable font and font size to make it readable on any device,
- Providing alt text for images to ensure that users with a screen reader can interact properly,
- Making UI components like buttons appropriately sized and easily clickable on all devices and screen sizes.


## Functionality

Functionality means ensuring my website works as intended, as expected, and ultimately serves my end-users.

### Relevance to the System

My website's design needs to be functional for both of my end-user groups - junior rates will expect it to 'just work' easily and without bugs or issues; anything buggy or unexpected will confuse them and ultimately void the purpose of my site, which is to make parade allocations easier for everyone. The same goes for the senior rates and officers - they need the interface for allocating roles and tracking people's work to be simply and functional, else they'll simply go back to the old system.

### Impact / Considerations

Making my website functional will involve iterative testing and feedback-gathering from both of my end-user groups. I will repeat the process of making changes and gathering feedback throughout the development of my site until the end of my third sprint, when I'll have a final design. I will need to evaluate the functionality of this design against my end users' wants and needs, ensuring my site is logical and bug-free.


## Ethics

Ethics means ensuring my website is appropriate and can't cause harm to my end-users.

### Relevance to the System

The main purpose of this site is for it to enable the allocation of parade roles in an easier, quicker, and notably, **fairer** way than presently. If my website isn't ethically sound - in other words, fair, then it won't achieve it's goal.

### Impact / Considerations

I need to consider how my website could cause harm - while my site's stakes for abuse aren't especially high, the outcomes my it creates should be fair for everyone - it wouldn't be fair if it resulted in the same person doing the same role every week. I might consider adding a warning when allocating the same person for the same role for multiple weeks in a row. I also need to make sure the personal statistics page doesn't 'put down' my users for not doing enough work - even if they're not pulling their load.


## Aesthetics

Asthetics relate to how my site will look in terms of design.

### Relevance to the System

A clean, good-looking site will make for an appealing and overall easier experience for my end-users compared to one that has innapropriate colours and unneeded clutter.

### Impact / Considerations

I will need to consider and work with my end-users to choose the right colour scheme, fonts, and element positioning that maximise aesthetics while retaining proper usability and accessibility.



## Usability

Usabulity is how easy to use my site will be for the end-user, without the need for help or guidance.

### Relevance to the System

It's important my end-users find navigating and operating my website to be easy - users will expect my site to follow established conventions (as described by Nielsen's usability heuristics), and if my website doesn't meet this expectation, my users will end up confused, bothered, and ultimately worse off than before my site.

### Impact / Considerations

A big part of making my website as usable as possible will come from the iterative design process: gathering feedback from both of my end-user groups, making appropriate changes, gathering more feedback, and so on.

Maximising usability will also mean making sure my website follows Nielsen's usability heuristics. These heuristics are detailed below in the *User Experience (UX) Principles* section.


---

# User Experience (UX) Principles

## NAME OF UX PRINCIPLE 1

Replace this text with a clear explanation of what the principle means.

### Relevance to the System

Replace this text with an explanation of why the principle is relevant to this particular project.

### Impact / Considerations

Replace this text with an explanation of what you will need to consider moving forward and how the project will be impacted by this principle.


## NAME OF UX PRINCIPLE 2

Replace this text with a clear explanation of what the principle means.

### Relevance to the System

Replace this text with an explanation of why the principle is relevant to this particular project.

### Impact / Considerations

Replace this text with an explanation of what you will need to consider moving forward and how the project will be impacted by this principle.


## NAME OF UX PRINCIPLE 3

Replace this text with a clear explanation of what the principle means.

### Relevance to the System

Replace this text with an explanation of why the principle is relevant to this particular project.

### Impact / Considerations

Replace this text with an explanation of what you will need to consider moving forward and how the project will be impacted by this principle.

