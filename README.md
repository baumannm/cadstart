cadstart
========

This is a small Python 3 application to run Pro/Engineer from individual student computers. It has the following features:
  * the app helps students to select the Pro/E version required by their teacher (if different versions are installed).
  * it helps to connect to the university VPN
  * the GUI assists to check the connection to a given PDM-System
  * in case of problems it helps to clean local caches
  * there are several support features such as
    * a RSS-Feed browser to read latest updates by admins and teachers
    * a feedback form to send meaningful support requests to the university CAD support staff
    * links to many teaching ressources, such as textbooks, homepages, video resources and so on
    
Until now the app was developed, compiled and packed by a single guy (me :-)). The public version should be considered as pre-alpha, since compilation to a Windows compatible exe an packing into a setup-package is not yet included. The GUI runs from command line. There are several open issues, see issue tracker.

In order to run you will need
  * Python 3
  * PySide
  * feedparser
  
In order to use and test you will need
  * a Pro/Engineer version installed on your computer
  * a directory structure with several Pro/E specific config files, templates and resources. This structure will be added to this project soon, as soon as some legal issues are solved.
  
A precompiled installer version of this GUI including the directory structure is available at [the CAD lecture page](http://www.ipek.kit.edu/CAD.php) of the IPEK - Institute of Product Engineering at Karlsruhe Institute of Technology.

Our goal is to leverage students programming skills to improve the application continuously.

OPVengineering is a start-up company at KIT. Since the cadstart application was maintained by one of the co-founders in his spare time, we want to support this software in the future.