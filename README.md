# Folder structure
Open to change, very open to change

## /parse
These are templates/general purpose codes that are designed to process output into something that's easier to handle than what we typically get out of cooker.

One of these is for taking high verbosity debug data that's written in xml tag style to be real by an xml reader in python
The other two are for reading rootfiles, `process_rootfiles` is a lot more interesting, but need uproot. The other one is just a wrapper for filtering

## /pbg_calib
Instead of general purpose, this one is goal oriented, maybe when we learn what we wish to from it, I'll generalize and reorganize the structure as needed

## /get_cooking
These are the tools I use for setting up my environment to run cooker as well as some scripts that I link to fish/functions via `GNU stow`

## /cooker
This is obviously not all of cooker, but this is for single file analysis/sandbox for testing what goes into and out of cooker
