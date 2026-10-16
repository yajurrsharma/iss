# Horizon Event

(came up w the name at 3 am coz i was thinking about black holes)


### This is a fun project I worked on, for my love of space and astronomy, combined with coding.

the ISS has always fascinated me for 2 reasons, how it was assembled, and how its ACTIVELY used to house astronauts. 

when i initially got into coding, i created a version of this using the requests module, with the entire project being CLI based. when i heard about expedition, i HAD to give my old project another try! so here it is, revamped and redone, with a web interface, new (and better) modules and more stuff.

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

---

## Sneaky Feature

I've also added a feature that, unfortunately, in the current stages has to be configured by the user. That feature is the *email notification system*. Basically, when the program finds the next visible pass (whether it be day or night) It'll send you an email when the pass is happening, so you can look out and above your horizon, to, well, see the event! (get it, horizon event?)

to setup the email system, all you need to do create a `.env` file in your cloned directory. Next, if you have 2FA enabled on your email account, simply to go that page, and search for *App Passwords*. Create one, and save it. Finally, just go to your newly created `.env` file, and paste these lines, 
```bash
SMTP_USERNAME=youremailhere
SMTP_PASSWORD=yourapp_passwordhere
```
and you're done! Save your file, and run the code as you would normally. However, now, you'll be able to recieve emails from, well, yourself about the horizon event!



