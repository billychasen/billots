Billots - Blockchain-Free Cryptocurrency
========================================

.. image:: http://billots.org/assets/img/logo.svg
   :width: 200px
   :align: center

http://billots.org

Billots is a cryptocurrency that doesn’t require a blockchain to prevent double spending. There are many potential benefits by not having a blockchain. Such as:

- Transactions happen in seconds instead of 10 minutes or longer.
- No fees since there’s no need to mine.
- Simpler to understand and implement.
- Smaller disk requirements.

And some cons are:

- Majority attack is possible (but can be reduced (more below)).
- Billots can become invalid.
- More complicated to send fractional amounts.

How it works
============

Billots is set up much like cash. There is a defined circulation with different denominations. Each billot has a value and an owner. When someone transfers a billot to someone else, they cryptographically prove they own that billot and broadcast a message saying who the new owner is. The new owner then checks multiple servers to see that they are the new owner. Once they confirm they are the new owner, they can consider the transaction complete (and do things like deliver goods/services).

Unlike blockchains, billots do not require the knowledge of every previous transaction to determine ownership and value.

"Trusted" servers
=================

To transact with billots, a client keeps a list of trusted servers. Trusted is a misnomer though, because you don’t really need to trust any individual server. You just need to trust that the majority of the servers on your trusted list are accurate. It is also relatively easy to see if a server is giving incorrect information based on analyzing the transaction data that is being broadcast.

Majority attacks are unfortunately a problem for all cryptocurrencies. Keeping a list of trusted servers helps protect against someone who tries to change the owner by simply running the most servers.

Double spending
===============

A good transaction works like this:

- User A broadcasts that User B is the new owner of a specified billot.
- Servers check the signature and verify the transaction and assign User B as the new owner.
- User B messages their trusted servers and sees they all report B as the owner.

Attempted double spend:

- User A broadcasts User B is the new owner and simultaneously broadcasts to different servers, User C is the owner.
- Depending how the broadcast moves around the network, some change the billot to User B and some to User C.
- User B and User C message their trusted servers and see conflicting owners and reject the billot.

The billot becomes invalid and can never be transferred again. This is akin to taking a dollar out of your pocket and destroying it.

What if User B has a completely different list of trusted servers than User C? While this would potentially allow a double spend it’s highly unlikely. Trusted server lists are not shared. User A would need to know which servers User B and User C are trusting to be an effective attack. Also, there would need to be minimal overlap in trusted servers between B and C. Lastly, B and C can employ different strategies to verify a transaction (B might want a simple majority of trusted servers, whereas C might want 90% of the entire network to agree).

Database
========

One of the benefits of no blockchain is that a new server doesn’t need to download and sync all old transactions. They can instantly start taking transactions. If a new server is asked about a billot it doesn’t know about, it can either reply that it doesn’t know or it can check its trusted servers and relay that information.

Since the database is just a list of ids and owners, its footprint is small. In testing, it takes around 25MB of storage to store the information of a million billots. Servers also keep a map of owners and which billots they own, but that functions more as a cache and isn’t completely necessary.

Cryptographic Check
===================

An owner id is a SHA-512 hash of the owner’s public key. When an owner wants to transfer a billot to a new owner, they need the new owner’s id and the billot id. The owner then signs the transfer with their private key and broadcasts the signature along with their public key. The owner is verified by checking the public key hash and signed data is correct. This ensures that only the owner can send valid transactions to change the billot owner.

Initial Supply
==============

To kick off using billots, they need to have an original owner. To help facilitate this, there is the billots.org mint that will transfer new billots.

Billots are numbered and get their value by their id prefix. Current denominations and circulation are defined as::

    {"prefix": "a-", "value": 100,   "circulation": 10000},
    {"prefix": "b-", "value": 50,    "circulation": 20000},
    {"prefix": "c-", "value": 20,    "circulation": 50000},
    {"prefix": "d-", "value": 10,    "circulation": 100000},
    {"prefix": "e-", "value": 5,     "circulation": 200000},
    {"prefix": "f-", "value": 1,     "circulation": 1000000},
    {"prefix": "g-", "value": 0.25,  "circulation": 4000000},
    {"prefix": "h-", "value": 0.1,   "circulation": 10000000},
    {"prefix": "i-", "value": 0.05,  "circulation": 30000000},
    {"prefix": "j-", "value": 0.01,  "circulation": 40000000},
    {"prefix": "k-", "value": 0.005, "circulation": 50000000}

Change
======

One issue with billots is sending exact amounts to someone. To solve this, there will need to be *change servers* that exchange larger billots for smaller values. This works much like cash in the real world. Not having exact change isn't a problem as long as other denominations are available.

Testing
=======

Testing can be done locally, but there are also two networks currently running (billots testnet runs on ``mint1.billots.org ports 17333-17335`` and live runs on ``mint1.billots.org ports 7333-7335``).

You can request testnet billots to play with at http://billots.org/test_billots.

Installing
==========

You can install using pip (requires Python 3)::

    pip install billots

Installing gives you access to the code for importing and some helpful command line scripts.

Billots Server
==============

To run the server::

    bserver [PORT]

For testing purposes, you can have the server pre-populate some billots. The prefix is for specifying the database prefix to use (this is useful if you want to run multiple servers from the same directory since leveldb databases get locked for individual processes). The private keys to the test users are in the mock folder.
::

    bserver [PORT] test --prefix=[PREFIX]

Billots Wallet
==============

The billots wallet creates keys, sends transactions, lists owned billots, and checks the owner of billots.

Create your owner private/public key
------------------------------------
::

    bwallet --genkeys 

This will put your private key in file “key” and public in “key.pub”. You can supply a different filename if desired. Your private key is unencrypted and is incredibly important to keep private and not lose. If you lose your private key there is no way to recover owned billots.

Get your owner hash
-------------------
::

    bwallet --hash

This is your owner id. It’s safe to give this to anyone that wants to send you billots. It functions much like an address in other cryptocurrencies. Similar to other cryptocurrencies, you can create as many keys and owner ids as you’d like.

List your billots
-----------------
::

    bwallet --list

Ask a server for which billots you own. This currently only asks your first trusted server. This can cause problems if that server was started after the date you received billots. Each billot returned is then verified with your trusted servers. A possible enhancement would be to poll multiple trusted servers to build a full list (or maintain the list clientside).

To check the owner of a billot
------------------------------
::

    bwallet --check-owner [ID]

This will check across your trusted servers and decide who the owner of the billot is. It will also say if the billot is disputed (different owners have been returned).
::

    bwallet --who-owns [ID]

Who owns the specified billot on one server. This is useful to see what the response is from an individual server.

Transfer a billot to a new owner
--------------------------------
::

    bwallet --transfer [ID] [TO]

Supply the ID of the billot and the owner hash that should become the new owner. Make sure you use the correct key by specifying ``keyfile``. This will broadcast the message to the server (set with ``--server``). After the transfer you can call ``check-owner`` to see if it has been successful.

Other options
-------------
::

    --server  - Specify the server for the request
                default: mint1.billots.org:7333
    --keyfile - Specify the key to use for the request (don’t include .pub, that is added automatically).
                default: key
    --trusted - Give a list of trusted hosts to use for checking ownership
                default: mint1.billots.org:7333, mint2.billots.org:7334, mint3.billots.org:7335

Testnet Example
---------------
::

If you are using testnet billots, make sure you specify the correct trusted and server arguments, such as::

    bwallet --check-owner a-1 --trusted mint1.billots.org:17333, mint2.billots.org:17334, mint3.billots.org:17335

::

    bwallet --list --trusted mint1.billots.org:17333, mint2.billots.org:17334, mint3.billots.org:17335

::

    bwallet --who-owns a-1 --server mint1.billots.org:17333

::

    bwallet --transfer a-1 67bc2eef2d... --server mint1.billots.org:17333

Testing
=======

Tests run with ``py.test``. Full test coverage is still being worked on.

There are two useful tools for launching many servers to test locally.
::

    mock_bservers

This will locally launch multiple servers on different ports.
::

    mock_disputed

This is a test script that will send different transactions to different local servers in an attempt to double spend. You can then check if it was successful by using bwallet.

You can run all the commands above with localhost after starting the server with ``bserver`` or with ``mock_bservers``
::

    bserver 7333 test --prefix=7333

::

    bwallet --who-owns a-1 --server localhost:7333

Library
=======

To import the billots library in python, use::

    import billots

You then have access to all main classes directly from ``billots``, such as ``billots.Billot()`` and ``billots.Wallet()``

**Note:** The library was written for Python 3 and requires it, however it can probably be easily modified to run on 2.x.

Classes
-------

This is a high level summary of the classes involved. There are many examples in the ``tests`` directory.

- ``Billot`` - Save/Load an individual billot, change the owner (locally in database), get the intrinsic value of it.
- ``Billots`` - Stores a list of billots.
- ``Crypto`` - All crypto methods (hashing, signing, verifying signature).
- ``Hosts`` - A list of hosts.
- ``Notifications`` - A list of seen messages from broadcasting (to minimize duplicate message handling).

- ``Server`` - All the code to implement the API and run a server.
- ``Wallet`` - Client methods to interact with a server.

Future development
==================

Billots is currently in Alpha. Anyone interested in helping is welcome to contribute. There is also a newly created subreddit (http://reddit.com/r/billots) or feel free to email me at billy [at] billychasen [dot] com.

