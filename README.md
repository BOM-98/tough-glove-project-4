# Tough Glove Project 4

# Table of Contents


# Project Background

## Overview

Tough glove has been created for a boxing gym owner who needs a way to present his gym to the world so he can acquire new members. Tough glove is also a system through which members can create an account, see what classes are available and book classes.

Tough glove is based in Dublin, Ireland and is separating itself from other boxing gyms in Ireland by fulfilling an unmet need in people who want to improve their fitness through boxing classes, while also picking up key boxing skills and principles. 

The market in Dublin has a segment of people - typically males between 18 - 50 - who do not want to competitively compete in boxing, but still want to learn the fundamental skills of the sport. Typical boxing gyms either serve as full-fledged amateur boxing gyms that prepare athletes for bouts, or ‘box-fit’ gyms that emphasise fitness over teching sound boxing principles. 

Members want to join a gym where they can improve their fitness, but also learn how to handle themselves appropriately in the ring and ensure they don’t pick up ‘bad habits’ typically seen when people work out in boxfit classes. The goal in boxfit classes is typically to tire out members and keep their heart rate up.

## Problem Statement

Your client is a new boxing club based in Dublin 6, Ireland. The owner is in need of a way to have members book classes (both 1:1 classes and group classes) and keep track of who is attending.

The manager also needs this website to be a marketing channel for his new gym and acquire new members. Therefore he needs to be able to communicate what differentiates his classes from other boxing gyms. This would involve a website that has a strong landing page to convert website visitors. The website needs to convey the value proposition of a high-paced boxing class that places equal value on good fundamental boxing skill building.

## Research: 

- User Interviews: 1:1 interviews were conducted with existing gym members, and also potential new gym members, to determine what goals they have and what messaging and value propositions appeal to them. 
- Competitive Analysis: Examining competing boxing gym classes and websites revealed existing offerings and their strengths and weaknesses. This informed our choice of target market, value proposition, messaging and strategy.
- User Testing: Usability testing of existing flows were carried out with existing gym members to examine how they navigate the system and competitor solutions (Glofox & Squarespace)

## Design

- I began the process by designing wireframes of the site in order to get an overall understanding of the user flows and necessary pages to achieve the client outcomes.
- I converted the wireframes into [a figma prototype](https://www.figma.com/proto/9gEj83rMB6EfxZzyMkmk81/Tough-Glove-Medium-Fidelity-Design?page-id=0%3A1&type=design&node-id=501-39&viewport=290%2C3902%2C0.52&t=QolXKX1XZCvxny5F-1&scaling=scale-down-width) to determine the flow, color schemes and typography that would be used.
- These prototypes were shared with the gym owner who gave some initial feedback to ensure it achieved their objectives. The messaging and branding was accepted by the owners. I confirmed that the business objectives were met with the figma prototype. 
- The design was then tested with current gym members to ensure they understood the proposition and were able to navigate the prototype without confusion.
- The logo, typeface and colour scheme were chosen to reflect the Tough Glove gym ethos of challenging oneself, respect for the science of boxing and professionalism.

![Colour palette](readme/colour-scheme.png)


## Agile Development

Agile software development methods were used to deliver this project and ensure that an iterative approach was taken to acheive the best results for the end-user. 
- The project was broken down from the high level business outcomes and problem statement into epics and user stories. 
- The end user's requirements were written from the end user's perspective to help make sure the right features were being built in a user-centric way.

A github projects board was used to track and manage the expected workload involved in this project, and break it down into a list of epics, and then further into user stories that could be worked towards to build the site on time.
- Each user story was written with a clear description following the convention of "As a ____, I want to ______, so that ____".
- A points system was used to estimate the effort involved with each story.
- The end user goal and end business goal was clearly articulated on each story, along with the acceptance criteria. 
- Each story contained the necessary tasks required to complete them and achieve the acceptance criteria. 
- #### [Link to the GitHub Project board](https://github.com/users/BOM-98/projects/4/views/1)


User stories were prioritized using the MoSCow method (Must have, Should have, Could have, Won't have)
- #### [Link to the MoSCow Prioritization Board](https://github.com/users/BOM-98/projects/4/views/3)

Some user stories relating to a blog section for the website were deemed to not be necessary and therefore were not added to the project. This could be added to the project on a future date as Tough Glove continue to grow.

## Data Models

The database schema for the tough glove site is shown below:

![Database schema](readme/drawSQL-tough-glove-database-schema.png)


- `User` - represents a user in the tough glove gym. This is the default model provided in the Django framework. Admin users are differentiated from gym members by the groups they are added to. 
- `Members` - represents additional information for each member in the gym, such as their phone number and date joined.
- `Classes` - represents Classes that the gym admin creates for the gym.
- `Bookings` - represents class bookings that members of the gym make to reserve their spot in each class.

Database Relationships:
- `Users` have a one to one relationship with `Members`
- `Users` have a one to many relationship with `Bookings`
- Classes have a one to many relationship with `Bookings`

# Features

## CRUD functionality:

- Member CRUD Functionality
  - Create:
    - Users can create a `User` with an associated `Member` on the register page
    - Users can create a `Bookings` for a class through the BookingForm
  - Read: 
    - Users can read their `User` information on their profile page
    - Users can read all of the `Classes` that are available in the classes page
    - Users can read their `Bookings` they have created in the user bookings page
  - Update: 
    - Users can update the `User` account with the update_member page and form
  - Delete:
    - Users can delete their `Bookings` in their cancel_bookings page
- Admin CRUD Functionality
  - Create:
    - Admins can create new `Users` other than themselves with admin privileges using the CreateUserForm
    - Admins can create `Classes` through the create_class page
    - Admins can create `Bookings` for themselves
  - Read: 
    - Admins can read all of the `Users` that are currently in the gym from the admin dashboard and the members page
    - Admins can read all of the `Classes` that are currently running from the admin dashboard and the classes page. Classes are also displayed on calendars on both pages
  - Update: 
    - Admins can update `Users` on the site, changing all of their details including first_name, last_name and email
    - Admins can update `Classes` by via the UpdateClassForm on the update class page
  - Delete:
    - Admins can delete `Users` and the associated `Members` data on the site if they need to remove members
    - Admins can delete `Classes` from the site
    - Admins can delete `Bookings` that are their own, but not other user's bookings. 


## Authentication / Authorization:

Certain access restrictions were put in place across the website. 

### No Login Required

- Homepage is viewable by everyone 

### Must Be Logged Out To View

Only users who are not logged in can view:
- The registration page to register an account
- The login page to login to their account

If a user is logged in and navigates to these pages they should be redirected to the available classes page


### Login Required:

Logins are required on a user account in order to access these pages:
- Available classes page
- Members page
- Profile page (only their own profile)
- Update Member page (only their own)
- Classes Page
- User Bookings Page (only their own)
- Book Class Page
- Cancel Bookings Page


### Admin Only Access: 

Only users logged in with an admin account can access these pages:

- Profile page (Profiles other than their own)
- Update Member page (can update everyone)
- Delete member page
- Admin dashboard page
- Create Class Page
- Update Class Page
- Delete Class Page
- User Bookings Page (only their own)
- Create User Page (Admin - can create multiple accounts from the admin dashboard)

## General Features: 

### Navigation & Footer

- A primary navigation is present on the header on all pages of the website.

- <b>If a user is logged in as an admin, the user has access to all available navigation links</b>

<details>
<summary>Screenshot of Admin Navigation</summary>

![Screenshot of Admin Navigation ](readme/navigation.png)

</details>
<br>

- If the user is logged in as a member, the user has access to the classes, my booking and profile links

<details>
<summary>Screenshot of Member Navigation</summary>

![Screenshot of Member Navigation ](readme/navigation-member.png)
</details>
<br>

- If the user is not logged in, the navigation displays the register and login links
<details>
<summary>Screenshot of Logged Out Navigation</summary>

![Screenshot of Logged Out Navigation ](readme/navigation-member.png)
</details>
<br>

- The navigation collapses into a burger menu on mobile screens
<details>
<summary>Screenshot of Collapse Menu</summary>

![Screenshot of Collapse Menu](readme/navigation-burger-menu.png)
</details>
<br>

The footer is present on all screens of the website and follows the same conditional login for presenting links as the primary navigation

### Homepage

The homepage acts as an advertising front for any visitors who are not currently members. The copy on the homepage will be optimised for SEO keywords to win search traffic from people searching for boxing gyms in Dublin.

<details>
<summary>Screenshots of The Homepage</summary>

![Screenshot of Hero Section](readme/hero-section.png)
![Screenshot of Homepage Section 3](readme/why-tough-glove.png)
![Screenshot of Homepage Member Plans](readme/membership-program.png)
</details>

### Login & Register

Login and register pages were implemented to manage user access to class schedules and secure contact information within the gym management system

The gym owner collects `first name`, `last name` and `email` for marketing purposes through the registration form. 

Form validation ensures that no username can be used twice. The gym owner requested that people can create multiple accounts with the same email so that field was not restricted as a unique field.

<details>
<summary>Screenshot of The Register Form</summary>

![Screenshot of The Register Form](readme/register-page.png)

</details>
<br>
<details>
<summary>Screenshot of The Login Form</summary>

![Screenshot of The Register Form](readme/login-page.png)

</details>

### Error Pages

Custom error pages were added to handle 400, 403, 404 and 500 errors. 

<details>
<summary>Screenshot of The 404 Page</summary>

![Screenshot of The 404 Page](readme/404-page.png)

</details>

## Admin Features: 

### Admin Dashboard

### Calendars

### Class Management

### Members Listings

## Members Features: 

### Classes Listings

### User Creation

## Member Features

###