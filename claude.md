# CLAUDE.md

## Project Goal

Build and maintain a professional, responsive, accessible, and production-ready portfolio website.

---

## Before Any Change

1. Read relevant files first.
2. Understand existing architecture.
3. Search for existing implementations.
4. Reuse before creating.
5. Keep changes minimal.

Never start coding immediately.

---

## Architecture Rules

* Do not create duplicate components.
* Do not create duplicate CSS.
* Do not create duplicate JavaScript.
* Do not create duplicate utilities.
* Extend existing code whenever possible.
* Follow existing project structure.
* Maintain a single source of truth.

---

## Naming Rules

Use consistent naming.

Examples:

Components:

* HeroSection
* ProjectCard
* ContactForm

Files:

* home.css
* projects.css
* contact.js

Classes:

* hero-section
* project-card
* contact-form

Never use:

* component-new
* component-v2
* final-final
* copy

---

## Frontend Standards

### HTML

* Semantic HTML only.
* Accessibility required.
* Structure only.

### CSS

* Store CSS in static/css/.
* Never use inline CSS.
* Never use style attributes.
* Use CSS variables.
* Reuse existing styles before creating new ones.

### JavaScript

* Store JavaScript in static/js/.
* Keep templates clean.
* Separate logic from markup.

---

## Responsive Design

Every feature must work on:

* Mobile
* Tablet
* Desktop

Use a mobile-first approach.

---

## Accessibility

Required:

* Keyboard navigation
* Focus states
* Semantic HTML
* Proper labels
* Accessible forms

---

## Performance

* Optimize images.
* Avoid unnecessary code.
* Remove unused imports.
* Remove dead code.
* Avoid duplicate logic.

---

## UI Standards

Target quality similar to:

* Vercel
* Linear
* Stripe
* Notion

Requirements:

* Clean layout
* Consistent spacing
* Consistent typography
* Professional appearance

---

## SEO

Ensure:

* Proper page titles
* Meta descriptions
* Semantic headings
* Open Graph metadata

---

## Before Completion

Verify:

* No duplicate code
* No duplicate files
* No inline CSS
* No inline JavaScript
* No console errors
* Mobile responsive
* Accessible
* Consistent naming

---

## Agent Behavior

Act as:

* Senior Frontend Engineer
* UI/UX Reviewer
* Accessibility Reviewer
* Performance Reviewer

Challenge poor implementations.

Always search the codebase before creating anything new.

Prefer reuse over creation.