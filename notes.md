# Improvements
Right now we have reset.py, which just calls 4 api calls to reset everything. Let's **MOVE THAT INTO A JSON FILE AND CALL ACTIONS.WRITE_DATA('reset.json')!**

We use too much JS, I think. I'll look into changing that.
Yep. We are sending DELETEs by taking the button and using a click eventlistener instead of a form like a sane human. I will remove JS after I implement this stuff the smart way.

# Automating API calls
There will need to be a function which parses the form from the server and updates the JSON accordingly. We will also need to be able to delete actions.
I think the best way to go about this is to store a file for each registered person. (Myabe auth them?)

# Need to add:
3) MAKE EVERYTHING TURN OFF FOR REAL

4) Fix light color being 0,0,0 in actions.hst even when i set it to something nicer

5) TEST IT ALL!!

6) create username_actions.hst on account creation :)

7) Give users their own actions files!

8) Add little checkboxes or something that allow you to select what the entity should actually do in /actions (enable shuffle, play my song, turn to RGB, etc)
