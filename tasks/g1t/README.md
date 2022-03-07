# g1t (Medium)

## Legend

### RU

Насколько уверенно вы чувствуете себя в VCS?

### EN

How confident do you feel in your VCS?

## Description

I really lazy to invent new tasks today...

## Solution

Just iterate over all branches, print file contents and use regexp for flag format.

Alternative solution: ` $ git log -p --all -G HITS` or `$ git rev-list —all | xargs git grep HITS`

## Flag

**HITS{z45cr1pt0v4l_kr454v4}**

## Handout

```repo.zip```
