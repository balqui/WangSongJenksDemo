
Demo of each single pass of the Jenks natural breaks algorithm.

Using Brython plus a Python version by Drew Dara-Abrams
(drewda at GitHub) of Jenks Natural Breaks (almost the 
same thing as the optimum 1D k-means discretization by 
Wang and Song) to construct a veeeery inefficient demo of 
the dynamic programming strategy behind these algorithms.

Aesthetics to be taken care of some day.

The algorithm proper would run this demoed process for each 
data point in increasing sequence.

However, to run the demo, I am taking the very slow path 
of calling the general solver for each of the possibilities; 
of course the real scheme tabulates all of them as per the 
Dynamic Programming strategy.

Originally suggested text for readme file follows, to look at and delete some day.

# README #

This README would normally document whatever steps are necessary to get your application up and running.

### What is this repository for? ###

* Quick summary
* Version
* [Learn Markdown](https://bitbucket.org/tutorials/markdowndemo)

### How do I get set up? ###

* Summary of set up
* Configuration
* Dependencies
* Database configuration
* How to run tests
* Deployment instructions

### Contribution guidelines ###

* Writing tests
* Code review
* Other guidelines

### Who do I talk to? ###

* Repo owner or admin
* Other community or team contact