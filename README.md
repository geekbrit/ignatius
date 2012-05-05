ignatius
========

&quot;Ants&quot; experiments

This is a port from a C++ project I wrote in 1995 to Python, essentially just to
give me an excuse to practise writing Python. It is quite fun - you can vary
several aspects of the environmental energy balance and observe how it affects
population growth in the Ants - I persist in calling them ants despite the fact
that since I show the last 16 pixels they have visited, they look like tiny worms.

The system is also an evolutionary model - the most successful ants will breed
and spin off progeny that are formed from a composite of their DNA - all behaviour
in this model is driven by two chromosones for each ant - a hunting chromosone
and a feeding chromosone.

The gui for this project was created using Qt Creator - open ants.ui in Qt Creator, 
then save after editing and run &quot;pyuic4 ants.ui > antsUI.py&quot; - never edit
antsUI.py directly.

You will need to have PyQt4 installed for this program to work:
http://www.riverbankcomputing.co.uk/

License
-------

Use in any way you wish, send me a copy of anything cool that you create from it.
