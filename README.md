# Horizon Event

(came up w the name at 3 am coz i was thinking about black holes)


### This is a fun project I worked on, for my love of space and astronomy, combined with coding.

the ISS has always fascinated me for 2 reasons, how it was assembled, and how its ACTIVELY used to house astronauts. 

when i initially got into coding, i created a version of this using the requests module, with the entire project being CLI based. when i heard about expedition, i HAD to give my old project another try! so here it is, revamped and redone, with a web interface, newer (and better) modules and more stuff.

## Installation

You can run 
```bash
pip install -r requirements.txt
```
in the folder where you've cloned/downloaded the repository. It'll download all the necessary modules.

After that, run 
```bash
uvicorn app:app --reload
```
in the directory, and go to `localhost:8000` to see the web app.

## How it works

To ensure you ALWAYS get a view, the program first searches for any passes in the next 2 weeks, above 30 degrees, during nighttime WHEN the ISS is sunlit (sunlight reflecting off the ISS so its visible). If none are found, the search is eased down to the ISS being above 15 degrees, in a 3 day window. and if still no pass is found, you get a "no available passes found" message!

## Feature 

I've also added a feature, ~unfortunately, in the current stages has to be configured by the user~ that is the *email notification system*. Basically, when the program finds the next visible pass (whether it be day or night), it'll send you an email 30 minutes before the pass is happening, so you can look out and above your horizon, to, well, see the event! (get it? horizon event? okay yeah ill stop)

---

and to end it, i'd say that this project is just there for some fun, and to revisit some old projects that i've wanted to work on/have worked on. this project was also made for the HackClub Expedition, and took around 6 hours over the span of 2 days to build!

