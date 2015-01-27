# Font Directory Collection

This is a prototype for how the font directory could be set up as a Git repository, using submodules.

## How to use this collection repository

This collection repository uses the git 'submodule' feature to include all the font repositories. 

```sh
mkdir -p ~/src/github.com/fontdirectory;
cd ~/src/github.com/fontdirectory;
git clone https://github.com/fontdirectory/collection.git;
cd collection;
git submodule update --init --recursive;
```

To update all these submodules:

```sh
git submodule foreach git pull origin master;
```
