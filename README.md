BattleQuip
==========
A client for the classic game Battleship.

Prerequisites
-------------
1. python 2.7
2. The will to watch an ugly Battleship board representation refresh in the terminal.

To use
------
1. Clone the repository
2. cd into the cloned repo
3. Run the following command:
    ```$ python -m battlequip <host> <username>```

Example:
    ```$ python -m battlequip "http://battleship.caseychance.com" casey```

Approach
--------
This client uses the HuntTarget strategy outlined by Nick Berry on the [DataGenetics website](http://www.datagenetics.com/blog/december32011/)
