# Information Disclosure

This directory contains scripts to perform an information disclosure attack against the physical and semi-digital twins.

First, activate Poetry:

```sh
poetry install
poetry shell
```

Then launch the ARP poisoner:

```sh
sudo python3 mitm.py attack <INTERFACE>
```

Where `INTERFACE` is the interface connected to the twin system.


In another shell, running

```sh
sudo python3 sniff.py
```

will cause a stream of messages to be logged.

