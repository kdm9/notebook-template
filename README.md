# A computational notebook infrastructure

## Installation

First, make a templated fork of this repository in github
(<https://github.com/kdm9/notebook-template>). Then clone YOUR FORK to
somewhere you want a notebook. I highly recommend you use git annex, so `git
annex init` now if you want to use it. Also, `pip install -r
.resources/requirements.txt` will set up the required python deps. You will
also need pandoc, ideally version 3.

## Usage:

```bash
# Create a directory
./new A title for today

cd <dir created above>
vim index.md
# Write something
cd ..

# Now compile it
make all 

# if you have caddy installed, you can browse it nicely with:
make serve  #unfortunately doesn't live update it
```
