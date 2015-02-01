Index
=======

* [Description](#markdown-header-description)
* [Installation](#markdown-header-installation)
    * [The Debian way](#markdown-header-the-debian-way)
    * [The Python pip way](#markdown-header-the-python-pip-way)
    * [The manual way](#markdown-header-the-manual-way)
* [API Reference](#markdown-header-api-reference)
* [References](#markdown-header-references)
* [Disclaimer](#markdown-header-disclaimer)

Description
===========

This is a pure Python library to access the Xiaomi Mi Band. It uses
the library called pygattlib underneath. Please see
https://bitbucket.org/OscarAcena/pygattlib
for instructions of how to install it.

If you want a **desktop application** that uses it, please see [Mibui](https://bitbucket.org/OscarAcena/mibui/overview).

**Note:** This software is tested using the 1.0.6.2 firmware version.
It may not work on other versions. If does not work for you, please issue a bug.

Installation
============

You could install this library using the provided Debian package,
through the Python pip or manually.

The Debian way
--------------

Just, add the following list to your file `/etc/sources.list`

    deb http://babel.esi.uclm.es/arco sid main

Then, update and install as always:

    $ sudo apt-get update
    $ sudo apt-get install python-mibanda

The Python pip way
------------------

As usually, using the pip tool:

    $ sudo pip install mibanda

**NOTE**: this package depends on pygattlib, which in turn, depends on
some C libraries. If you have any problem installing it, please try to
install the pygattlib depends first (listed of a file called `DEPENDS`
in the pygattlib source).

The manual way
--------------

Just download this repository and extract (or clone) to a known
location. Then make sure that your Python binary could find the miband
package. You can set the `PYTHONPATH` to the proper location (i.e: this
repo root dir) doing the following:

    miband$ . setenv.sh

Now, just import the module `mibanda`, and use it according to the API
documentation, or as in the examples.

API Reference
=============

See the [mibanda API reference](http://oscaracena.bitbucket.org/mibanda/api/).

References
==========

* http://forum.xda-developers.com/android/software/xiaomi-mi-bluetooth-le-band-protocol-t2963581
* http://allmydroids.blogspot.de/2014/12/xiaomi-mi-band-ble-protocol-reverse.html
* https://github.com/KashaMalaga/XiaomiMiBand

Disclaimer
==========

This software may harm your device. Use it at your own risk.

THERE IS NO WARRANTY FOR THE PROGRAM, TO THE EXTENT PERMITTED BY
APPLICABLE LAW. EXCEPT WHEN OTHERWISE STATED IN WRITING THE COPYRIGHT
HOLDERS AND/OR OTHER PARTIES PROVIDE THE PROGRAM “AS IS” WITHOUT
WARRANTY OF ANY KIND, EITHER EXPRESSED OR IMPLIED, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
A PARTICULAR PURPOSE. THE ENTIRE RISK AS TO THE QUALITY AND
PERFORMANCE OF THE PROGRAM IS WITH YOU. SHOULD THE PROGRAM PROVE
DEFECTIVE, YOU ASSUME THE COST OF ALL NECESSARY SERVICING, REPAIR OR
CORRECTION.