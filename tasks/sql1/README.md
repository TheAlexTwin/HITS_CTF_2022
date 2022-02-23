# 5ql1

## Legend

### Easy Auth (Easy)

#### RU

Сегодня каждый станет администратором.

#### EN

Today, everyone will become an administrator.

### Blind SQLi (Hard)

#### RU

Вы действительно хотите узнать, насколько глубока эта кроличья нора?

#### EN

Are you really wanna go down that rabbit hole?

## Description

Simpe SQL injections in PHP service.

## Solutions

1. Try to inject something like ```'or 1='1``` after parameters. Flag is waiting for you at ```welcome.php``` page.

2. Oh, I'm pretty lazy to prepare a write-up for a blind SQLi. Just follow usual time-based techniques and try to get flag from table with name ```secret```.

## Flags

**HITS{g00d_st4rt_br0}**

**HITS{r34lly_un3xp3ct3d_4ch13v3m3nt_f0r_4_h175_57ud3n7}**

## Handout

*nothing*

## Acknowledgements

Service originally made by https://github.com/dnyaneshwargiri
